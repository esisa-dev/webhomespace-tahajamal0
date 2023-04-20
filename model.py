from dataclasses import dataclass, field


@dataclass
class User:
    username:str
    password:str
    filesystem:list = field(default_factory=lambda : [])
