from mysql import connector

from .constants import *


class Database:

    def __init__(self, host, port, user, password, database):
        self.connection = connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

        cursor = self.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS users (id VARCHAR(%s), name VARCHAR(%s))", [MAX_CHARACTERS_IN_USER_ID, MAX_CHARACTERS_IN_USER_NAME])
        cursor.execute("CREATE TABLE IF NOT EXISTS permissions (user VARCHAR(%s), permission VARCHAR(%s), PRIMARY KEY (user, permission))", [MAX_CHARACTERS_IN_USER_ID, MAX_CHARACTERS_IN_PERMISSION])

    def cursor(self):
        return self.connection.cursor()

    def __enter__(self):
        return self.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()

    def get_user(self, id):
        cursor = self.cursor()
        cursor.execute("SELECT id, name FROM users WHERE id=%s", [id])

        for value in cursor:
            return value

    def set_user(self, id, name):
        with self as cursor:
            cursor.execute("INSERT INTO users (id, name) VALUES (%s, %s)", [id, name])

    def has_permission(self, user, permission):
        cursor = self.cursor()
        cursor.execute("SELECT permission FROM permissions WHERE user=%s AND permission=%s", [user, permission])

        for _ in cursor:
            return True

    def get_permissions(self, user):
        cursor = self.cursor()
        cursor.execute("SELECT permission FROM permissions WHERE user=%s", [user])

        permissions = []
        for value in cursor:
            permissions.append(value)
        return permissions

    def add_permission(self, user, permission):
        with self as cursor:
            cursor.execute("INSERT INTO permissions (user, permission) VALUES (%s, %s)", [user, permission])

    def remove_permission(self, user, permission):
        with self as cursor:
            cursor.execute("DELETE FROM permissions WHERE user=%s AND permission=%s", [user, permission])

    def get_users_with_permission(self, permission):
        cursor = self.cursor()
        cursor.execute("SELECT user FROM permissions WHERE permission=%s", [permission])

        users = []
        for value in cursor:
            users.append(int(value[0]))
        return users
