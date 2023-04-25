import datetime
import fnmatch
import re
import shutil
import spwd
import os
import json
from model import User


class UserDB:
    def __init__(self) -> None:
        self._db = []
        for entry in spwd.getspall():
            if (len(entry.sp_pwdp) > 2):
                self._db.append(User(entry.sp_namp, entry.sp_pwdp))
        self._initDB()
        self.searchResult = []

    def _initDB(self):
        if (self._db):
            for user in self._db:
                home = f'/home/{user.username}'
                user.filesystem.update({home: {}})
                user.filesystem[home]["_nbFiles_"] = 0
                user.filesystem[home]["_nbDirs_"] = 0
                self.__crawl(home, user.filesystem[home])

    def __initUser(self, user: User):
        if (self._db):
            home = f'/home/{user.username}'
            user.filesystem.update({home: {}})
            self.__crawl(home, user.filesystem[home])

    @property
    def db(self):
        return self._db

    def __crawl(self, directory, dict):
        dict["_nbFiles_"] = 0
        dict["_nbDirs_"] = 0
        dict["_totalSize_"] = 0
        for data in os.listdir(directory):
            path = os.path.join(directory, data)
            mtime = datetime.datetime.fromtimestamp(
                os.path.getmtime(path)).strftime("%d %b %Y, %H:%M")
            size = os.path.getsize(path)
            dict["_totalSize_"] += size
            if (os.path.isfile(path)):
                dict["_nbFiles_"] += 1
                if (data.split('.')[1] == "txt"):
                    f = open(path, 'r')
                    content = f.read()
                    bad_char_pattern = re.compile(r'[\x00-\x1F\x7F-\x9F]')
                    clean_contents = bad_char_pattern.sub('', content)
                    f.close()
                    dict[data] = {"type": "txt", "mtime": mtime,
                                  "size": size, "content": clean_contents}
                else:
                    dict[data] = {"type": "file", "mtime": mtime, "size": size}
            elif (os.path.isdir(path)):
                dict["_nbDirs_"] += 1
                dict[data] = {"type": "dir", "mtime": mtime,
                              "size": size, "data": {}}
                self.__crawl(os.path.join(directory, data), dict[data]["data"])

    def refreshUser(self, username):
        for user in self._db:
            if (user.username == username):
                user.filesystem = {}
                self.__initUser(user)
                # print(user.filesystem)

    def searchRec(self, keyword, directory, k):
        if (keyword in k):
            self.searchResult.append((k, directory))
        if directory['type'] == 'dir':
            if (isinstance(directory['data'], dict)):
                for key, value in directory['data'].items():
                    if (isinstance(value, dict)):
                        if value['type'] == 'file' or (value['type'] == 'txt'):
                            if (keyword in key):
                                self.searchResult.append((key, value))
                        if (value['type'] == 'dir'):
                            self.searchRec(keyword, value, key)

    def searchFileDir(self, username, keyword):
        self.searchResult = []
        for user in self.db:
            if (user.username == username):
                fs = user.filesystem[f'/home/{username}']
                for data in fs:
                    if (isinstance(fs[data], dict)):
                        self.searchRec(keyword, fs[data], data)

    def filePath(self, username, filename):
        for root, dirs, files in os.walk(f'/home/{username}'):
            for filename in fnmatch.filter(files, filename):
                yield os.path.join(root, filename)

    def makeArchive(self, username):
        shutil.make_archive(f'/home/{username}',
                            'zip', f'/home/', f'{username}')


_userDB = UserDB()


def get_instance():
    return _userDB


def __getattr__(name):
    if name == 'instance':
        return get_instance()


if (__name__ == "__main__"):
    # print(_userDB.db[0].filesystem['/home/dev'].items())
    # _userDB.searchFileDir('test', 'text')
    _userDB.makeArchive('dev')
    # print(len(_userDB.searchResult))
    # for query in _userDB.searchResult:
    #     print(query)
