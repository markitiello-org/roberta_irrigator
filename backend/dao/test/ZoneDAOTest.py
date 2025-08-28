import datetime
import unittest
from backend.db.SqlLite import SqlLite
from backend.datatype.Zone import Zone
from backend.datatype.irrigation_info import IrrigationInfo
from backend.dao.ZoneDAO import ZoneDAO


class TestZoneDAO(unittest.TestCase):
    db = None

    @classmethod
    def setUpClass(self):
        print("Setting up the database for IrrigationInfoDAO tests")
        self.db = SqlLite.get_instance()
        self.db.CreateDb()

    @classmethod
    def tearDownClass(self):
        print("Tearing down the database after IrrigationInfoDAO tests")
        self.db.RemoveDb()

    def test_add_zone(self):
        print("==== test add zone =====")
        zone_to_add = Zone("test", 1)
        ZoneDAO.AddNewIrrigator(zone_to_add)
        irrigator = ZoneDAO.GetZoneById(zone_to_add.id)
        self.assertEqual(irrigator, zone_to_add)

    def test_add_zone_with_irrigation_info(self):
        print("==== test add zone =====")
        zone_to_add = Zone("test", 2)
        irrigation_info_to_add = IrrigationInfo(datetime.time(10, 20, 00, 00), 120)
        zone_to_add.irrigation_info.append(irrigation_info_to_add)
        ZoneDAO.AddNewIrrigator(zone_to_add)
        zone = ZoneDAO.GetZoneById(zone_to_add.id)
        self.assertNotEqual(len(zone.irrigation_info), 0)
        self.assertEqual(zone, zone_to_add)

    def test_add_zone_with_more_than_one_irrigation_info(self):
        print("==== test add zone with multiple irrigation info =====")
        zone_to_add = Zone("test3", 3)
        irrigation_info_to_add_1 = IrrigationInfo(datetime.time(10, 20, 00, 00), 120)
        irrigation_info_to_add_2 = IrrigationInfo(datetime.time(15, 20, 00, 00), 120)
        irrigation_info_to_add_3 = IrrigationInfo(datetime.time(21, 20, 00, 00), 120)
        zone_to_add.irrigation_info.append(irrigation_info_to_add_1)
        zone_to_add.irrigation_info.append(irrigation_info_to_add_2)
        zone_to_add.irrigation_info.append(irrigation_info_to_add_3)
        ZoneDAO.AddNewIrrigator(zone_to_add)
        irrigator = ZoneDAO.GetZoneById(zone_to_add.id)
        self.assertEqual(len(irrigator.irrigation_info), 3)
        self.assertEqual(irrigator.irrigation_info[0], irrigation_info_to_add_1)
        self.assertEqual(irrigator.irrigation_info[1], irrigation_info_to_add_2)
        self.assertEqual(irrigator.irrigation_info[2], irrigation_info_to_add_3)

    def test_edit_zone(self):
        print("==== test edit zone =====")
        zone_to_add = Zone("test4", 4)
        irrigation_info_to_add = IrrigationInfo(datetime.time(10, 20, 00, 00), 120)
        zone_to_add.irrigation_info.append(irrigation_info_to_add)
        ZoneDAO.AddNewIrrigator(zone_to_add)
        zone_to_add.name = "updated_test"
        zone_to_add.gpio_pin = 5
        zone_to_add.irrigation_info[0].for_how_many_seconds = 150
        zone_to_add.irrigation_info[0].time_to_start = datetime.time(11, 30, 00, 00)
        zone_to_add.last_irrigation_date = datetime.datetime.now()
        ZoneDAO.AddNewIrrigator(zone_to_add)
        irrigator = ZoneDAO.GetZoneById(zone_to_add.id)
        self.assertEqual(irrigator.name, "updated_test")
        self.assertEqual(irrigator.gpio_pin, 5)
        self.assertEqual(len(irrigator.irrigation_info), 1)
        self.assertEqual(irrigator.irrigation_info[0].for_how_many_seconds, 150)
        self.assertEqual(
            irrigator.irrigation_info[0].time_to_start, datetime.time(11, 30, 00, 00)
        )


if __name__ == "__main__":
    unittest.main()
