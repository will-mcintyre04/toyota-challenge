#Start with imports, ie: import the wrapper
#import other libraries as needed
import TMMC_Wrapper
import modules.safety_features
import rclpy
import numpy as np
import math
import time
import statistics as stats
import modules

def wall_dist(scan):
    #30:75
    #285:330
    left_scan = scan.ranges[280:360]
    right_scan = scan.ranges[0:80]

    left_angle = left_scan.index(max(left_scan))
    right_angle = right_scan.index(max(right_scan))

    left_mean = stats.mean(left_scan)
    right_mean = stats.mean(right_scan)
    
    
    print("Right: ", right_mean, right_angle)
    print("Left: ", left_mean, left_angle)
    #time.sleep(0.2)


    return (right_mean,left_mean)

def p_follow(dist_arr, gain):
    error = dist_arr[0]-dist_arr[1]
    power = abs(error*gain)

    # if dist_arr[1] > 1.5 and dist_arr[0] > 0.2:
    #     robot.send_cmd_vel(0.0,0.0)
    #     time.sleep(0.1)
    #     robot.turn_left()
    #     time.sleep(0.1)
    #     robot.send_cmd_vel(0.0,0.0)


    # if abs(error) > 1:
    #     robot.send_cmd_vel(0.0,0.0)
    #     return

    if dist_arr[0] < dist_arr[1]:
        robot.send_cmd_vel(0.2, power)
    elif dist_arr[0] > dist_arr[1]:
        robot.send_cmd_vel(0.2, -power)
    
    time.sleep(0.1)

#Start ros with initializing the rclpy object
if not rclpy.ok():
    rclpy.init()

TMMC_Wrapper.is_SIM = False
if not TMMC_Wrapper.is_SIM:
    #Specify hardware api
    TMMC_Wrapper.use_hardware()
    lidar_const = 2
    lidar_shift = 180
    
if not "robot" in globals():
    robot = TMMC_Wrapper.Robot()
    lidar_const = 1
    lidar_shift = 0


#Debug messaging 
print("running main")

#start processes
#add starter functions here
robot.start_keyboard_control() 

#rclpy,spin_once is a function that updates the ros topics once
rclpy.spin_once(robot, timeout_sec=0.1)

#run control functions on loop
try:
    print("Entering the robot loop which cycles until the srcipt is stopped")
    while True: 
        
        #rclpy,spin_once is a function that updates the ros topics once
        rclpy.spin_once(robot, timeout_sec=0.1)
        scan = robot.checkScan()
        if scan is not None:
            dist_arr = wall_dist(scan)
            p_follow(dist_arr, 1.2)

        #Add looping functionality here
        
except KeyboardInterrupt:
    print("keyboard interrupt receieved.Stopping...")
finally:
    #when exiting program, run the kill processes
    #add functionality to ending processes here
    robot.destroy_node()
    rclpy.shutdown()
