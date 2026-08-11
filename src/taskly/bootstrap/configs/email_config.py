
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EmailConnectionConfig:
    hostname: str
    port: int
    sender: str
    username: str
    password: str
    use_tls: bool
    use_ssl: bool

@dataclass(frozen=True, slots=True)
class EmailTemplateRendererConfig:
    template_path_folder: str
