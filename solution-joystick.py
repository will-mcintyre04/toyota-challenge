#start with imports, ie: import the wrapper
import TMMC_Wrapper
import modules.safety_features
import rclpy
import numpy as np
import math
from modules import safety_features
from modules import image
import time

#start ros
if not rclpy.ok():
    rclpy.init()

TMMC_Wrapper.is_SIM = True
if not TMMC_Wrapper.is_SIM:
    #specify hardware api
    TMMC_Wrapper.use_hardware()
    
if not "robot" in globals():
    robot = TMMC_Wrapper.Robot()

#debug messaging 
print("running main")

#start processes
robot.start_keyboard_control()   #this one is just pure keyboard control

rclpy.spin_once(robot, timeout_sec=0.1)

#run the keyboard control functions
try:
    print("Listening for keyboard events. Press keys to test, Ctrl C to exit")

    april_stops = {
        2:False,
        3:False
    }

    while True: 
        rclpy.spin_once(robot, timeout_sec=0.1)
        
        aprils_detected = safety_features.detect_aprils(robot)
        
        if not np.isin(2, aprils_detected) and april_stops[2]:
            april_stops[2] = False
        if not np.isin(3, aprils_detected) and april_stops[3]:
            april_stops[3] = False

        scan = robot.checkScan()
        min_distance = safety_features.find_min_distance_in_view(scan, 30, TMMC_Wrapper.is_SIM)
        print("-------------")
        print(aprils_detected)
        print(min_distance)
        print(april_stops[2])
        print(april_stops[3])

        if np.isin(2, aprils_detected) and not april_stops[2]:
            if min_distance < 1.15:
                robot.stop(wait=2)
                print("stop")
                april_stops[2] = True
        if np.isin(3, aprils_detected) and not april_stops[3]:
            if min_distance < 1.15:
                robot.stop(wait=2)
                print("stop")
                april_stops[3] = True


except KeyboardInterrupt:
    print("keyboard interrupt receieved.Stopping...")
finally:
    #when exiting program, run the kill processes
    robot.stop_keyboard_control()
    robot.destroy_node()
    rclpy.shutdown()


