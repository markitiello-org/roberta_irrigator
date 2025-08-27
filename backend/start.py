import datetime
import logging
import os
import sys
import time
from backend.datatype.Zone import Zone
from backend.datatype.irrigation_info import IrrigationInfo
from backend.db.SqlLite import SqlLite
from backend.hw_io.gpio import PiGpio
from backend.dao.ZoneDAO import ZoneDAO
import rpyc
from threading import Thread
import threading


class Executor:
    zone_list = []
    _current_day_of_the_week = 0
    _current_time = datetime.time()
    _sleep_milliseconds_time = 800
    _thread = None
    _stop_executor = False
    _db = None
    _instance = None
    _service_instance = None
    _last_run = None

    def LoadZone(self):
        return ZoneDAO.GetZoneById()

    def SetCurrentTimeInformation(self):
        now = datetime.datetime.now()
        self._current_day_of_the_week = now.weekday()
        self._current_time = now.time()

    def CheckIfHaveToOpenAnyZone(self):
        for zone in self.zone_list:
            zone.CheckIfNeedToOpen(self._current_time, self._current_day_of_the_week)

    def CheckIfHaveToCloseAnyZone(self):
        for zone in self.zone_list:
            zone.CheckIfNeedToClose(self._current_time)

    def CheckIfAZoneIsOpenForTooManyTime(self):
        for zone in self.zone_list:
            zone.CheckEmergencyClosing(self._current_time)

    def CloseAll(self):
        for zone in self.zone_list:
            zone.OverrideOpen(False)

    def Wait(self):
        time.sleep(self._sleep_milliseconds_time / 1000)

    def SetLastRun(self):
        self._last_run = datetime.datetime.now()

    def AmIRunning(self):
        print(self._last_run)
        print(datetime.datetime.now())
        print(
            (self._last_run - datetime.datetime.now())
            < datetime.timedelta(milliseconds=self._sleep_milliseconds_time)
        )
        return (datetime.datetime.now() - self._last_run) < datetime.timedelta(
            milliseconds=self._sleep_milliseconds_time
        )

    def SetServiceInstance(self, service):
        self._service_instance = service
        print("Service instance set")

    def Main(self):
        try:
            print("Setting up pins")
            output_pin = []
            print("Setting up pins")
            for zone in self.zone_list:
                output_pin.append(zone.gpio_pin)
            print("output_pin")
            PiGpio.instance().SetUp(output_pin)
            print("===================")
            print(self.zone_list)
            print("===================")
            while not self._stop_executor:
                print("Runner....")
                self.SetCurrentTimeInformation()
                self.CheckIfHaveToOpenAnyZone()
                self.CheckIfHaveToCloseAnyZone()
                self.CheckIfAZoneIsOpenForTooManyTime()
                self.SetLastRun()
                self.Wait()
        except Exception as ex:
            self.LogInformation(f"Critical error in main loop: {ex}", is_error=True)
            logging.error(f"Main loop error: {ex}")
            logging.critical("Hardware or database failure - forcing shutdown")
            print(f"Critical error in main loop: {ex}")
            self.CloseAll()
            if self._db:
                self._db.CloseConnection()
            os._exit(1)
        finally:
            self.CloseAll()
            if self._db:
                self._db.CloseConnection()
            self.Stop()

    def LogInformation(self, message, is_error=False):
        if is_error:
            logging.error(f"Executor - {message}")
        else:
            logging.info(f"Executor - {message}")

    def Stop(self):
        self._stop_executor = True
        self.LogInformation("Stopping executor")
        print("Stopping")

    def Start(self):
        if self._thread is not None and self._thread.is_alive():
            self.LogInformation("Executor already running", is_error=True)
            return
        self._stop_executor = False
        self._thread = Thread(target=self.Main, daemon=True)
        self._thread.start()

    def WaitForShutdown(self, timeout=30):
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout)
            if self._thread.is_alive():
                self.LogInformation(
                    "Thread did not shut down gracefully", is_error=True
                )

    def GetIrrigators(self):
        return self.zone_list

    def __init__(self):
        raise RuntimeError("Call instance() instead")

    @classmethod
    def instance(self):
        if self._instance is None:
            print("Executor - Creating new instance")
            self._instance = self.__new__(self)
        return self._instance


