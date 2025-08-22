import unittest
from backend.db.SqlLite import SqlLite
import sys
import datetime

sys.path.insert(0, "..")
from backend.datatype.Zone import Zone
from backend.datatype.IrrigationInfo import IrrigationInfo
from backend.datatype.Log import Log, EventId


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
