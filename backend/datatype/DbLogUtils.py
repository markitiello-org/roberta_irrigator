from backend.datatype.Log import EventId
class DbLogUtils:
    _logger = None
    def __init__(self, logger):
        self._logger = logger
    def LogOpenZone(self, zone):
        self._logger.AddLog(zone.id, EventId.irrigation_start, f"Zone {zone.name} opened")
    def LogCloseZone(self, zone):
        self._logger.AddLog(zone.id, EventId.irrigation_stop, f"Zone {zone.name} closed")
    def LogGeneral(self, zone, message):
        self._logger.AddLog(zone.id, EventId.general, message)     