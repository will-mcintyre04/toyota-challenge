from TMMC_Wrapper import Robot as rb
import time

BACKUP_DIST = 0.6  # in metres

# Function to find the minimum distance within the desired angle range (from center)
def find_min_distance_in_view(scan, angle):
    
    # Slice the ranges array to get the desired segment
    ranges = scan.ranges
    segment = ranges[180:180 + int(angle) + 1] + ranges[180 - int(-angle): 180 + 1]
    
    # Find the minimum distance in the segment
    min_distance = min(segment)
    
    return min_distance

def stop_backup(robot: rb):
    robot.stop_keyboard_control()

    robot.stop()
    time.sleep(0.5)

    robot.move_distance_from_wall(BACKUP_DIST)

    robot.start_keyboard_control()

