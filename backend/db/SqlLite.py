import sqlite3
import os
import threading
import sys

# tell interpreter where to look
sys.path.insert(0, "..")

class SqlLite:
    _instance = None
    _lock = threading.Lock()  # Class-level lock for singleton creation
    _file_name = "database.db"
    _conn = None
    _cursor = None

    def __new__(cls, *args, **kwargs):
        # Double-checked locking pattern for thread-safe singleton
        if cls._instance is None:
            cls._instance = super(SqlLite, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def get_instance():
        # Thread-safe singleton access
        if SqlLite._instance is None:
            print("Creating new SqlLite instance")
            with SqlLite._lock:
                print("Acquired lock for SqlLite instance creation")
                SqlLite._instance = SqlLite()
        return SqlLite._instance

    def __init__(self) -> None:
        # Evita di reinizializzare se già inizializzato
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._conn = None
        self._db_lock = threading.RLock()  # Instance-level lock for database operations
        self._initialized = True

    def CreateDb(self):
        with self._db_lock:
            self.OpenConnection()
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
            except Exception as e:
                print(f"Error creating db: {e}")
                self.RemoveDb()
            finally:
                self.CloseConnection()  

    def DbExists(self):
        return os.path.isfile(self._file_name)

    def OpenConnection(self):
        with self._db_lock:
            if self._conn is None:
                # Enable thread safety and check same thread = False for multi-threaded access
                self._conn = sqlite3.connect(self._file_name, check_same_thread=False)
                # Enable WAL mode for better concurrent access
                self._conn.execute('PRAGMA journal_mode=WAL;')
                self._cursor = self._conn.cursor()

    def RemoveDb(self):
        os.remove(self._file_name)

    def ExecuteQueryNoResult(self, query, params=None):
        with self._db_lock:
            self.OpenConnection()
            try:
                if params is None:
                    self._cursor.execute(query)
                else:
                    self._cursor.execute(query, params)
                self._conn.commit()
            except Exception as e:
                print(f"Error executing query (no result): {e}")
                self._conn.rollback()
                raise
            finally:
                self.CloseConnection()

    def ExecuteQuery(self, query, params=None):
        with self._db_lock:
            self.OpenConnection()
            try:
                if params is None:
                    self._cursor.execute(query)
                else:
                    self._cursor.execute(query, params)
                return self._cursor.fetchall()
            except Exception as e:
                print(f"Error executing query: {e}")
                raise
            finally:
                self.CloseConnection()  


    def CloseConnection(self):
        with self._db_lock:
            if self._conn is not None:
                try:
                    self._conn.close()
                    self._conn = None
                    self._cursor = None
                except Exception as e:
                    print(f"Error closing connection: {e}")

    def __del__(self):
        try:
            self.CloseConnection()
        except:
            pass  # Ignore errors during cleanup