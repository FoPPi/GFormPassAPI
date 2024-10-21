import logging
import sys
from pathlib import Path
from loguru import logger
from fastapi.logger import logger as fastapi_logger

class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

def setup_logging(log_level: str = "INFO", json_logs: bool = False):
    # Remove all existing handlers
    logging.root.handlers = []
    fastapi_logger.handlers = []

    # Set log level
    logging.root.setLevel(log_level)

    # Configure loguru
    logger.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "level": log_level,
                "serialize": json_logs,
                "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level> | <dim>{extra}</dim>"
            },
            {
                "sink": Path("logs/app.log"),
                "rotation": "500 MB",
                "retention": "10 days",
                "level": log_level,
                "serialize": json_logs,
                "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level> | <dim>{extra}</dim>"
            }
        ]
    )

    # Intercept standard logging messages toward loguru
    logging.getLogger().handlers = [InterceptHandler()]

    # Other loggers
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    return logger

# Create logger instance
logger = setup_logging()