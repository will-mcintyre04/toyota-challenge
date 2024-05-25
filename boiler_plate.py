#Start with imports, ie: import the wrapper
#import other libraries as needed
import TMMC_Wrapper
import rclpy
import numpy as np
import math
import modules.safety_features

# Constant for angle range from center
VIEWING_ANGLE_RANGE = 90

#Start ros with initializing the rclpy object
if not rclpy.ok():
    rclpy.init()

TMMC_Wrapper.is_SIM = True
if not TMMC_Wrapper.is_SIM:
    #Specify hardware api
    TMMC_Wrapper.use_hardware()
    
if not "robot" in globals():
    robot = TMMC_Wrapper.Robot()

#Debug messaging 
print("running main")

#start processes
robot.start_keyboard_control() 
#add starter functions here

#rclpy,spin_once is a function that updates the ros topics once
rclpy.spin_once(robot, timeout_sec=0.1)

# Function to find the minimum distance within the desired angle range (from center)
def find_min_distance_in_view(scan, angle):
    
    # Slice the ranges array to get the desired segment
    ranges = scan.ranges
    segment = ranges[:int(angle/2) + 1] + ranges[int(-angle/2):]
    
    # Find the minimum distance in the segment
    min_distance = min(segment)
    
    return min_distance

#run control functions on loop
try:
    print("Entering the robot loop which cycles until the script is stopped")
    while(True):
        # Spin once to update the ROS topics
        rclpy.spin_once(robot, timeout_sec=0.1)

        # Get the LIDAR scan data
        scan = robot.checkScan()

        # Ensure scan data is valid
        if scan is not None and hasattr(scan, 'ranges'):
            min_distance = find_min_distance_in_view(scan, VIEWING_ANGLE_RANGE)
            print(min_distance)
            if(min_distance < 0.2):
                modules.safety_features.stop_backup(robot)
        
except KeyboardInterrupt:
    print("keyboard interrupt receieved.Stopping...")
finally:
    #when exiting program, run the kill processes
    #add functionality to ending processes here
    robot.destroy_node()
    rclpy.shutdown()


