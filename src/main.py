import time

from measure import Measure


if __name__ == "__main__":
    measure = Measure()

    while(True):
        data = measure.measure()
        measure.save(data)
        measure.log(data)
        time.sleep(measure.sleep_cycle)
