"""
Unit tests for PersistentLogDAO: verifies logging and retrieval of persistent log entries.
"""

import datetime
from time import sleep
import unittest
from backend.db.SqlLite import SqlLite
from backend.dao.persistent_log_dao import PersistentLogDAO
from backend.datatype.log import Log, EventId


class TestPersistentLog(unittest.TestCase):
    """
    Test suite for PersistentLogDAO database operations.
    """

    db = None

    @classmethod
    def setUpClass(cls):
        """
        Set up the test database before running tests.
        """
        print("Setting up the database for IrrigationInfoDAO tests")
        cls.db = SqlLite.get_instance()
        cls.db.CreateDb()

    @classmethod
    def tearDownClass(cls):
        """
        Remove the test database after running tests.
        """
        print("Tearing down the database after IrrigationInfoDAO tests")
        cls.db.RemoveDb()

    def test_add_log(self):
        """
        Test adding a single log entry and retrieving it from the database.
        """
        print("==== test add log =====")
        log_to_add = Log(
            zone_id=1,
            date_time=datetime.datetime.now(),
            event_id=EventId.general,
            log="Test log entry",
        )
        PersistentLogDAO.add_log(log_to_add)
        logs = PersistentLogDAO.get_logs(1)
        self.assertNotEqual(len(logs), 0)
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0].zone_id, log_to_add.zone_id)
        self.assertEqual(logs[0].event_id, log_to_add.event_id)
        self.assertEqual(logs[0].log, log_to_add.log)
        # self.assertEqual(logs[0], log_to_add)

    def test_add_more_then_one_log(self):
        """
        Test adding multiple log entries and retrieving them with filters and limits.
        """
        print("==== test add more than one log =====")
        log_to_add_1 = Log(
            zone_id=2,
            date_time=None,
            event_id=EventId.irrigation_start,
            log="Irrigation started",
        )
        log_to_add_2 = Log(
            zone_id=2,
            date_time=None,
            event_id=EventId.irrigation_stop,
            log="Irrigation ended",
        )
        sleep(1)
        log_to_add_3 = Log(
            zone_id=2,
            date_time=None,
            event_id=EventId.irrigation_start,
            log="Irrigation started",
        )
        log_to_add_4 = Log(
            zone_id=2,
            date_time=None,
            event_id=EventId.irrigation_stop,
            log="Irrigation ended",
        )

        PersistentLogDAO.add_log(log_to_add_1)
        PersistentLogDAO.add_log(log_to_add_2)
        PersistentLogDAO.add_log(log_to_add_3)
        PersistentLogDAO.add_log(log_to_add_4)

        logs = PersistentLogDAO.get_logs(2, number_of_logs_to_get=1)
        self.assertEqual(logs[0], log_to_add_4)
        self.assertEqual(len(logs), 1)
        logs = PersistentLogDAO.get_logs(2, EventId.irrigation_start)
        self.assertEqual(len(logs), 2)
        self.assertEqual(logs[0], log_to_add_3)
        self.assertEqual(logs[1], log_to_add_1)


if __name__ == "__main__":
    unittest.main()
