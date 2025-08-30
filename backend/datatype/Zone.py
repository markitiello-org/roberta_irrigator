"""Zone class for managing irrigation zones and their state."""

import datetime
import logging
import json
from backend.datatype.irrigation_info import IrrigationInfo
from backend.dao.persistent_log_dao import PersistentLogDAO
from backend.datatype.log import Log, EventId
from backend.hw_io.gpio import PiGpio

# pylint: disable=too-many-instance-attributes
class Zone:
    """Represents an irrigation zone with scheduling and control logic."""

    name = ""
    gpio_pin = 0
    irrigation_info = []
    id = 0
    _is_open = False
    last_irrigation_date = None
    _last_irrigation_date: datetime.time = None
    _is_override_open = False
    _is_override_close = False
    _how_many_second_can_i_stay_open = 120
    _logger = None
    _active_irrigation = None

    def __init__(
        self, name: str, gpio_pin: int, irrigation_info: list = None, zone_id: int = 0
    ):
        """Initialize a Zone instance."""
        self._logger = logging.getLogger()
        self.name = name
        self.gpio_pin = gpio_pin
        self.id = int(zone_id)
        if irrigation_info is None:
            self.irrigation_info = []
        else:
            self.irrigation_info = irrigation_info
        self.id = -1

    def _check_if_is_right_day_of_the_week_to_open(
        self, irrigation_info: IrrigationInfo, current_day_of_the_week
    ):
        """Check if today is a valid day for irrigation."""
        return current_day_of_the_week in irrigation_info.day_of_the_week

    def get_last_irrigation_date(self):
        """Get the last irrigation start date from logs."""
        logs = PersistentLogDAO.get_logs(
            self.id, EventId.irrigation_start, number_of_logs_to_get=1
        )
        if len(logs) != 0:
            return logs[0].date_time
        return None

    def print_zone(self):
        """Print zone information."""
        print(
            f"Id {self.id}, Name {self.name}, Gpio pin: {self.gpio_pin}, "
            f"IrrigatorInfo: {self.irrigation_info}"
        )

    def log_information(self, message, is_a_warning=False):
        """Log zone information or warning."""
        if is_a_warning:
            logging.warning("%s - %s", self.name, message)
        else:
            logging.info("%s - %s", self.name, message)

    def set_id(self, zone_id):
        """Set the zone ID."""
        self.id = int(zone_id)

    def is_open(self):
        """Return True if the zone is open."""
        return self._is_open

    def _open_it(self):
        """Open the zone and log the event."""
        self._is_open = True
        self.log_information(f"Open zone {self.name}")
        self._last_irrigation_date = datetime.datetime.now().time()
        PiGpio.instance().OpenPin(self.gpio_pin)
        PersistentLogDAO.add_log(
            Log(
                zone_id=self.id,
                date_time=datetime.datetime.now(),
                event_id=EventId.irrigation_start,
                log=f"Zone {self.name} opened",
            )
        )

    def _close_it(self):
        """Close the zone and log the event."""
        self._is_open = False
        self._is_override_open = False
        self._last_irrigation_date = None
        self.log_information(f"Close zone {self.name}")
        PiGpio.instance().ClosePin(self.gpio_pin)
        PersistentLogDAO.add_log(
            Log(
                zone_id=self.id,
                date_time=datetime.datetime.now(),
                event_id=EventId.irrigation_stop,
                log=f"Zone {self.name} closed",
            )
        )

    def override_open(self, is_override=True):
        """Override and open the zone, unless override close is active."""
        if self._is_override_close:
            self.log_information("Override Open: cannot open since override close!")
            return
        if is_override:
            self._open_it()
            self._is_override_open = True
        else:
            self._close_it()

    def is_override(self):
        """Return True if override open is active."""
        return self._is_override_open

    def override_close(self):
        """Override and close the zone."""
        self._close_it()
        self._is_open = False
        self._is_override_open = False
        self._last_irrigation_date = None
        self._is_override_close = True

    def check_if_need_to_open(self, current_time: datetime.time, current_day_of_the_week):
        """Check if the zone needs to be opened based on schedule."""
        if self._is_open:
            self.log_information("Already Open", True)
            return
        if self._is_override_close:
            self.log_information("Closed by override", True)
            return
        for irrigation in self.irrigation_info:
            if self._check_if_is_right_day_of_the_week_to_open(
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
                    self.log_information("Too Late to open")
                    return
                if current_time < time_to_open:
                    self.log_information("Too Early to open")
                    return
                if time_to_open < current_time < time_to_close:
                    self.log_information("Open command for timing", False)
                    self._open_it()
                    self._active_irrigation = irrigation

    def check_if_need_to_close(self, current_time):
        """Check if the zone needs to be closed based on schedule."""
        if not self._is_open:
            self.log_information("Already Closed", True)
            return
        if self._is_override_open:
            self.log_information("Override, not my responsibility to close it", True)
            return
        datetime_to_close = datetime.datetime.combine(
            datetime.date.today(), self._active_irrigation.time_to_start
        ) + datetime.timedelta(seconds=self._active_irrigation.for_how_many_seconds)
        time_to_close = datetime_to_close.time()
        if current_time > time_to_close:
            self.log_information("Closing for timing ", False)
            self._close_it()

    def check_emergency_closing(self, current_time):
        """Check if the zone needs to be closed due to emergency (open too long)."""
        if not self._is_open:
            self.log_information("Emergency closing, already closed")
            return
        open_time: datetime = None
        if self._is_override_open:
            open_time = self._last_irrigation_date
        else:
            open_time = self._active_irrigation.time_to_start
        if open_time is None:
            self._close_it()
            return
        current_datetime = datetime.datetime.combine(
            datetime.date.today(), current_time
        )
        last_opened_datetime = datetime.datetime.combine(
            datetime.date.today(), open_time
        )
        if current_datetime - last_opened_datetime > datetime.timedelta(
            seconds=self._how_many_second_can_i_stay_open
        ):
            self.log_information("Emergency closing, need to close!")
            self._close_it()
        else:
            self.log_information(
                "Emergency closing, number of seconds: %s",
                current_datetime - last_opened_datetime,
            )

    def to_json(self):
        """Return a JSON representation of the zone."""
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __eq__(self, other):
        """Compare two zones for equality."""
        if other is None or len(self.irrigation_info) != len(other.irrigation_info):
            return False
        return (
            self.id == int(other.id)
            and self.name == other.name
            and self.gpio_pin == other.gpio_pin
            and self.irrigation_info == other.irrigation_info
        )
