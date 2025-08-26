from backend.datatype.IrrigationInfo import IrrigationInfo
import datetime


class ZoneWeb:
    name = ""
    id = 0
    is_open = False
    is_override = False
    logs = ""
    last_irrigation_date = None
    irrigation_info = list()

    def __init__(self, name, id, is_open, is_override, irrigation_info, last_irrigation_date:str=None) -> None:
        self.name = name
        self.id = id
        self.is_open = is_open
        self.is_override = is_override
        self.irrigation_info = irrigation_info
        self.last_irrigation_date = last_irrigation_date

    def serialize(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "is_open": str(self.is_open),
            "is_override": str(self.is_override),
            "last_irrigation_date": str(self.last_irrigation_date),
            "irrigation_info": [s.serializes() for s in self.irrigation_info],
        }
