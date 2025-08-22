import sqlite3
import os

import sys

# tell interpreter where to look
sys.path.insert(0, "..")

class SqlLite:
    _instance = None
    _file_name = "database.db"
    _conn = None
    _cursor = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SqlLite, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def get_instance():
        if SqlLite._instance is None:
            SqlLite._instance = SqlLite()
        return SqlLite._instance

    def __init__(self) -> None:
        # Evita di reinizializzare se già inizializzato
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._conn = None
        self._initialized = True

    def CreateDb(self):
        try:
            self._cursor.execute(
                """ CREATE TABLE configuration (maximum_seconds INTEGER)"""
            )
            self._cursor.execute(
                """ INSERT INTO configuration (maximum_seconds) VALUES (120) """
            )
            self._cursor.execute(
                """ CREATE TABLE zone (id INT NOT NULL PRIMARY KEY, name TEXT, gpio_pin INTEGER, last_irrigation_time TEXT)"""
            )
            self._cursor.execute(
                """ CREATE TABLE scheduler (id INT NOT NULL PRIMARY KEY, zone_id INT, sheduled_time TEXT, for_how_many_seconds INT)"""
            )
            self._cursor.execute(
                """ CREATE TABLE log (zone_id INT, date_time TEXT, event INT, description TEXT)"""
            )

            self._conn.commit()
        except:
            print("Error creating db")
            self.RemoveDb()

    def DbExists(self):
        return os.path.isfile(self._file_name)

    def Init(self):
        self._conn = sqlite3.connect(self._file_name)
        self._cursor = self._conn.cursor()

    def RemoveDb(self):
        os.remove(self._file_name)

    def ExecuteQueryNoResult(self, query, params=None):
        if params is None:
            self._cursor.execute(query)
        else:
            self._cursor.execute(query, params)
        self._conn.commit()

    def ExecuteQuery(self, query, params=None):
        if params is None:
            self._cursor.execute(query)
        else:
            self._cursor.execute(query, params)
        return self._cursor.fetchall()


    def CloseConnection(self):
        if self._conn != None:
            self._conn.close()
            self._conn = None

    def __del__(self):
        self.CloseConnection()