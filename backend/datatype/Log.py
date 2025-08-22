import datetime

from enum import Enum



class EventId(Enum):
    irrigation_start = 0
    irrigation_stop = 1
    log_in = 2
    log_out = 3
    general = 4

class Log:
    date_time = datetime.datetime.now()
    event_id : EventId = EventId.general
    zone_id: int = None
    log = ""


    def __init__(self, zone_id, date_time, event_id, log) -> None:
        self.zone_id = zone_id
        self.date_time = date_time
        self.log = log
        self.event_id = event_id

    def __eq__(self, other):
        if other is None:
            return False
        return (
            self.zone_id == other.zone_id
            and self.date_time == other.date_time
            and self.event_id == other.event_id
            and self.log == other.log
        )

    def serialize(self):
        return {"date_time": self.date_time, "event": str(self.event_id), "log": self.log}

