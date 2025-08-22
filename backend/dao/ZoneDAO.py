import backend.datatype.Zone as Zone
from backend.db.SqlLite import SqlLite
from backend.datatype.IrrigationInfo import IrrigationInfo
from backend.datatype.Zone import Zone
from backend.dao.IrrigationInfoDAO import IrrigationInfoDAO

class ZoneDAO:
    """
    Data Access Object for Zone operations.
    This class provides methods to interact with the Zone data in the database.
    """

    @staticmethod
    def RemoveIrrigators():
        SqlLite.get_instance().ExecuteQueryNoResult(""" DELETE FROM zone """)

    @staticmethod
    def GetZoneById(id=None):
        if id == None:
            rows = SqlLite.get_instance().ExecuteQuery("""SELECT * FROM zone""")
            returned_zone = list()
            for data in rows:
                print("got data: ", data)
                zone = Zone(data[1], data[2], IrrigationInfoDAO.GetIrrigationInfo(data[0]))
                print("got zone: ", zone)
                zone.SetId(data[0])
                returned_zone.append(zone)
            return returned_zone
        else:
            data = SqlLite.get_instance().ExecuteQuery("""SELECT * FROM zone where id = ?""", [id])
            if data != None:
                zone = Zone(data[0][1], data[0][2], IrrigationInfoDAO.GetIrrigationInfo(id))
                zone.SetId(data[0][0])
                return zone
            else:
                return None
    
    @staticmethod
    def AddNewIrrigator(zone: Zone):
        if zone.id == -1:
            num = SqlLite.get_instance().ExecuteQuery(
                """SELECT COUNT(*) FROM zone"""
            )
            id = int(num[0][0]) + 1
            zone.SetId(id)
            SqlLite.get_instance().ExecuteQueryNoResult("""INSERT INTO zone VALUES (?, ?, ?, ?) """,
                [zone.id, zone.name, zone.gpio_pin, None])
        else:
            SqlLite.get_instance().ExecuteQueryNoResult("""UPDATE zone SET name=?, gpio_pin=?, last_irrigation_time=? WHERE id = ?""",
                [zone.name, zone.gpio_pin, zone.last_irrigation_date, zone.id])
        zone.Print()
        for irrigation_info_element in zone.irrigation_info:
            print(f"Adding irrigation info {irrigation_info_element} to zone {zone.id}")
            IrrigationInfoDAO.AddNewIrrigatorInfo(irrigation_info_element, zone.id)