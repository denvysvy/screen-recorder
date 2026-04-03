from SystemRecord import start_recording_mic, start_recording_system, stop_audio, find_mic, find_stereo_mix, save_audio
from ScreenRecord import start_recording, stop_recording
import subprocess
import os
from DirManager import is_file_cap_exists, remove_cap, video_cap, audio_cap, correct_name, combine_filename_with_dir, BASE_DIR
from LogManager import log



def record(settings: dict, region: dict) -> None:
    mic_id, sound_id = config_audio(settings["micro"], settings["volume"])
    start_recording(video_cap(), region, int(settings['fps']), debag = True)
    if mic_id:
        start_recording_mic(mic_id)
    if sound_id:
        start_recording_system(sound_id)

def stop_record(settings: dict) -> None:
    stop_recording()
    if settings["micro"] or settings["volume"]  :
        stop_audio()
        save_audio(audio_cap(), settings['micro'], settings["volume"])


def save_video(filename: str) -> None:
    filename = correct_name(filename)
    filename = combine_filename_with_dir(filename)
    if is_file_cap_exists("audio"):
        merge_video_audio(out=filename)
        remove_cap("audio")
        remove_cap("video")
    elif is_file_cap_exists("video"):
        convert_video_no_audio(out=filename)
        remove_cap("video")
    else:
        log(level="error", log_type="SAVING", message="No video file found")




def config_audio(isMic: bool, isSound: bool) -> tuple[int, int]:
    mic_id = None
    sound_id = None
    if isMic:
        mic_id = find_mic()
    if isSound:
        sound_id = find_stereo_mix()
    return mic_id, sound_id


def merge_video_audio(out: str) -> None:
    ext = os.path.splitext(out)[1].lower()
    if ext == ".mp4":
        vcodec = "libx264"
        acodec = "aac"
        extra_flags = ["-movflags", "+faststart"]
    elif ext == ".webm":
        vcodec = "libvpx-vp9"
        acodec = "libopus"
        extra_flags = []
    elif ext == ".ogg":
        vcodec = "libtheora"
        acodec = "libvorbis"
        extra_flags = []
    else:
        log(level="error", log_type="MERGEVIDEO", message=f"Unsupported format: {ext}")
        raise ValueError(f"Unsupported format: {ext}")
    cmd = [
        os.path.join(BASE_DIR, "ffmpeg/bin/ffmpeg.exe"),
        "-i", video_cap(),
        "-i", audio_cap(),
        "-c:v", vcodec,
        "-c:a", acodec,
        "-shortest",
        *extra_flags,
        out
    ]
    subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    log(level="debug", log_type="MERGEVIDEO", message="Video merged", extention=ext, vcodec=vcodec)

def convert_video_no_audio(out: str) -> None:
    ext = os.path.splitext(out)[1].lower()
    if ext == ".mp4":
        vcodec = "libx264"
        extra_flags = ["-movflags", "+faststart"]

    elif ext == ".webm":
        vcodec = "libvpx-vp9"
        extra_flags = []

    elif ext == ".ogg":
        vcodec = "libtheora"
        extra_flags = []
    else:
        log(level="error", log_type="CONVERTVIDEO", message=f"Unsupported format: {ext}")
        raise ValueError(f"Unsupported format: {ext}")

    cmd = [
        os.path.join(BASE_DIR, "ffmpeg/bin/ffmpeg.exe"),
        "-i", video_cap(),
        "-c:v", vcodec,
        "-an",
        *extra_flags,
        out
    ]
    subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    log(level="debug", log_type="CONVERTVIDEO", message="Video converted" , extention=ext, vcodec=vcodec)