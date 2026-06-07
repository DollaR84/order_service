from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class BaseData:

    def dict(self, exclude_unset: bool = False, exclude: set[str] | None = None) -> dict[str, Any]:
        result = {}

        for key, value in asdict(self).items():
            value = getattr(self, key)

            if exclude_unset and value is None:
                continue

            if exclude and key in exclude:
                continue

            result[key] = value
        return result
