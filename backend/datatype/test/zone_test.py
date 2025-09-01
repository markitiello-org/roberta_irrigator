"""Unit tests for the Zone class."""

import unittest
import datetime

from backend.datatype.zone import Zone
from backend.datatype.irrigation_info import IrrigationInfo
from backend.db.SqlLite import SqlLite


class TestZone(unittest.TestCase):
    """Test cases for Zone behavior."""

    db = None

    @classmethod
    def setUpClass(cls):
        """Set up the database for IrrigationInfoDAO tests."""
        print("Setting up the database for IrrigationInfoDAO tests")
        cls.db = SqlLite.get_instance()
        cls.db.CreateDb()

    @classmethod
    def tearDownClass(cls):
        """Tear down the database after IrrigationInfoDAO tests."""
        print("Tearing down the database after IrrigationInfoDAO tests")
        cls.db.RemoveDb()

    def test_time_to_open_then_zone_is_open(self):
        """Test that the zone opens at the correct time."""
        irrigation_info = [
            IrrigationInfo(datetime.time(10, 20, 0, 0), 120),
            IrrigationInfo(datetime.time(22, 20, 0, 0), 120),
        ]
        zone = Zone("test", 1, irrigation_info)
        now = datetime.time(10, 19, 0, 0)
        zone.check_if_need_to_open(now, 3)
        self.assertEqual(zone.is_open(), False)
        now = datetime.time(10, 20, 1, 0)
        zone.check_if_need_to_open(now, 3)
        self.assertEqual(zone.is_open(), True)
        now = datetime.time(10, 21, 59, 0)
        self.assertEqual(zone.is_open(), True)
        print("Zone should be open now")

    def test_time_to_close_then_zone_is_closed(self):
        """Test that the zone closes at the correct time."""
        irrigation_info = [
            IrrigationInfo(datetime.time(10, 20, 0, 0), 120),
            IrrigationInfo(datetime.time(22, 20, 0, 0), 120),
        ]
        zone = Zone("test", 1, irrigation_info)
        now = datetime.time(10, 19, 0, 0)
        zone.check_if_need_to_open(now, 3)
        now = datetime.time(10, 20, 1, 0)
        zone.check_if_need_to_open(now, 3)
        now = datetime.time(10, 22, 1, 0)
        zone.check_if_need_to_close(now)
        self.assertEqual(zone.is_open(), False)

    def test_zone_opened_for_more_than_allowed_time_then_zone_is_closed(self):
        """Test that the zone closes if open for too long."""
        irrigation_info = [
            IrrigationInfo(datetime.time(10, 20, 0, 0), 120),
            IrrigationInfo(datetime.time(22, 20, 0, 0), 120),
        ]
        zone = Zone("test", 1, irrigation_info)
        now = datetime.time(10, 19, 0, 0)
        zone.override_open()
        self.assertEqual(zone.is_open(), True)
        now = datetime.datetime.now() + datetime.timedelta(minutes=1)
        zone.check_if_need_to_open(now.time(), 3)
        zone.check_if_need_to_close(now.time())
        self.assertEqual(zone.is_open(), True)
        now = now + datetime.timedelta(minutes=1, seconds=1)
        zone.check_emergency_closing(now.time())
        self.assertEqual(zone.is_open(), False)

    def test_try_to_open_zone_with_right_time_but_wrong_day_then_zone_is_closed(self):
        """Test that the zone does not open on the wrong day."""
        irrigation_info = [
            IrrigationInfo(datetime.time(10, 20, 0, 0), 120, [2, 3, 4, 5, 6]),
            IrrigationInfo(datetime.time(22, 20, 0, 0), 120, [2, 3, 4, 5, 6]),
        ]
        zone = Zone("test", 1, irrigation_info)
        now = datetime.time(10, 19, 0, 0)
        zone.check_if_need_to_open(now, 1)
        self.assertEqual(zone.is_open(), False)

    def test_open_in_override_then_stop_then_zone_is_closed(self):
        """Test override open then stop closes the zone."""
        irrigation_info = [
            IrrigationInfo(datetime.time(10, 20, 0, 0), 120, [2, 3, 4, 5, 6]),
            IrrigationInfo(datetime.time(22, 20, 0, 0), 120, [2, 3, 4, 5, 6]),
        ]
        zone = Zone("test", 1, irrigation_info)
        zone.override_open()
        self.assertEqual(zone.is_open(), True)

        zone.override_open(False)
        self.assertEqual(zone.is_open(), False)

    def test_override_close_and_right_time_then_zone_is_closed(self):
        """Test override close prevents opening at right time."""
        irrigation_info = [
            IrrigationInfo(datetime.time(10, 20, 0, 0), 120, [2, 3, 4, 5, 6]),
            IrrigationInfo(datetime.time(22, 20, 0, 0), 120, [2, 3, 4, 5, 6]),
        ]
        zone = Zone("test", 1, irrigation_info)
        zone.override_close()
        now = datetime.time(10, 20, 1, 0)
        zone.check_if_need_to_open(now, 2)
        self.assertEqual(zone.is_open(), False)

    def test_override_close_and_try_to_open_in_override_then_zone_is_closed(self):
        """Test override close prevents override open."""
        irrigation_info = [
            IrrigationInfo(datetime.time(10, 20, 0, 0), 120, [2, 3, 4, 5, 6]),
            IrrigationInfo(datetime.time(22, 20, 0, 0), 120, [2, 3, 4, 5, 6]),
        ]
        zone = Zone("test", 1, irrigation_info)
        zone.override_close()
        zone.override_open()
        self.assertEqual(zone.is_open(), False)


if __name__ == "__main__":
    unittest.main()
