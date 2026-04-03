import cv2
import numpy as np
import mss
import queue
import time
import threading
import os
from LogManager import log



capture_counter = 0
write_counter = 0
dropped_frames = 0
duplicated_frames = 0

capture_times = []
write_times = []

stop_event = threading.Event()
video_queue = queue.Queue(maxsize=30)

record_thread = None
writer_thread = None




def start_recording(filename: str, region: dict, fps: int = 24, debag:bool = True) -> None:
    global record_thread, writer_thread
    stop_event.clear()
    record_thread = threading.Thread(
        target=record_screen,
        args=(region, fps),
        daemon=True
    )
    writer_thread = threading.Thread(
        target=write_video,
        args=(region, filename, fps),
        daemon=True
    )
    record_thread.start()
    writer_thread.start()
    if debag:
        debug_thread = threading.Thread(
            target=debug_monitor,
            daemon=True
        )
        debug_thread.start()

def stop_recording() -> None:
    stop_event.set()
    if record_thread and writer_thread:
        record_thread.join()
        writer_thread.join()




def record_screen(region: dict, fps: int) -> None:
    log(log_type="VIDEORECORD", message="Video started")
    with mss.mss() as sct:
        frame_time = 1 / fps
        next_frame_time = time.perf_counter()
        while not stop_event.is_set():
            now = time.perf_counter()
            if now < next_frame_time:
                time.sleep(next_frame_time - now)
            frame = capture_frame(sct, region)
            timestamp = time.perf_counter()
            try:
                video_queue.put((frame, timestamp), block=False)
            except queue.Full:
                global dropped_frames
                dropped_frames += 1
            next_frame_time += frame_time

def capture_frame(sct, region: dict) -> None:
    global capture_counter
    start = time.perf_counter()
    img = sct.grab(region)
    capture_counter += 1
    frame = np.asarray(img)
    frame = frame[..., :3]
    capture_times.append(time.perf_counter() - start)
    return frame


def write_video(region: dict, filename: str, fps: int = 24) -> None:
    global write_counter, duplicated_frames
    out = create_video_writer(region["width"], region["height"], filename, fps)
    frame_time = 1 / fps
    expected_ts = None
    last_frame = None
    while not stop_event.is_set() or not video_queue.empty():
        try:
            start = time.perf_counter()
            frame, ts = video_queue.get(timeout=0.1)
            if expected_ts is None:
                expected_ts = ts
            delta = ts - expected_ts
            missed = int(delta / frame_time)
            if missed < 0:
                missed = 0
            if missed > fps:
                missed = fps
            for _ in range(missed):
                if last_frame is not None:
                    out.write(last_frame)
                    duplicated_frames += 1
                expected_ts += frame_time
            out.write(frame)
            expected_ts += frame_time
            last_frame = frame
            write_times.append(time.perf_counter() - start)
            write_counter += 1
        except queue.Empty:
            continue
    out.release()

def create_video_writer(width: int, height: int, filename: str, fps: int) -> cv2.VideoWriter:
    log(log_type="VIDEOWRITER", fourcc="XVID")
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    return cv2.VideoWriter(filename, fourcc, fps, (width, height))




def debug_monitor() -> None:
    global capture_counter, write_counter, duplicated_frames

    while not stop_event.is_set():
        time.sleep(1)

        capture_fps = capture_counter
        write_fps = write_counter
        queue_size = video_queue.qsize()

        dup = duplicated_frames
        duplicated_frames = 0

        capture_counter = 0
        write_counter = 0

        if capture_times:
            avg_capture = sum(capture_times[-50:]) / min(len(capture_times), 50)
        else:
            avg_capture = 0

        if write_times:
            avg_write = sum(write_times[-50:]) / min(len(write_times), 50)
        else:
            avg_write = 0

        log(
            level="debug",
            log_type="VIDEORECORD",
            capture_fps=capture_fps,
            write_fps=write_fps,
            queue=queue_size,
            dropped=dropped_frames,
            duplicated=dup,
            capture_time=f"{avg_capture:.4f}s",
            write_time=f"{avg_write:.4f}s"
        )















