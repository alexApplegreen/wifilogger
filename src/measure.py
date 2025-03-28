import speedtest
import os
import sys
import logging

from dotenv import load_dotenv

from database import Database

class Measure():

    def __init__(self):
        load_dotenv()

        self._logger = logging.getLogger(__name__)
        self._threads = None
        self._servers = []
        self._database = self.init_db()
        try:
            self._sleep_cycle = int(os.environ.get("SLEEP_CYCLE", 10))
        except ValueError:
            self._sleep_cycle = 10 * 60  # 10 minutes

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
        except Exception:
            self._logger.error("Could not connect to database")
            sys.exit(-1)

    def measure(self) -> dict:
        s = speedtest.Speedtest(secure=True)
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
        down, up, ping = self.parse(data)
        self._logger.info(f"Measurement: Downlink: {down} bit/s, Uplink: {up} bit/s")

    @property
    def sleep_cycle(self):
        return self._sleep_cycle

    @sleep_cycle.setter
    def sleep_cycle(self, val):
        self._sleep_cycle = val
