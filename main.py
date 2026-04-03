from LogManager import log
from DirManager import generate_time_id, config_cap_dir, debag
from UXManager import open_app_window, update_region, get_full_screen, clean_up




def start_app() -> None:
    debag()
    log(log_type="APP", message="Program started")
    generate_time_id()
    config_cap_dir()
    update_region(*get_full_screen())
    log(log_type="APP", message="Open window")
    open_app_window()
    clean_up()
    log(log_type="APP", message="Program closed")




start_app()






