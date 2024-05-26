from TMMC_Wrapper import Robot as rb
import time
import cv2
import numpy as np
from cv_bridge import CvBridge

__backup_dist = 0.33  # in metres

def stop_backup(robot: rb):
    if robot.keyboard_listener is not None:
        robot.keyboard_listener.wait()

    robot.stop()
    time.sleep(0.5)
    robot.move_distance(-__backup_dist)

    if robot.keyboard_listener is not None:
        robot.keyboard_listener.start()

def detect_stopsign(robot: rb):
    img_msg = robot.checkImage()
    if img_msg is not None:
        bridge = CvBridge()
        cv2_image = bridge.imgmsg_to_cv2(img_msg, desired_encoding='passthrough')
        cv2.imshow("output window", cv2_image)
        cv2.waitKey(0)
