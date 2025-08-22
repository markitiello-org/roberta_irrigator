from backend.db.SqlLite import SqlLite
from backend.datatype.IrrigationInfo import IrrigationInfo  
import datetime

class IrrigationInfoDAO:
    @staticmethod
    def AddNewIrrigatorInfo(irrigation_info: IrrigationInfo, zone_id):
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
                """UPDATE scheduler SET zone_id = ?, sheduled_time = ?, for_how_many_seconds = ? WHERE id = ?""",
                [
                    zone_id,
                    irrigation_info.time_to_start.strftime("%H:%M:%S"),
                    irrigation_info.for_how_many_seconds,
                    irrigation_info.id,
                ],
            )

    @staticmethod
    def GetIrrigationInfo(id_irrigator):
        data = SqlLite.get_instance().ExecuteQuery(
            """SELECT * FROM scheduler WHERE zone_id = ?""", [id_irrigator]
        )
        if data != None:
            list_of_irrigation_info = list()
            for row in data:
                irrigation_info = IrrigationInfo(
                    datetime.datetime.strptime(row[2], "%H:%M:%S").time(), row[3]
                )
                irrigation_info.id = row[0]
                list_of_irrigation_info.append(irrigation_info)
            return list_of_irrigation_info
        else:
            return list()
        
    @staticmethod
    def RemoveIrrigatorInfo(id):
        SqlLite.get_instance().ExecuteQueryNoResult(
            """DELETE FROM scheduler WHERE id = ?""", [id]
        )
