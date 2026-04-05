import subprocess
import sys

subprocess.run([
    sys.executable, "-m", "PyInstaller",
    "--onedir",
    "--noconsole",
    "--name", "recorder",
    "--icon", "recorder_icon.ico",
    "recorder.py",
    "--collect-all", "cv2",
    "--collect-all", "numpy",
    "--collect-all", "mss",
    "--collect-all", "PIL",
    "--collect-all", "webview",
    "--collect-all", "loguru",
    "--collect-all", "soundfile"
])