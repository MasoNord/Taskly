from dataclasses import dataclass
from typing import Any, ClassVar, dataclass_transform, override


@dataclass_transform(kw_only_default=True)
def app_error[ClsT](cls: type[ClsT]) -> type[ClsT]:
    return dataclass(slots=True, kw_only=True)(cls)


@app_error
class AppError(Exception):
    message: str
    code: ClassVar[str]

    @property
    def meta(self) -> dict[str, Any] | None:
        return None

    @override
    def __str__(self) -> str:
        return f"{self.code}: {self.message}{'\n':<6}meta={self.meta}"