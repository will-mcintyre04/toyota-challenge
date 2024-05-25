#Start with imports, ie: import the wrapper
#import other libraries as needed
import TMMC_Wrapper
import rclpy
import numpy as np
import math
import time

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

#run control functions on loop
try:
    print("Entering the robot loop which cycles until the srcipt is stopped")
    while True:

        #rclpy,spin_once is a function that updates the ros topics once
        rclpy.spin_once(robot, timeout_sec=0.1)

        scan = robot.checkScan()
        print(scan)
        print(robot.detect_obstacle(scan))

        #Add looping functionality here
        if robot.detect_obstacle(scan) != (-1, -1):
            print("too close")
            start_time = time.time()
            while time.time() - start_time < 2:
                robot.send_cmd_vel(0.0, 0.0)
            robot.keyboard_listener.stop()
            print("Stop loop ended") 

            # Get the current time
            start_time = time.time()

            print("looping")
            # Loop for 2 seconds
            while time.time() - start_time < 3:
                robot.move_backward()

            print("Back Loop has ended.")  

            start_time = time.time()
            while time.time() - start_time < 2:
                robot.send_cmd_vel(0.0, 0.0)   

            print("Stop loop ended") 

            robot.keyboard_listener.stop()                                                                      

        # If UNSAFE (lidar detects close objecs)
            # do something that stops the listener and then go to newmans function then start the listener again
        
except KeyboardInterrupt:
    print("keyboard interrupt receieved.Stopping...")
finally:
    #when exiting program, run the kill processes
    #add functionality to ending processes here
    robot.destroy_node()
    rclpy.shutdown()
