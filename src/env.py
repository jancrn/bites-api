import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


def get(key: str, default: Optional[str] = None) -> str:
    value = os.environ.get(key, default)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value


def get_int(key: str, default: Optional[int] = None) -> int:
    value = os.environ.get(key)
    if value is not None:
        return int(value)
    if default is not None:
        return default
    raise RuntimeError(f"Missing required integer environment variable: {key}")


def get_bool(key: str, default: Optional[bool] = None) -> bool:
    value = os.environ.get(key)
    if value is not None:
        return value.lower() in ("1", "true", "yes", "on")
    if default is not None:
        return default
    raise RuntimeError(f"Missing required boolean environment variable: {key}")
