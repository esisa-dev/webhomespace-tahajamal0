import os, spwd, crypt
from model import User
from db import instance

class UserDao:
  def __init__(self) -> None:
    self.db = instance

  def authenticate(self, username, password) -> bool:
      user = spwd.getspnam(username)
      salt = user.sp_pwdp
      generated_hash = crypt.crypt(password, salt)
      if generated_hash == salt:
        return True
      return False