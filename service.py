from dal import UserDao

class UserService:
  def __init__(self) -> None:
    self.dao = UserDao()

  def authenticate(self, username, password) -> bool :
    return self.dao.authenticate(username, password)

  def getUserData(self, username) -> dict:
    for user in self.dao.db:
      if(user.username == username):
        return user.filesystem
    return {}