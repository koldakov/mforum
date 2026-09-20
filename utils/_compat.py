import tomllib
from typing import Any


def _get_config() -> dict[str, Any]:
    with open("pyproject.toml", "rb") as f:
        return tomllib.load(f)


config: dict[str, Any] = _get_config()
