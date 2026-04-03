import os
import webview
from time import sleep
from PIL import Image
from RecordManager import record, stop_record, save_video
from DirManager import ask_directory, get_dir, video_cap, screenshot_dir, clean_cap, BASE_DIR, WEB_DIR
import mss
from LogManager import log


settings = {'fps': '80', 'resolution': '1440p', 'volume': True, 'micro': True}
region = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}



window = None

recording = False


class Api:

    def start_record(self, api_settings: dict) -> dict[str, str]:
        global settings, recording
        settings = api_settings
        record(settings, region)
        log(log_type="RECORDING", message="Start recording")
        log(log_type="SETTINGS", message=settings)
        recording = True
        return {"status": "recording"}

    def stop_record(self) -> dict[str, str]:
        global recording
        stop_record(settings)
        log(log_type="RECORDING", message="Stop recording")
        recording = False
        return {"status": "stopped"}

    def save_file(self, filename: str, filetype: str) -> None:
        save_video(f'{filename}.{filetype}')
        log(log_type="SAVING", file=f"{get_dir()}/{filename}.{filetype}")

    def screen_size_selector(self) -> None:
        window.minimize()
        sleep(0.2)
        save_screen()
        open_selector()

    def get_directory(self) -> None:
        ask_directory()
        log(log_type="DIRECTORY", folder=f"{get_dir()}")

    def open_preview(self) -> None:
        os.startfile(video_cap())
        log(log_type="PREVIEW", message="Opened preview video")

    def close(self) -> None:
        window.destroy()


    def minimize(self) -> None:
        window.minimize()
        log(log_type="APP", message="Program minimized")



class ApiSelector:

    def __init__(self) -> None:
        self.screen = None

    def set_capture_area(self, area: dict) -> None:
        global region
        region = area
        log(log_type="REGION", message=area)

    def get_screen(self) -> None:
        log(log_type="REGION", message="Make screenshot")
        return self.screen

    def close_selector(self) -> None:
        webview.windows[-1].destroy()
        window.restore()
        emit(window, 'render-size-icon', {"screen": "selected"})
        os.remove(screenshot_dir)






def open_app_window() -> None:
    global window, api
    window = webview.create_window(
        "Screen Recorder",
        os.path.join(WEB_DIR, "index.html"),
        width=750,
        height=480,
        resizable=False,
        frameless=True,
        easy_drag=True,
        js_api=api
    )
    webview.start()


def open_selector() -> None:
    global api_selector
    webview.create_window(
        "Select Area",
        os.path.join(WEB_DIR, "selector.html"),
        fullscreen=True,
        on_top=True,
        easy_drag=False,
        js_api=api_selector
    )




def get_full_screen() -> tuple[int, int, int, int]:
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        return monitor["left"], monitor["top"], monitor["width"], monitor["height"]


def save_screen() -> None:
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        img = sct.grab(monitor)
        image = Image.frombytes("RGB", img.size, img.rgb)
        image.save(screenshot_dir)



def update_region(top: int = None, left: int = None, width: int = None, height: int = None) -> None:
    global region
    if top: region['top'] = top
    if left: region['left'] = left
    if width: region['width'] = width
    if height: region['height'] = height



def emit(window, event: str, data: dict) -> None:
    import json
    window.evaluate_js(
        f"window.dispatchEvent(new CustomEvent('{event}', {{detail:{json.dumps(data)}}}))"
    )
    log(log_type="EMIT", message=data, event=f'{event}')

def clean_up() -> None:
    if recording:
        stop_record(settings)
        log(log_type="RECORDING", message='Recording interrupt')
    clean_cap()



api_selector = ApiSelector()
api = Api()

if __name__ == "__main__":
    update_region(*get_full_screen())
    open_app_window()

