import os
from .message import bot
from .progress import ProgressBar
from .namer import RobotNamer

# Shared logging import for both client and default.py (for headless)
QME_LOG_LEVEL = os.environ.get("QME_LOG_LEVEL", "INFO")
QME_LOG_LEVELS = ["DEBUG", "CRITICAL", "ERROR", "WARNING", "INFO", "QUIET", "FATAL"]
if QME_LOG_LEVEL not in QME_LOG_LEVELS:
    QME_LOG_LEVEL = "INFO"
