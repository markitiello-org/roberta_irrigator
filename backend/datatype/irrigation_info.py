"""
This module defines the IrrigationInfo class for representing irrigation scheduling data.
"""

import datetime
from typing import List


class IrrigationInfo:
    """
    Represents irrigation scheduling information, including start time, duration,
    days of the week, and an identifier.
    """

    time_to_start = datetime.time()
    for_how_many_seconds = 0
    day_of_the_week = [0, 1, 2, 3, 4, 5, 6]
    id = -1

    def __init__(
        self,
        time_to_start: datetime.time,
        for_how_many_seconds: int,
        day_of_the_week: List[int] = None,
    ):
        if day_of_the_week is None:
            day_of_the_week = [0, 1, 2, 3, 4, 5, 6]
        self.time_to_start = time_to_start
        self.for_how_many_seconds = for_how_many_seconds
        self.day_of_the_week = day_of_the_week
        self.id = -1

    def serializes(self):
        """
        Serializes the irrigation info into a dictionary format for easy export or logging.
        """
        return {
            "id": str(self.id),
            "time_to_start": self.time_to_start.strftime("%H:%M:%S"),
            "day_of_the_week": list(self.day_of_the_week),
            "for_how_many_seconds": int(self.for_how_many_seconds),
        }

    def __eq__(self, other):
        return (
            (other is None)
            or self.time_to_start == other.time_to_start
            and self.day_of_the_week == other.day_of_the_week
        )
