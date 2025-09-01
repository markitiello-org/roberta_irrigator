"""Module for log data structures and event identifiers."""

import datetime
from enum import Enum


class EventId(Enum):
    """Enumeration of possible event types for logging."""

    IRRIGATION_START = 1
    IRRIGATION_STOP = 2
    LOG_IN = 3
    LOG_OUT = 4
    GENERAL = 5


class Log:
    """Represents a log entry for irrigation events."""

    zone_id: int
    date_time: datetime.datetime
    event_id: EventId
    log: str

    def __init__(
        self, zone_id: int, date_time: datetime.datetime, event_id: EventId, log: str
    ) -> None:
        """Initialize a Log entry."""
        self.zone_id = zone_id
        self.date_time = date_time
        self.event_id = event_id
        self.log = log

    def __eq__(self, other: object) -> bool:
        """Check equality between two Log entries."""
        if not isinstance(other, Log):
            return False
        return (
            self.zone_id == other.zone_id
            and self.date_time == other.date_time
            and self.event_id == other.event_id
            and self.log == other.log
        )

    def serialize(self) -> dict:
        """Serialize the log entry to a dictionary."""
        return {
            "date_time": self.date_time,
            "event": str(self.event_id),
            "log": self.log,
        }
