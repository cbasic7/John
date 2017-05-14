import sqlite3

class Sqlite3Adapter:
    def __init__(self, database_name):
        self.database_name = database_name

    def connect(self):
        self.connection = sqlite3.connect(self.database_name)

    def execute(self, sql):
        self.connection.execute(sql)
