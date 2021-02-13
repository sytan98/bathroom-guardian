# Logs the past few accel values to a file called 'accel.log'

import logging
from logging.handlers import RotatingFileHandler
import datetime
import time
import board
import busio
import adafruit_lsm303_accel
import numpy as np

i2c = busio.I2C(board.SCL, board.SDA)
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)
accel.range = adafruit_lsm303_accel.Range.RANGE_8G

def create_rotating_log(path):
    # Creates a rotating log to log items
    handler = RotatingFileHandler(path, maxBytes=65536, backupCount=1)
    handler.setLevel(logging.INFO)
    return handler

if __name__ == "__main__":
    rot_handler = create_rotating_log("accel.log")
    logger = logging.getLogger("Rotating Log")
    logger.addHandler(rot_handler)
    logger.setLevel(logging.INFO)

    while True:
        now = datetime.datetime.now()
        accel_x, accel_y, accel_z = accel.acceleration
        squares = ( np.power(accel_x,2) + np.power(accel_y,2) + np.power(accel_z,2) )
        val = np.sqrt(squares)

        logstring = str(now) + " %0.5f %0.5f %0.5f %0.5f" %(accel_x, accel_y, accel_z, val)
        print(logstring)
        logger.info(logstring)

        if val > 10:
            print("HALLO?")
            break

        time.sleep(0.1)
