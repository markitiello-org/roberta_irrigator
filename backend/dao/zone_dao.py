"""
This module provides the ZoneDAO class for managing zone records in the database.
"""

from backend.datatype.zone import Zone
from backend.db.SqlLite import SqlLite
from backend.dao.irrigation_info_dao import IrrigationInfoDAO


class ZoneDAO:
    """
    Data Access Object for Zone operations.
    This class provides methods to interact with the Zone data in the database.
    """

    @staticmethod
    def remove_irrigators():
        """
        Remove all zone records from the database.
        """
        SqlLite.get_instance().ExecuteQueryNoResult(""" DELETE FROM zone """)

    @staticmethod
    def get_zone_by_id(zone_id=None):
        """
        Retrieve one or all zone records from the database.
        Args:
            zone_id (int, optional): The ID of the zone to retrieve. If None, retrieves all zones.
        Returns:
            Zone or list[Zone] or None: The zone(s) matching the query.
        """
        if zone_id is None:
            rows = SqlLite.get_instance().ExecuteQuery("""SELECT * FROM zone""")
            returned_zone = []
            for data in rows:
                print("got data: ", data)
                zone = Zone(
                    data[1], data[2], IrrigationInfoDAO.get_irrigation_info(data[0])
                )
                print("got zone: ", zone)
                zone.set_id(data[0])
                returned_zone.append(zone)
            return returned_zone
        data = SqlLite.get_instance().ExecuteQuery(
            """SELECT * FROM zone where id = ?""", [zone_id]
        )
        if data is not None:
            zone = Zone(
                data[0][1], data[0][2], IrrigationInfoDAO.get_irrigation_info(zone_id)
            )
            zone.set_id(data[0][0])
            return zone
        return None

    @staticmethod
    def add_new_irrigator(zone: Zone):
        """
        Add a new zone or update an existing zone in the database, and add related irrigation info.
        Args:
            zone (Zone): The zone object to add or update.
        """
        if zone.id == -1:
            num = SqlLite.get_instance().ExecuteQuery("""SELECT COUNT(*) FROM zone""")
            new_zone_id = int(num[0][0]) + 1
            zone.set_id(new_zone_id)
            SqlLite.get_instance().ExecuteQueryNoResult(
                """INSERT INTO zone VALUES (?, ?, ?, ?) """,
                [zone.id, zone.name, zone.gpio_pin, None],
            )
        else:
            SqlLite.get_instance().ExecuteQueryNoResult(
                """UPDATE zone SET name=?, gpio_pin=?, last_irrigation_time=? WHERE id = ?""",
                [zone.name, zone.gpio_pin, zone.last_irrigation_date, zone.id],
            )
        zone.print_zone()
        for irrigation_info_element in zone.irrigation_info:
            print(f"Adding irrigation info {irrigation_info_element} to zone {zone.id}")
            IrrigationInfoDAO.add_new_irrigator_info(irrigation_info_element, zone.id)
