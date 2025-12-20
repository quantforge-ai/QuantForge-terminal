"""
QuantTerminal Logging Configuration
Structured logging setup using Loguru
"""

import sys
from loguru import logger
from backend.core.config import settings


def setup_logging():
    """
    Configure Loguru logger with appropriate settings
    """
    # Remove default handler
    logger.remove()
    
    # Console handler with color formatting for development
    if settings.is_development:
        logger.add(
            sys.stdout,
            colorize=True,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level=settings.LOG_LEVEL
        )
    else:
        # JSON format for production (log aggregation)
        logger.add(
            sys.stdout,
            serialize=True,  # JSON output
            level=settings.LOG_LEVEL
        )
    
    # File handler for errors
    logger.add(
        "logs/error.log",
        rotation="500 MB",
        retention="10 days",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}"
    )
    
    return logger


# Initialize logger
log = setup_logging()


# Export commonly used log functions
def log_info(message: str, **kwargs):
    """Log info message"""
    log.info(message, **kwargs)


def log_error(message: str, **kwargs):
    """Log error message"""
    log.error(message, **kwargs)


def log_warning(message: str, **kwargs):
    """Log warning message"""
    log.warning(message, **kwargs)


def log_debug(message: str, **kwargs):
    """Log debug message"""
    log.debug(message, **kwargs)
