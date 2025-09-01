import datetime
import unittest
from backend.db.SqlLite import SqlLite
from backend.datatype.irrigation_info import IrrigationInfo
from backend.dao.irrigation_info_dao import IrrigationInfoDAO


class TestIrrigationInfo(unittest.TestCase):
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

    def test_add_irrigator_info(self):
        print("==== test add irrigator info =====")
        irrigation_info_to_add_1 = IrrigationInfo(datetime.time(10, 20, 00, 00), 120)
        irrigation_info_to_add_2 = IrrigationInfo(datetime.time(15, 20, 00, 00), 120)
        irrigation_info_to_add_3 = IrrigationInfo(datetime.time(21, 20, 00, 00), 120)
        IrrigationInfoDAO.add_new_irrigator_info(irrigation_info_to_add_1, 1)
        IrrigationInfoDAO.add_new_irrigator_info(irrigation_info_to_add_2, 1)
        IrrigationInfoDAO.add_new_irrigator_info(irrigation_info_to_add_3, 1)
        irrigator_list = IrrigationInfoDAO.get_irrigation_info(1)
        self.assertEqual(len(irrigator_list), 3)
        self.assertEqual(irrigator_list[0], irrigation_info_to_add_1)
        self.assertEqual(irrigator_list[1], irrigation_info_to_add_2)
        self.assertEqual(irrigator_list[2], irrigation_info_to_add_3)
        self.assertNotEqual(irrigator_list, None)

    def test_edit_irrigator_info(self):
        print("==== test edit irrigator info =====")
        irrigation_info_to_add_1 = IrrigationInfo(datetime.time(10, 20, 00, 00), 120)
        irrigation_info_to_add_2 = IrrigationInfo(datetime.time(15, 20, 00, 00), 120)
        irrigation_info_to_add_3 = IrrigationInfo(datetime.time(21, 20, 00, 00), 120)
        IrrigationInfoDAO.add_new_irrigator_info(irrigation_info_to_add_1, 3)
        IrrigationInfoDAO.add_new_irrigator_info(irrigation_info_to_add_2, 3)
        IrrigationInfoDAO.add_new_irrigator_info(irrigation_info_to_add_3, 3)
        irrigator_list = IrrigationInfoDAO.get_irrigation_info(1)
        self.assertEqual(irrigator_list[0], irrigation_info_to_add_1)
        irrigation_info_to_add_1.for_how_many_seconds = 250
        IrrigationInfoDAO.add_new_irrigator_info(irrigation_info_to_add_1, 3)
        irrigator_list = IrrigationInfoDAO.get_irrigation_info(1)
        self.assertEqual(len(irrigator_list), 3)
        self.assertEqual(irrigator_list[0], irrigation_info_to_add_1)
        self.assertEqual(irrigator_list[1], irrigation_info_to_add_2)
        self.assertEqual(irrigator_list[2], irrigation_info_to_add_3)
        self.assertNotEqual(irrigator_list, None)

    def test_remove_irrigator_info(self):
        print("==== test remove irrigator info =====")
        irrigation_info_to_add_1 = IrrigationInfo(datetime.time(10, 20, 00, 00), 120)
        irrigation_info_to_add_2 = IrrigationInfo(datetime.time(15, 20, 00, 00), 120)
        irrigation_info_to_add_3 = IrrigationInfo(datetime.time(21, 20, 00, 00), 120)
        IrrigationInfoDAO.add_new_irrigator_info(irrigation_info_to_add_1, 4)
        IrrigationInfoDAO.add_new_irrigator_info(irrigation_info_to_add_2, 4)
        IrrigationInfoDAO.add_new_irrigator_info(irrigation_info_to_add_3, 4)
        irrigator_list = IrrigationInfoDAO.get_irrigation_info(1)
        self.assertEqual(len(irrigator_list), 3)
        IrrigationInfoDAO.remove_irrigator_info(irrigator_list[0].id)
        irrigator_list = IrrigationInfoDAO.get_irrigation_info(1)
        self.assertEqual(len(irrigator_list), 2)
        self.assertEqual(irrigator_list[0], irrigation_info_to_add_2)
        self.assertEqual(irrigator_list[1], irrigation_info_to_add_3)


if __name__ == "__main__":
    unittest.main()