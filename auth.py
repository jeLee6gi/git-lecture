from crypt import crypt
import getpass
import pickle
import sys


class PWDB:
    def __init__(self, path):
        self.salt = "$6$DzRM4CMIlJMyjc40"
        self.path = path
        self._db = None

    def authenticate(self, username, password):
        if username in self._db:
            if crypt(password, salt=self.salt) == self._db[username]:
                return True
        return False

    def add_user(self, username, password):
        if username not in self._db:
            self._db[username] = crypt(password, salt=self.salt)

    def _read_pwdb(self):
        try:
            with open(self.path, "rb") as h:
                self._db = pickle.load(h)
        except FileNotFoundError:
            self._db = {}

    def _write_pwdb(self):
        with open(self.path, "wb") as h:
            pickle.dump(self._db, h)

    def __enter__(self):
        self._read_pwdb()
        return self

    def __exit__(self, *args):
        self._write_pwdb()


def get_credentials():
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    return username, password


if __name__ == "__main__":
    DEFAULT_PWDB = "pwdb.pkl"

    with PWDB(DEFAULT_PWDB) as pwdb:
        username, password = get_credentials()

        if pwdb.authenticate(username, password):
            print("Successfull authentication", username, password)
        else:
            ans = input(
                "User not known or password is wrong. Do you want to add the "
                "user to the password database? [y/n]"
            )

            if ans == "y":
                pwdb.add_user(username, password)
