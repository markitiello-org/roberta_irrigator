import datetime
from backend.db.SqlLite import SqlLite
from backend.datatype.log import EventId, Log


class PersistentLogDAO:
    @staticmethod
    def AddLog(log: Log):
        if log.event_id == EventId.general and log.log is None:
            raise Exception("Used a general event id but no text has been provided")
        log.date_time = datetime.datetime.now()
        SqlLite.get_instance().ExecuteQueryNoResult(
            """INSERT INTO log VALUES (?, ?, ?, ?)""",
            [
                log.zone_id,
                log.date_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
                int(log.event_id.value),
                log.log,
            ],
        )

    @staticmethod
    def GetLogs(
        zone_id: int = None, event_id: EventId = None, number_of_logs_to_get: int = None
    ):
        query = "SELECT * FROM log"
        params = []
        conditions = []

        if zone_id is not None:
            conditions.append("zone_id = ?")
            params.append(zone_id)
        if event_id is not None:
            conditions.append("event = ?")
            params.append(
                int(event_id.value) if hasattr(event_id, "value") else event_id
            )

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY date_time DESC"
        data = SqlLite.get_instance().ExecuteQuery(query, params)

        logs = []
        if number_of_logs_to_get is not None:
            data = data[:number_of_logs_to_get]
        for row in data:
            print(row[1])
            logs.append(
                Log(
                    row[0],
                    datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S.%f"),
                    EventId(row[2]),
                    row[3],
                )
            )
        return logs
