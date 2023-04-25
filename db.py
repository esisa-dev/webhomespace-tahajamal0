import datetime
import spwd, os, json
from model import User

class UserDB:
  def __init__(self) -> None:
    self._db = []
    for entry in spwd.getspall():
      if(len(entry.sp_pwdp) > 2):
        self._db.append(User(entry.sp_namp, entry.sp_pwdp))
    self._initDB()

  def _initDB(self):
    if(self._db):
      for user in self._db:
        home = f'/home/{user.username}'
        user.filesystem.update( { home:{} } )
        self.__crawl(home, user.filesystem[home])

  def __initUser(self, user:User):
    if(self._db):
      home = f'/home/{user.username}'
      user.filesystem.update( { home:{} } )
      self.__crawl(home, user.filesystem[home])

  @property
  def db(self):
    return self._db

  def __crawl(self, directory, dict):
    for data in os.listdir(directory):
      path = os.path.join(directory, data)
      mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime("%d %b %Y, %H:%M")
      size = os.path.getsize(path)
      if (os.path.isfile(path)):
        if(data.split('.')[1] == "txt"):
          dict[data] = {"type":"txt", "mtime":mtime, "size":size}
        else: dict[data] = {"type":"file", "mtime":mtime, "size":size}
      elif (os.path.isdir(path)):
        dict[data] = {"type":"dir", "mtime": mtime, "size": size, "data":{}}
        self.__crawl(os.path.join(directory, data), dict[data]["data"])
    
  def refreshUser(self, username):
    for user in self._db:
      if(user.username == username):
        user.filesystem = {}
        self.__initUser(user)
        print(user.filesystem)
    
_userDB = UserDB()

def get_instance():
    return _userDB

def __getattr__(name):
    if name == 'instance':
        return get_instance()

if(__name__ == "__main__"):
  _userDB.refreshUser('test')