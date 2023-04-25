from dataclasses import dataclass, field
import json

@dataclass
class User:
  username:str
  password:str
  filesystem:dict = field(default_factory=dict)

  def getJSONFilesystem(self, key):
    return json.dumps(self.filesystem[key])