class RpcService(rpyc.Service):
    executor = None

    def StartUp(self):
        print("Starting up the service...")
        self._db = SqlLite.get_instance()
        print("Database instance obtained")
        db_exists = self._db.DbExists()
        print(f"Database exists: {db_exists}")
        if not db_exists:
            print("Create db")
            self._db.CreateDb()
            zone_to_add_1 = Zone("Zona 1 ", 37)
            zone_to_add_2 = Zone("Zona 2 ", 38)
            zone_to_add_3 = Zone("Zona 3 ", 40)
            irrigation_info_to_add_1 = IrrigationInfo(
                datetime.time(00, 00, 00, 00), 120
            )
            irrigation_info_to_add_2 = IrrigationInfo(datetime.time(5, 00, 00, 00), 120)
            irrigation_info_to_add_3 = IrrigationInfo(
                datetime.time(13, 00, 00, 00), 120
            )
            zone_to_add_1.irrigation_info.append(irrigation_info_to_add_1)
            zone_to_add_1.irrigation_info.append(irrigation_info_to_add_2)
            zone_to_add_1.irrigation_info.append(irrigation_info_to_add_3)
            irrigation_info_to_add_1_zone_2 = IrrigationInfo(
                datetime.time(00, 2, 30, 00), 120
            )
            irrigation_info_to_add_2_zone_2 = IrrigationInfo(
                datetime.time(5, 2, 30, 00), 120
            )
            irrigation_info_to_add_3_zone_2 = IrrigationInfo(
                datetime.time(13, 2, 30, 00), 120
            )
            zone_to_add_2.irrigation_info.append(irrigation_info_to_add_1_zone_2)
            zone_to_add_2.irrigation_info.append(irrigation_info_to_add_2_zone_2)
            zone_to_add_2.irrigation_info.append(irrigation_info_to_add_3_zone_2)
            irrigation_info_to_add_1_zone_3 = IrrigationInfo(
                datetime.time(00, 4, 30, 00), 120
            )
            irrigation_info_to_add_2_zone_3 = IrrigationInfo(
                datetime.time(5, 4, 30, 00), 120
            )
            zone_to_add_3.irrigation_info.append(irrigation_info_to_add_1_zone_3)
            zone_to_add_3.irrigation_info.append(irrigation_info_to_add_2_zone_3)
            ZoneDAO.AddNewIrrigator(zone_to_add_1)
            ZoneDAO.AddNewIrrigator(zone_to_add_2)
            ZoneDAO.AddNewIrrigator(zone_to_add_3)

    def exposed_start(self):
        if self._executor.AmIRunning():
            logging.info("Executor already running")
            return
        try:
            self._executor.Start()
            logging.info("Executor started via RPC")
        except Exception as ex:
            logging.error(f"Error starting executor via RPC: {ex}")
            print(f"Error starting executor: {ex}")
            # Force immediate termination on startup failure
            os._exit(1)

    def exposed_stop(self):
        logging.info("Stop requested via RPC")
        self._executor.Stop()
        self._executor.WaitForShutdown()

    def exposed_AmIRunning(self):
        return self._executor.AmIRunning()

    def exposed_GetIrrigators(self):
        print(self._executor.zone_list)
        return self._executor.zone_list

    def exposed_OpenZone(self, id: int):
        thread_id = threading.get_ident()
        print(f"Thread ID: {thread_id}")
        zone = next((x for x in self._executor.zone_list if x.id == id), None)
        zone.OverrideOpen(True)

    def exposed_CloseZone(self, id):
        zone = next((x for x in self._executor.zone_list if x.id == id), None)
        zone.OverrideOpen(False)

    def exposed_GetZoneInfo(self, id):
        return self._executor.zone_list[id]

    def __init__(self):
        self._executor = Executor.instance()
        try:
            self.StartUp()
            self._executor.zone_list = self._executor.LoadZone()
            self._executor.Start()
            print("Executor started")
            logging.info("Executor started successfully")
        except Exception as ex:
            logging.error(f"Error starting executor: {ex}")
            print(f"Error starting executor: {ex}")
            # Force immediate termination on startup failure
            os._exit(1)


if __name__ == "__main__":
    service = None
    server = None
    try:
        logging.basicConfig(
            format="%(asctime)s %(levelname)-8s %(message)s",
            filename="markitiello_irrigator.log",
            encoding="utf-8",
            level=logging.DEBUG,
        )

        logging.info("Starting Roberta Irrigator service...")
        service = RpcService()

        from rpyc.utils.server import ThreadedServer

        server = ThreadedServer(
            service,
            port=18871,
            protocol_config={"allow_public_attrs": True, "allow_pickle": True},
        )

        logging.info("RPC Server starting on port 18871")
        server.start()

    except KeyboardInterrupt:
        logging.info("Received shutdown signal")
    except Exception as ex:
        logging.error(f"Critical server error: {ex}")
        print(f"Critical error: {ex}")
    finally:
        logging.info("Shutting down service...")
        if service:
            try:
                service.exposed_stop()
            except Exception as cleanup_ex:
                logging.error(f"Error during service cleanup: {cleanup_ex}")
        if server:
            try:
                server.close()
            except Exception as cleanup_ex:
                logging.error(f"Error during server cleanup: {cleanup_ex}")
        logging.info("Service shutdown complete")
        sys.exit(0)
