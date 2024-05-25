from TMMC_Wrapper import Robot as rb
import time

__backup_dist = 0.33  # in metres

def stop_backup(robot: rb):
    if robot.keyboard_listener is not None:
        robot.keyboard_listener.stop()

    robot.stop()
    time.sleep(0.5)
    robot.move_distance(-__backup_dist)

    if robot.keyboard_listener is not None:
        robot.keyboard_listener.run()