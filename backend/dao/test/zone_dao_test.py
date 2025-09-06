"""
Unit tests for ZoneDAO: verifies adding, editing,
and retrieving zone records and their irrigation info.
"""

import datetime
import unittest
from backend.db.SqlLite import SqlLite
from backend.datatype.zone import Zone
from backend.datatype.irrigation_info import IrrigationInfo
from backend.dao.zone_dao import ZoneDAO


class TestZoneDAO(unittest.TestCase):
    """
    Test suite for ZoneDAO database operations.
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

    def test_add_zone(self):
        """
        Test adding a zone and retrieving it from the database.
        """
        print("==== test add zone =====")
        zone_to_add = Zone("test", 1)
        ZoneDAO.add_new_irrigator(zone_to_add)
        irrigator = ZoneDAO.get_zone_by_id(zone_to_add.id)
        self.assertEqual(irrigator, zone_to_add)

    def test_add_zone_with_irrigation_info(self):
        """
        Test adding a zone with irrigation info and verifying retrieval.
        """
        print("==== test add zone =====")
        zone_to_add = Zone("test", 2)
        irrigation_info_to_add = IrrigationInfo(datetime.time(10, 20, 00, 00), 120)
        zone_to_add.irrigation_info.append(irrigation_info_to_add)
        ZoneDAO.add_new_irrigator(zone_to_add)
        zone = ZoneDAO.get_zone_by_id(zone_to_add.id)
        self.assertNotEqual(len(zone.irrigation_info), 0)
        self.assertEqual(zone, zone_to_add)

    def test_add_zone_with_more_than_one_irrigation_info(self):
        """
        Test adding a zone with multiple irrigation info entries and 
        verifying retrieval.
        """
        print("==== test add zone with multiple irrigation info =====")
        zone_to_add = Zone("test3", 3)
        irrigation_info_to_add_1 = IrrigationInfo(datetime.time(10, 20, 00, 00), 120)
        irrigation_info_to_add_2 = IrrigationInfo(datetime.time(15, 20, 00, 00), 120)
        irrigation_info_to_add_3 = IrrigationInfo(datetime.time(21, 20, 00, 00), 120)
        zone_to_add.irrigation_info.append(irrigation_info_to_add_1)
        zone_to_add.irrigation_info.append(irrigation_info_to_add_2)
        zone_to_add.irrigation_info.append(irrigation_info_to_add_3)
        ZoneDAO.add_new_irrigator(zone_to_add)
        irrigator = ZoneDAO.get_zone_by_id(zone_to_add.id)
        self.assertEqual(len(irrigator.irrigation_info), 3)
        self.assertEqual(irrigator.irrigation_info[0], irrigation_info_to_add_1)
        self.assertEqual(irrigator.irrigation_info[1], irrigation_info_to_add_2)
        self.assertEqual(irrigator.irrigation_info[2], irrigation_info_to_add_3)

    def test_edit_zone(self):
        """
        Test editing a zone and its irrigation info, then verifying the updates.
        """
        print("==== test edit zone =====")
        zone_to_add = Zone("test4", 4)
        irrigation_info_to_add = IrrigationInfo(datetime.time(10, 20, 00, 00), 120)
        zone_to_add.irrigation_info.append(irrigation_info_to_add)
        ZoneDAO.add_new_irrigator(zone_to_add)
        zone_to_add.name = "updated_test"
        zone_to_add.gpio_pin = 5
        zone_to_add.irrigation_info[0].for_how_many_seconds = 150
        zone_to_add.irrigation_info[0].time_to_start = datetime.time(11, 30, 00, 00)
        zone_to_add.last_irrigation_date = datetime.datetime.now()
        ZoneDAO.add_new_irrigator(zone_to_add)
        irrigator = ZoneDAO.get_zone_by_id(zone_to_add.id)
        self.assertEqual(irrigator.name, "updated_test")
        self.assertEqual(irrigator.gpio_pin, 5)
        self.assertEqual(len(irrigator.irrigation_info), 1)
        self.assertEqual(irrigator.irrigation_info[0].for_how_many_seconds, 150)
        self.assertEqual(
            irrigator.irrigation_info[0].time_to_start, datetime.time(11, 30, 00, 00)
        )

    def test_get_all_zones(self):
        """
        Test retrieving all zones from the database.
        """
        print("==== test get all zones =====")
        ZoneDAO.remove_irrigators()
        zones = ZoneDAO.get_zone_by_id()
        self.assertGreaterEqual(len(zones), 0)
        zone_to_add = Zone("test5", 4)
        irrigation_info_to_add = IrrigationInfo(datetime.time(10, 20, 00, 00), 120)
        zone_to_add.irrigation_info.append(irrigation_info_to_add)
        zone_to_add_2 = Zone("test5", 4)
        irrigation_info_to_add_2 = IrrigationInfo(datetime.time(10, 20, 00, 00), 120)
        zone_to_add_2.irrigation_info.append(irrigation_info_to_add_2)
        ZoneDAO.add_new_irrigator(zone_to_add_2)
        ZoneDAO.add_new_irrigator(zone_to_add)
        zones = ZoneDAO.get_zone_by_id()
        self.assertEqual(len(zones), 2)


if __name__ == "__main__":
    unittest.main()
