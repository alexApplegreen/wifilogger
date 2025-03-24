import time
import logging

from measure import Measure


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger(__name__)

    measure = Measure()

    while(True):
        data = measure.measure()
        measure.log(data)
        measure.save(data)
        time.sleep(measure.sleep_cycle)
