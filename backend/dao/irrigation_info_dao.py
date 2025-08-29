"""
This module provides the IrrigationInfoDAO class for managing irrigation
scheduling data in the database.
"""

from backend.db.SqlLite import SqlLite
from backend.datatype.irrigation_info import IrrigationInfo
import datetime


class IrrigationInfoDAO:
    """
    Data Access Object for irrigation scheduling information.
    Handles database operations for IrrigationInfo.
    """

    @staticmethod
    def add_new_irrigator_info(irrigation_info: IrrigationInfo, zone_id: int):
        """
        Adds a new irrigation info record to the database or updates an existing one.
        Args:
            irrigation_info (IrrigationInfo): The irrigation info to add or update.
            zone_id (int): The zone identifier for the irrigation info.
        """
        if irrigation_info.id == -1:
            num = SqlLite.get_instance().ExecuteQuery(
                """SELECT COUNT(*) FROM scheduler"""
            )
            id = int(num[0][0]) + 1
            SqlLite.get_instance().ExecuteQueryNoResult(
                """INSERT INTO scheduler VALUES (?, ?, ?, ?) """,
                [
                    id,
                    zone_id,
                    irrigation_info.time_to_start.strftime("%H:%M:%S"),
                    irrigation_info.for_how_many_seconds,
                ],
            )
            irrigation_info.id = id
        else:
            SqlLite.get_instance().ExecuteQueryNoResult(
                """UPDATE scheduler SET zone_id = ?, sheduled_time = ?, 
                        for_how_many_seconds = ? WHERE id = ?""",
                [
                    zone_id,
                    irrigation_info.time_to_start.strftime("%H:%M:%S"),
                    irrigation_info.for_how_many_seconds,
                    irrigation_info.id,
                ],
            )

    @staticmethod
    def get_irrigation_info(id_irrigator: int):
        """
        Retrieves irrigation info records for a given zone ID.
        Args:
            id_irrigator (int): The zone identifier to query.
        Returns:
            list[IrrigationInfo]: List of irrigation info objects for the zone.
        """
        data = SqlLite.get_instance().ExecuteQuery(
            """SELECT * FROM scheduler WHERE zone_id = ?""", [id_irrigator]
        )
        if data is not None:
            list_of_irrigation_info = list()
            for row in data:
                irrigation_info = IrrigationInfo(
                    datetime.datetime.strptime(row[2], "%H:%M:%S").time(), row[3]
                )
                irrigation_info.id = row[0]
                list_of_irrigation_info.append(irrigation_info)
            return list_of_irrigation_info
        return list()

    @staticmethod
    def remove_irrigator_info(id: int):
        """
        Removes an irrigation info record from the database by its ID.
        Args:
            id (int): The ID of the irrigation info to remove.
        """
        SqlLite.get_instance().ExecuteQueryNoResult(
            """DELETE FROM scheduler WHERE id = ?""", [id]
        )
