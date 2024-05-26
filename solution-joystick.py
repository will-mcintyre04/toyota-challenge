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

TMMC_Wrapper.is_SIM = False
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


    ss_data = []
    avgs = {}
    april_stops = {
        2:False,
        3:False
    }

    while True: 
        rclpy.spin_once(robot, timeout_sec=0.1)
        
        # safety_features.detect_stopsign_april(robot)
        april_detect = safety_features.detect_stopsign_april(robot)
        # if len(april_detect) > 0:
        #     ss_data.append(april_detect)
        # if ss_data.__len__() == 5:
        #     avgs.clear()
        #     for dic in ss_data:
        #         for key in dic:
        #             if key in april_stops:
        #                 if key not in avgs:
        #                     dist = dic[key][0]
        #                     if dist > 1000:
        #                         avgs[key] = [None,dic[key][1][0]]
        #                     else:
        #                         avgs[key] = [dic[key][0],dic[key][1][0]]
        #                 else:
        #                     if dic[key][0] <= 1000:
        #                         if avgs[key][0] == None:
        #                                 avgs[key][0] = dic[key][0]
        #                         else:
        #                             avgs[key][0] = (dic[key][0] + avgs[key][0]) / 2
        #                     avgs[key][1] = (dic[key][1][0] + avgs[key][1]) / 2
        #     ss_data.clear()
        #     print(avgs)
        
        if not (2 in april_detect) and april_stops[2]:
            april_stops[2] = False
        if not (3 in april_detect) and april_stops[3]:
            april_stops[3] = False

        scan = robot.checkScan()
        min_distance = safety_features.find_min_distance_in_view(scan, 30, TMMC_Wrapper.is_SIM)
        print("-------------")
        print(april_detect)
        print(min_distance)
        print(april_stops[2])
        print(april_stops[3])

        if 2 in april_detect and not april_stops[2]:
            if min_distance < 1.15:
                robot.stop(wait=2)
                print("stop")
                april_stops[2] = True
        if 3 in april_detect and not april_stops[3]:
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


