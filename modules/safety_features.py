from TMMC_Wrapper import Robot as rb
import time
import cv2
import numpy as np
from cv_bridge import CvBridge
from ultralytics import YOLO
from pathlib import Path
from modules import image

__backup_dist = 0.33  # in metres




def stop_backup(robot: rb):
    if robot.keyboard_listener is not None:
        robot.keyboard_listener.wait()

    robot.stop()
    time.sleep(0.5)
    robot.move_distance(-__backup_dist)

    if robot.keyboard_listener is not None:
        robot.keyboard_listener.start()

def detect_stopsign_april(robot: rb):
    
    img = image.get_viewport(robot)
    if img is not None:
        image.display_img(img)
        print(robot.detect_april_tag_from_img(img))

def detect_stopsign_ml(robot: rb):
    
    img = image.get_viewport(robot)
    if img is not None:
        model = YOLO(Path(__file__).parent.parent / "yolov8n.pt")
        ss, x1, x2, y1, y2 = robot.ML_predict_stop_sign(model, img)

        if ss:
            pass
            cv2.rectangle(img, (x1,x2), (y1,y2), (0,0,255), 2) # mutates ary so don't need to assign
            image.display_img(img)
