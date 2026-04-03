
from loguru import logger
import sys




def setup_logger():
    logger.remove()
    logger.add(
        sys.stdout,
        level="DEBUG",
        format="[<level>{level}</level>] <green>{time:HH:mm:ss}</green> >  (<yellow>{extra[log_type]}</yellow>):  {message}",
        colorize=True
    )
    logger.add(
        "app.log",
        level="DEBUG",
        format="[{level}] {time:YYYY-MM-DD HH:mm:ss} > ({extra[log_type]}): {message}",
        rotation="10 MB",
        retention="1 days",
    )
    logger.bind(log_type="general")
    return logger

setup_logger()

def log(level: str="info", log_type: str="GENERAL", message: str | dict='', **kwargs) -> None:
    message_spl = ''
    if isinstance(message, dict):
        message = format_dict(message)
    if message:
        message_spl = ' | '
    if kwargs:
        message = f"{message}{message_spl}{format_dict(kwargs)}"
    log = logger.bind(log_type=log_type)
    levels = {
        'info': log.info,
        'debug': log.debug,
        'error': log.error,
        'warning': log.warning,
        'critical': log.critical
    }

    levels[level.lower()](message)

def format_dict(dictionary: dict) -> str:
    items = [f"{k}={v}" for k, v in dictionary.items()]
    return " | ".join(items)