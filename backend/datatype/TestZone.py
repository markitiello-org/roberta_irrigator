import unittest
import sys
import datetime

from backend.datatype.Zone import Zone
from backend.datatype.IrrigationInfo import IrrigationInfo
from backend.db.SqlLite import SqlLite

class TestInitSqlLite(unittest.TestCase):

    db = None

    @classmethod
    def setUpClass(self):
        print("Setting up the database for IrrigationInfoDAO tests")
        self.db = SqlLite.get_instance()
        self.db.Init()
        self.db.CreateDb()

    @classmethod
    def tearDownClass(self):
        print("Tearing down the database after IrrigationInfoDAO tests")
        self.db.RemoveDb()

    def test_TimeToOpen_ThenZoneIsOpen(self):
        print("==== test TimeToOpen_ThenZoneIsOpen =====")
        irrigation_info = [IrrigationInfo(datetime.time(10,20,00,00), 120), IrrigationInfo(datetime.time(22,20,00,00), 120)]
        zone = Zone("test",1,irrigation_info)
        now = datetime.time(10, 19,00,00 )
        zone.CheckIfNeedToOpen(now, 3)
        self.assertEqual(zone.IsOpen(), False)
        now = datetime.time(10, 20,1,00 )
        zone.CheckIfNeedToOpen(now, 3)
        self.assertEqual(zone.IsOpen(), True)
        now = datetime.time(10, 21,59,00 )
        self.assertEqual(zone.IsOpen(), True)
        print("Zone should be open now")

    def test_TimeToClose_ThenZoneIsClosed(self):
        irrigation_info = [IrrigationInfo(datetime.time(10,20,00,00), 120), IrrigationInfo(datetime.time(22,20,00,00), 120)]
        zone = Zone("test",1,irrigation_info)
        now = datetime.time(10, 19,00,00 )
        zone.CheckIfNeedToOpen(now, 3)
        now = datetime.time(10, 20,1,00 )
        zone.CheckIfNeedToOpen(now, 3)
        now = datetime.time(10,22,1,00)
        zone.CheckIfNeedToClose(now)
        self.assertEqual(zone.IsOpen(),False)

    def test_ZoneOpenedForMoreThanAllowedTime_ThenZoneIsClosed(self):
        irrigation_info = [IrrigationInfo(datetime.time(10,20,00,00), 120), IrrigationInfo(datetime.time(22,20,00,00), 120)]
        zone = Zone("test",1,irrigation_info)
        now = datetime.time(10, 19,00,00 )
        zone.OverrideOpen()
        self.assertEqual(zone.IsOpen(),True)
        now = datetime.datetime.now() + datetime.timedelta(minutes=1)
        zone.CheckIfNeedToOpen(now.time(), 3)
        zone.CheckIfNeedToClose(now.time())
        self.assertEqual(zone.IsOpen(),True)
        now = now + datetime.timedelta(minutes=1,seconds=1)
        zone.CheckEmergencyClosing(now.time())
        self.assertEqual(zone.IsOpen(),False)

    def test_TryToOpenAZoneWithTheRigtTimeButNotRightDayOfTheWeek_ThenZoneIsClosed(self):
        irrigation_info = [IrrigationInfo(datetime.time(10,20,00,00), 120, [2,3,4,5,6]), IrrigationInfo(datetime.time(22,20,00,00), 120, [2,3,4,5,6])]
        zone = Zone("test",1,irrigation_info)
        now = datetime.time(10, 19,00,00 )
        zone.CheckIfNeedToOpen(now, 1)
        self.assertEqual(zone.IsOpen(),False)
 
    def test_OpenInOverrideThanStop_ThanZoneIsClosed(self):
        irrigation_info = [IrrigationInfo(datetime.time(10,20,00,00), 120, [2,3,4,5,6]), IrrigationInfo(datetime.time(22,20,00,00), 120, [2,3,4,5,6])]
        zone = Zone("test",1,irrigation_info)
        zone.OverrideOpen()
        self.assertEqual(zone.IsOpen(),True)

        zone.OverrideOpen(False)
        self.assertEqual(zone.IsOpen(), False) 

    def test_OverrideCloseAndRightTime_ThanZoneIsClosed(self):
        irrigation_info = [IrrigationInfo(datetime.time(10,20,00,00), 120, [2,3,4,5,6]), IrrigationInfo(datetime.time(22,20,00,00), 120, [2,3,4,5,6])]
        zone = Zone("test",1,irrigation_info)
        zone.OverrideClose()
        now = datetime.time(10, 20,1,00 )
        zone.CheckIfNeedToOpen(now, 2)
        self.assertEqual(zone.IsOpen(),False)

    def test_OverrideCloseAndTryToOpenInOverride_ThanZoneIsClosed(self):
        irrigation_info = [IrrigationInfo(datetime.time(10,20,00,00), 120, [2,3,4,5,6]), IrrigationInfo(datetime.time(22,20,00,00), 120, [2,3,4,5,6])]
        zone = Zone("test",1,irrigation_info)
        zone.OverrideClose()
        zone.OverrideOpen()
        self.assertEqual(zone.IsOpen(),False)


if __name__ == '__main__':
    unittest.main()