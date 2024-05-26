from TMMC_Wrapper import Robot as rb
import time
import cv2
import numpy as np
from cv_bridge import CvBridge
from ultralytics import YOLO
from pathlib import Path
from modules import image
import rclpy

__backup_dist = 0.33  # in metres


# Function to find the minimum distance within the desired angle range (from center)
def find_min_distance_in_view(scan, angle, is_sim):
    
    # Slice the ranges array to get the desired segment
    ranges = scan.ranges
    if (is_sim):
        segment = ranges[0:int(angle/2) + 1] + ranges[-int(angle/2):] # Sim
    else:
        segment = ranges[180:180 + int(angle) + 1] + ranges[180 - int(-angle): 180 + 1] #  Real Life
    
    # Find the minimum distance in the segment
    min_distance = min(segment)
    
    return min_distance

def backup_until_distance(robot, desired_distance, angle, is_sim):
    robot.stop_keyboard_control()
    # Start moving backwards
    robot.move_backward() # Moving backwards at a slow speed

    while True:
        # Spin once to update the ROS topics
        rclpy.spin_once(robot, timeout_sec=0.1)

        # Get the LIDAR scan data
        scan = robot.checkScan()

        # Ensure scan data is valid
        if scan is not None and hasattr(scan, 'ranges'):
            min_distance = find_min_distance_in_view(scan, angle, is_sim)
            print(f"Current minimum distance: {min_distance:.2f} meters")

            # Check if the robot is at the desired distance
            if min_distance >= desired_distance:
                robot.stop()
                break

    robot.start_keyboard_control()

def detect_stopsign_april(robot: rb):
    
    img = image.get_viewport(robot)
    if img is not None:
        image.display_img(img)
        return robot.detect_april_tag_from_img(img)

def detect_stopsign_ml(robot: rb):
    
    img = image.get_viewport(robot)
    if img is not None:
        model = YOLO(Path(__file__).parent.parent / "yolov8n.pt")
        ss, x1, x2, y1, y2 = robot.ML_predict_stop_sign(model, img)

        if ss:
            print("output")
            cv2.rectangle(img, (x1,x2), (y1,y2), (0,0,255), 2) # mutates ary so don't need to assign
        image.display_img(img)

def detect_stopsign_red(robot: rb):

    img = image.get_viewport(robot)
    if img is not None:
        img = robot.red_filter(img)
        image.display_img(img)

