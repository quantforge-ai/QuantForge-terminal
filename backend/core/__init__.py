"""Core module updated"""
from backend.core.config import settings, get_settings
from backend.core.logger import log, log_info, log_error, log_warning, log_debug
from backend.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    generate_api_key
)
# Note: Import dependencies directly from backend.core.dependencies to avoid circular imports
# from backend.core.dependencies import get_current_user, ...

__all__ = [
    "settings",
    "get_settings",
    "log",
    "log_info",
    "log_error",
    "log_warning",
    "log_debug",
    "hash_password",
    "verify_password",
    "create_access_token",
    "decode_access_token",
    "generate_api_key",
]
