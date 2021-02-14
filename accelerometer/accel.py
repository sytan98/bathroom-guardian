import board
import busio
import adafruit_lsm303_accel
import queue
import numpy as np
import time

class accelerometer:
    max_len = 5             # Length of past values kept in array
    door_timeout = 5.0      # Timeout for door open detection

    curr_val = 0            # Holder for current value
    past_vals = []          # Array of vals to keep past accel values
    door_open = False       # Output bool
    door_open_time = 0      # Time to keep track of timeout
    
    accel = None            # Accelerometer object

    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.accel = adafruit_lsm303_accel.LSM303_Accel(i2c)
        self.accel.range = adafruit_lsm303_accel.Range.RANGE_8G

    def get_door_open(self):
        return self.door_open

    def updateAccel(self):
        self.curr_val = np.linalg.norm(np.array(self.accel.acceleration)) # Gets the magnitude of the array
        
        # Shift registering here
        self.past_vals.append(self.curr_val)
        if len(self.past_vals) > self.max_len:
            self.past_vals.pop(0)

        # TODO Condition for switching states
        if False:
            self.door_open = True
            self.door_open_time = time.time()
        
        # Door timeout
        if self.door_open and (time.time()-self.door_open_time) > self.door_timeout:
            self.door_open = False