from TMMC_Wrapper import Robot as rb
import time

__backup_dist = 0.33  # in metres

def stop_backup(robot: rb):
    robot.stop_keyboard_control()

    robot.stop()
    time.sleep(0.5)
    robot.move_distance(-__backup_dist)

    robot.start_keyboard_control()
