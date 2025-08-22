import datetime


class IrrigationInfo:
    time_to_start = datetime.time()
    for_how_many_seconds = 0
    day_of_the_week = [0, 1, 2, 3, 4, 5, 6]
    id = -1

    def __init__(
        self,
        time_to_start: datetime.time,
        for_how_many_seconds: int,
        day_of_the_week=[0, 1, 2, 3, 4, 5, 6],
    ):
        self.time_to_start = time_to_start
        self.for_how_many_seconds = for_how_many_seconds
        self.day_of_the_week = day_of_the_week
        self.id = -1

    def serializes(self):
        return {
            "id": str(self.id),
            "time_to_start": self.time_to_start.strftime("%H:%M:%S"),
            "day_of_the_week": list(self.day_of_the_week),
            "for_how_many_seconds": int(self.for_how_many_seconds),
        }

    def __eq__(self, other):
        return (
            (other == None)
            or self.time_to_start == other.time_to_start
            and self.day_of_the_week == other.day_of_the_week
        )
