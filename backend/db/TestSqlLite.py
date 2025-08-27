import unittest
from backend.db.SqlLite import SqlLite
import sys

sys.path.insert(0, "..")


class TestInitSqlLite(unittest.TestCase):
    db = None

    @classmethod
    def setUpClass(self):
        self.db = SqlLite()
        self.db.Init()
        self.db.CreateDb()

    @classmethod
    def tearDownClass(self):
        self.db.RemoveDb()


if __name__ == "__main__":
    unittest.main()
