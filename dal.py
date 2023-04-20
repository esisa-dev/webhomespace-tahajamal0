import os, spwd, crypt
from model import User

class UserDao:
  def __init__(self) -> None:
    f=open('/etc/shadow', 'r')
    self.data = f.readlines()
    f.close()

  def authenticate(self, username, password) -> bool:
      user = spwd.getspnam(username)
      salt = user.sp_pwdp
      generated_hash = crypt.crypt(password, salt)
      if generated_hash == salt:
        return True
      return False