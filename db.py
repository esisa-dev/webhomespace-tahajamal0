import spwd, os
from model import User

class UserDB:
  def __init__(self) -> None:
    self._db = []
    for entry in spwd.getspall():
      if(len(entry.sp_pwdp) > 2):
        self._db.append(User(entry.sp_namp, entry.sp_pwdp))
    if(self._db):
      for user in self._db:
        home = f'/home/{user.username}'
        user.filesystem.update( { home:{} } )
        self.__crawl(home, user.filesystem[home])

  @property
  def db(self):
    return self._db

  def __crawl(self, directory, dict):
    for data in os.listdir(directory):
      if (os.path.isfile(os.path.join(directory, data))):
        if(data.split('.')[1] == 'txt'):
          dict[data] = 'txt'
        else: dict[data] = 'file'
      elif (os.path.isdir(os.path.join(directory, data))):
        dict[data] = {}
        self.__crawl(os.path.join(directory, data), dict[data])

  def print_files(self, curr_dict, indent=''):
    for key, value in curr_dict.items():
        if isinstance(value, dict):
            print(indent + key + '/')
            self.print_files(value, indent + '    ')
        else:
            print(indent + key)
    
_userDB = UserDB()

def get_instance():
    return _userDB

def __getattr__(name):
    if name == 'instance':
        return get_instance()

if(__name__ == "__main__"):
  userDB = UserDB()
  udb = userDB.db[1].filesystem
  userDB.print_files(udb)
  # print(udb)