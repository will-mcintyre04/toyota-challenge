#Start with imports, ie: import the wrapper
#import other libraries as needed
import TMMC_Wrapper
from modules import safety_features
import rclpy

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

#add starter functions here
robot.start_keyboard_control() 

#rclpy,spin_once is a function that updates the ros topics once
rclpy.spin_once(robot, timeout_sec=0.1)

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
            min_distance = safety_features.find_min_distance_in_view(scan, VIEWING_ANGLE_RANGE, TMMC_Wrapper.is_SIM)
            if(min_distance < 0.2):
                safety_features.backup_until_distance(robot, 0.35, VIEWING_ANGLE_RANGE, TMMC_Wrapper.is_SIM)
        
except KeyboardInterrupt:
    print("keyboard interrupt receieved.Stopping...")
finally:
    #when exiting program, run the kill processes
    #add functionality to ending processes here
    robot.destroy_node()
    rclpy.shutdown()

