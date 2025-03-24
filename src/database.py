import psycopg2
from logging import getLogger

class Database():

    def __init__(self, host, user, name):
        self._logger = getLogger(__name__)
        self._name = name
        self._conn = self.connect(host, user, name)

    def connect(self, host, user, name):
        try:
            conn = psycopg2.connect(
                dbname=name,
                user=user,
                host=host,
                password=None
            )
            self._logger.info("Successfully connected to dabatase")
            return conn
        except:
            self._logger.error("Could not connect to database")
            return None

    def save_measurement(self, down, up, ping):
        with self._conn.cursor as cursor:
            try:
                sql = f"INSERT INTO logs(down, up, ping) VALUES({down}, {up}, {ping})"
                cursor.execute(sql)
                self._logger.info("Successfully saved measurement")
            except psycopg2.OperationalError:
                print("Could not save measurement to Dabatase")
