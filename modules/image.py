import cv2
from cv_bridge import CvBridge
import threading

# class imageOutput():
#     def __init__(self, robot):
        
#         self.frame = None
#         self.stop = False

#         self.read_thread = threading.Thread(target=self.read, args=(robot,))
#         self.read_thread.daemon = True
#         self.read_thread.start()

#         self.dspl_thread = threading.Thread(target=self.display, args=())
#         self.dspl_thread.daemon = True
#         self.dspl_thread.start()

#     def stop(self):
#         self.stop = True

#     def __read(self, robot):
#         while not self.Stop:
#             self.frame = get_viewport(robot)

#     def __display(self):
#         while not self.stop():
#             if self.frame:
#                 cv2.imshow('Output Frame', self.frame)
#                 key = cv2.waitKey(1) 

def get_viewport(robot):
    img_msg = robot.checkImage()
    if img_msg is not None:
        bridge = CvBridge()
        img = bridge.imgmsg_to_cv2(img_msg, desired_encoding='passthrough')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img
    return None


def display_img(img, hold=False):
    cv2.imshow("output window", img)
    if hold:
        cv2.waitKey(0)
    else:
        cv2.waitKey(1)