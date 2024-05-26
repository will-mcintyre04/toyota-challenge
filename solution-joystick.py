#start with imports, ie: import the wrapper
import TMMC_Wrapper
import modules.safety_features
import rclpy
import numpy as np
import math
from modules import safety_features
from modules import image

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
    while True: 
        rclpy.spin_once(robot, timeout_sec=0.1)
        
        # safety_features.detect_stopsign_april(robot)
        safety_features.detect_stopsign_ml(robot)

except KeyboardInterrupt:
    print("keyboard interrupt receieved.Stopping...")
finally:
    #when exiting program, run the kill processes
    robot.stop_keyboard_control()
    robot.destroy_node()
    rclpy.shutdown()


