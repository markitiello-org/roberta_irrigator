from backend.datatype.IrrigationInfo import IrrigationInfo
import datetime
import logging
import json
from backend.dao.PersistentLogDAO import PersistentLogDAO
from backend.datatype.Log import Log, EventId
from backend.hw_io.gpio import PiGpio

class Zone:
    name = ""
    gpio_pin = 0
    irrigation_info = list()
    id = 0
    _is_open = False
    _last_irrigation_date: datetime.time = None
    _next_irrigation_date = None
    _is_override_open = False
    _is_override_close = False
    _how_many_second_can_i_stay_open = 120
    _logger = None
    _active_irrigation = None

    def __init__(self, name:str, gpio_pin:int, irrigation_info:list =None, id:int=0):
        self._logger = logging.getLogger()
        self.name = name
        self.gpio_pin = gpio_pin
        self.id = int(id)
        if irrigation_info == None:
            self.irrigation_info = list()
        else:
            self.irrigation_info = irrigation_info
        self.id = -1

    def _CheckIfIsRightDayOfTheWeekToOpen(
        self, irrigation_info:IrrigationInfo, current_day_of_the_week
    ):
        return current_day_of_the_week in irrigation_info.day_of_the_week

    def GetLastIrrigationDate(self):
        logs = PersistentLogDAO.GetLogs(self.id, EventId.irrigation_start, number_of_logs_to_get=1)
        if len(logs) != 0:
            return logs[0].date_time
        return None
    
    def Print(self):
        print(
            f"Id {self.id}, Name {self.name}, Gpio pin: {self.gpio_pin}, IrrigatorInfo: {self.irrigation_info} "
        )

    def LogInformation(self, message, is_a_warning=False):
        if is_a_warning:
            logging.warning(f"{self.name} - {message}")
        else:
            logging.info(f"{self.name} - {message}")

    def SetId(self, id):
        self.id = int(id)

    def IsOpen(self):
        return self._is_open

    def _OpenIt(self):
        self._is_open = True
        self.LogInformation(f"Open zone {self.name}")
        self._last_irrigation_date = datetime.datetime.now().time()
        PiGpio.instance().OpenPin(self.gpio_pin)
        PersistentLogDAO.AddLog(
            Log(
                zone_id=self.id,
                date_time=datetime.datetime.now(),
                event_id=EventId.irrigation_start,
                log=f"Zone {self.name} opened"
            )
        )

    def _CloseIt(self):
        self._is_open = False
        self._is_override_open = False
        self._last_irrigation_date = None
        self.LogInformation(f"Close zone {self.name}")
        PiGpio.instance().ClosePin(self.gpio_pin)
        PersistentLogDAO.AddLog(
            Log(
                zone_id=self.id,
                date_time=datetime.datetime.now(),
                event_id=EventId.irrigation_stop,
                log=f"Zone {self.name} closed"
            )
        )

    def OverrideOpen(self, is_ovverride=True):
        if self._is_override_close:
            self.LogInformation("Override Open: cannot open since override close!")
            return
        if is_ovverride:
            self._OpenIt()
            self._is_override_open = True
        else:
            self._CloseIt()

    def IsOverride(self):
        return self._is_override_open

    def OverrideClose(self):
        self._CloseIt()
        self._is_open = False
        self._is_override_open = False
        self._last_irrigation_date = None
        self._is_override_close = True

    def CheckIfNeedToOpen(self, current_time: datetime.time, current_day_of_the_week):
        if self._is_open:
            self.LogInformation("Already Open", True)
            return
        if self._is_override_close:
            self.LogInformation("Closed by override", True)
            return
        for irrigation in self.irrigation_info:
            if self._CheckIfIsRightDayOfTheWeekToOpen(
                irrigation, current_day_of_the_week
            ):
                datetime_to_open = datetime.datetime.combine(
                    datetime.date.today(), irrigation.time_to_start
                )
                time_to_close = (
                    datetime_to_open
                    + datetime.timedelta(seconds=irrigation.for_how_many_seconds)
                ).time()
                time_to_open = datetime_to_open.time()
                if current_time > time_to_close:
                    self.LogInformation("Too Late to open")
                    return
                if current_time < time_to_open:
                    self.LogInformation("Too Early to open")
                    return
                if current_time > time_to_open and current_time < time_to_close:
                    self.LogInformation("Open command for timing", False)
                    self._OpenIt()
                    self._active_irrigation = irrigation
    def CheckIfNeedToClose(self: datetime.time, current_time):
        if not self._is_open:
            self.LogInformation("Already Closed", True)
            return
        if self._is_override_open:
            self.LogInformation("Override, not my responsability to close it", True)
            return
        datetime_to_close = datetime.datetime.combine(
            datetime.date.today(), self._active_irrigation.time_to_start
        ) + datetime.timedelta(seconds=self._active_irrigation.for_how_many_seconds)
        time_to_close = datetime_to_close.time()
        if current_time > time_to_close:
            self.LogInformation("Closing for timing ", False)
            self._CloseIt()

    def CheckEmergencyClosing(self, current_time):
        if not self._is_open:
            self.LogInformation("Emerency closing, already closed")
            return
        open_time:datetime = None
        if self._is_override_open:
            open_time = self._last_irrigation_date
        else:
            open_time = self._active_irrigation.time_to_start
        if open_time == None:
            self._CloseIt()
            return
        current_datatime = datetime.datetime.combine(
            datetime.date.today(), current_time
        )
        last_opened_datatime = datetime.datetime.combine(
            datetime.date.today(), open_time
        )
        if current_datatime - last_opened_datatime > datetime.timedelta(
            seconds=self._how_many_second_can_i_stay_open
        ):
            self.LogInformation("Emergency closing, need to close!")
            self._CloseIt()
        else:
            self.LogInformation(
                f"Emergency closing, number of seconds: {current_datatime - last_opened_datatime} "
            )

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __eq__(self, other):
        if other == None or len(self.irrigation_info) != len(other.irrigation_info):
            return False
        return (
            self.id == int(other.id)
            and self.name == other.name
            and self.gpio_pin == other.gpio_pin
            and self.irrigation_info == other.irrigation_info
        )
