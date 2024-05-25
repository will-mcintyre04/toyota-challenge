from TMMC_Wrapper import Robot as rb

backup_dist = 0.25  # in metres

def stop_backup(robot: rb, ):
    robot.keyboard_listener.stop()
    robot.stop()
    robot.move_distance(backup_dist)
    robot.keyboard_listener.start()