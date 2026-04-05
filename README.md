# 🎥 Screen Recorder (Python)

A multi-threaded screen recording application for Windows built with Python. The project uses a WebView-based UI and supports screen capture, audio recording, and post-processing with FFmpeg.

---

## 🚀 Features

-   📺 Screen recording (full screen or selected area)
    
-   🖱️ Area selection using a built-in selector tool
    
-   🎧 Microphone recording (optional)
    
-   🔊 System audio recording (optional)
    
-   ⚡ Multi-threaded architecture:
    
    -   Screen capture thread (takes screenshots)
    -   Frame processing/writing thread
    -   Logging thread (frame drops, timing, performance)
    -   Microphone recording thread
    -   System audio recording thread
-   🧠 Performance logging (FPS, dropped frames, timing)
    
-   🌐 Web-based UI using WebView
    
-   💾 Save recordings to a selected directory
    
-   🎬 FFmpeg integration for:
    
    -   Combining audio & video
    -   Converting to desired formats

---

## 🧩 Project Structure

-   `main.py` → used for debugging and development
    
-   `recorder.py` → used for building the `.exe` version by `biuld.py`
    
-   `web/` → UI (HTML, CSS, JavaScript)
    
-   core modules:
    
    -   `ScreenRecord.py`
    -   `RecordManager.py`
    -   `SystemRecord.py`
    -   `LogManager.py`
    -   `UXManager.py`
    -   `DirManager.py`

---

## 📦 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

Main libraries used:

-   opencv-python (`cv2`)
-   numpy
-   mss
-   pillow (`PIL`)
-   pywebview
-   loguru
-   soundfile

Built-in modules:

-   queue
-   threading
-   time
-   os
-   subprocess
-   sys
-   tkinter

For biulding exe:

-   pyinstaller
---

## ⚙️ FFmpeg

This project requires **FFmpeg** for video processing.

It is used for:

-   merging audio and video
-   encoding output files

👉 You must install FFmpeg and add it to your system PATH: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

👉 And make sure you have right path to `ffmpeg.exe` same as `ffmpeg\bin\ffmpeg.exe`

---

## 🖥️ Usage

Run in development mode:

```bash
python main.py
```

---

## 📦 Build (EXE)

To build the executable version:

```bash
python build.py
```

---

## 📁 Output

After recording:

-   You can choose a directory
-   The app will process and save the final video file

---

## 🧠 How It Works

The recorder uses multiple threads:

1.  Screen capture thread → grabs frames (screenshots)
2.  Writer thread → processes and saves frames
3.  Logging thread → tracks FPS, dropped frames, timing
4.  Audio threads → record microphone and/or system audio
5.  FFmpeg → merges everything into final output

---

## 📸 UI

The interface is built using HTML/CSS/JS and rendered via WebView.

---

## 📜 License

MIT License

---

## ⚠️ Notes

-   Performance depends on your hardware
-   High FPS recording may increase CPU usage
-   Make sure FFmpeg is correctly installed

---

## 💡 Future Improvements

-   GPU acceleration
-   Better audio sync
-   Cross-platform support
-   UI improvements
-   Using FFmpeg for recording

---