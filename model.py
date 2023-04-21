from dataclasses import dataclass, field


@dataclass
class User:
    username:str
    password:str
    filesystem:dict = field(default_factory=dict)
