import sounddevice as sd
import soundfile as sf
import queue
import threading
import numpy as np
import time
from LogManager import log
mic_queue = queue.Queue()
system_queue = queue.Queue()

stop_event = threading.Event()

mic_stream = None
system_stream = None


# ---------------- MIC ----------------
def start_recording_mic(device: int, fs: int = 44100, channels: int = 1) -> None:
    global mic_stream
    mic_stream = sd.InputStream(
        device=device,
        samplerate=fs,
        channels=channels,
        blocksize=1024,
        callback=mic_callback
    )
    mic_stream.start()
    log(log_type="MICRECORD", message="Mic recording started")


def mic_callback(indata, frames, time, status):
    if status:
        log(level="debug", log_type="MICCALLBACK", status=status)
    mic_queue.put(indata.copy())


# ---------------- SYSTEM AUDIO ----------------

def start_recording_system(device: int, fs: int = 44100, channels: int = 2) -> None:
    global system_stream
    system_stream = sd.InputStream(
        device=device,
        samplerate=fs,
        channels=channels,
        blocksize=1024,
        callback=system_callback
    )
    system_stream.start()
    log(log_type="SYSTEMRECORD", message="System audio recording started")



def system_callback(indata, frames, time, status):
    if status:
        log(level="debug", log_type="SYSTEMCALLBACK", status=status)
    system_queue.put(indata.copy())


# ---------------- STOP ----------------

def stop_audio() -> None:
    global mic_stream, system_stream
    stop_event.set()
    if mic_stream:
        mic_stream.stop()
        mic_stream.close()
        log(log_type="MICRECORD", message="Mic audio recording stopped")
    if system_stream:
        system_stream.stop()
        system_stream.close()
        log(log_type="SYSTEMRECORD", message="System audio recording stopped")

# ---------------- DEVICE FINDERS ----------------

def find_mic() -> int:
    devices = sd.query_devices()
    for i, d in enumerate(devices):
        if "microphone" in d["name"].lower():
            log(log_type="FINDMIC", message="Found mic", name=d["name"], index=i)
            return i
    log(level="error", log_type="FINDMIC", message="Mic not found")
    raise RuntimeError("Mic not found")


def find_stereo_mix() -> int:
    devices = sd.query_devices()
    for i, d in enumerate(devices):
        if "stereo mix" in d["name"].lower():
            log(log_type="FINDSTEREO", message="Found stereo mix", name=d["name"], index=i)
            return i
    log(level="error", log_type="FINDSTEREO", message="Stereo Mix not found")
    raise RuntimeError("Stereo Mix not found")


# ---------------- SAVE ----------------

def save_audio(filename: str, ismic: bool = True, issystem: bool = True) -> None:
    fs = 44100
    if ismic and issystem:
        save_mix_audio(filename, fs)

    elif issystem:
        save_mono_audio(filename, fs, system_queue)
    elif ismic:
        save_mono_audio(filename, fs, mic_queue)

def save_mix_audio(filename: str, fs: int) -> None:
    mic = queue_to_array(mic_queue)
    system = queue_to_array(system_queue)
    if len(mic) == 0 and len(system) == 0:
        log(level="error", log_type="AUDIOMIX", message="No audio captured")
        return
    offset = find_offset(system, mic)
    log(level="debug", log_type="AUDIOMIX", offset=offset)
    if offset > 0:
        mic = mic[offset:]
    else:
        system = system[-offset:]
    min_len = min(len(mic), len(system))
    mic = mic[:min_len]
    system = system[:min_len]
    if mic.ndim == 1 or mic.shape[1] == 1:
        mic = np.repeat(mic, 2, axis=1)
    mixed = (system + mic) * 0.5
    sf.write(filename, mixed, fs)
    log(log_type="SAVING", message="Save mix audio", file=filename)

def save_mono_audio(filename: str, fs: int, audio_queue) -> None:
    audio = queue_to_array(audio_queue)
    sf.write(filename, audio, fs)
    log(log_type="SAVING", message="Saved mono audio", file=filename)

def queue_to_array(q) -> np.ndarray:
    data = []
    while not q.empty():
        data.append(q.get())
    if len(data) == 0:
        return np.array([])
    return np.concatenate(data)


def find_offset(a, b, max_offset=44100):
    a = a[:,0]
    b = b[:,0]
    corr = np.correlate(a[:max_offset], b[:max_offset], mode="full")
    offset = corr.argmax() - (len(a[:max_offset]) - 1)
    return offset


if __name__ == "__main__":
    mic = find_mic()
    system = find_stereo_mix()

    start_recording_mic(mic)
    start_recording_system(system)

    time.sleep(10)

    stop_audio()

    save_audio("capture/audio.wav")