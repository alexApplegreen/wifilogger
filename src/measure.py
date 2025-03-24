import speedtest
import os
import sys

from dotenv import load_dotenv
from logging import getLogger

from database import Database

class Measure():

    def __init__(self):
        load_dotenv()

        self._logger = getLogger(__name__)
        self._threads = None
        self._servers = []
        self._database = self.init_db()
        try:
            self._sleep_cycle = int(os.environ.get("SLEEP_CYCLE", 10))
        except ValueError:
            self._sleep_cycle = 10

        self._logger.info(f"Measureing with cycle of {self._sleep_cycle} seconds")


    def init_db(self):
        db_host = os.environ.get("DB_HOST", "")
        db_name = os.environ.get("DB_NAME", "")
        db_user = os.environ.get("DB_USER", "")

        try:
            database = Database(
                db_host,
                db_user,
                db_name
            )
            return database
        except:
            sys.exit(-1)

    def measure(self) -> dict:
        s = speedtest.Speedtest()
        s.get_servers()
        s.get_best_server()
        s.download(threads=self._threads)
        s.upload(threads=self._threads)

        return s.results.dict()

    def parse(self, data: dict):
        download = data["download"]
        upload = data["upload"]
        ping = data["ping"]

        return download, upload, ping

    def save(self, data: dict) -> None:
        down, up, ping = self.parse(data)
        self._database.save_measurement(down, up, ping)

    def log(self, data: dict) -> None:
        self._logger.info("Measurement: Downlink: {down} Mbit/s, Uplink: {up} Mbit/s")

    @property
    def sleep_cycle(self):
        return self.sleep_cycle

    @sleep_cycle.setter
    def sleep_cycle(self, val):
        self._sleep_cycle = val
