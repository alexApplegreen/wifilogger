import psycopg2
import logging

class Database():

    def __init__(self, host, user, name):
        self._logger = logging.getLogger(__name__)
        self._name = name
        self._conn = self.connect(host, user, name)

    def connect(self, host, user, name):
        conn = psycopg2.connect(
            dbname=name,
            user=user,
            host=host,
            password=None
        )
        self._logger.info("Successfully connected to dabatase")
        return conn

    def save_measurement(self, down, up, ping):
        with self._conn.cursor() as cursor:
            try:
                down = float(down)
                up = float(up)
                ping = float(ping)
                sql = f"INSERT INTO logs(down, up, ping) VALUES({down}, {up}, {ping})"
                cursor.execute(sql)
                self._logger.info("Successfully saved measurement")
            except psycopg2.OperationalError:
                self._logger.error("Could not save measurement to Dabatase")
            except ValueError:
                self._logger.error("Could not convert datatypes of measured values")
