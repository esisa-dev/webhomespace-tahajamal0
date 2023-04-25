import os
import spwd
import crypt
from model import User
from db import instance


class UserDao:
    def __init__(self) -> None:
        self.db = instance.db
        self.instance = instance

    def authenticate(self, username, password) -> bool:
        user = spwd.getspnam(username)
        salt = user.sp_pwdp
        generated_hash = crypt.crypt(password, salt)
        if generated_hash == salt:
            return True
        return False

    def refreshUser(self, username) -> dict:
        for user in self.db:
            if (user.username == username):
                self.instance.refreshUser(username)
                return user.getJSONFilesystem(f'/home/{username}')
        return {}

    def search(self, username, key):
        self.instance.searchFileDir(username, key)
        return self.instance.searchResult

    def readFile(self, path) -> str:
        f = open(path, 'r')
        data = f.read()
        return data

    def makeArchive(self, username):
        self.instance.makeArchive(username)
