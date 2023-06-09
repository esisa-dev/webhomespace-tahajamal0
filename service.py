from dal import UserDao


class UserService:
    def __init__(self) -> None:
        self.dao = UserDao()

    def authenticate(self, username, password) -> bool:
        return self.dao.authenticate(username, password)

    def getUserData(self, username) -> dict:
        for user in self.dao.db:
            if (user.username == username):
                return user.getJSONFilesystem(f'/home/{username}')
        return {}

    def refreshUser(self, username) -> dict:
        return self.dao.refreshUser(username)

    def readFile(self, path) -> str:
        return self.dao.readFile(path)

    def searchFile(self, username, key):
        return self.dao.search(username, key)

    def makeArchive(self, username):
        self.dao.makeArchive(username)
