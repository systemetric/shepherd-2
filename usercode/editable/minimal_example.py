"""  _____                                 _             _
    |  ___|                               | |           | |
    | |__  __  __  __ _  _ __ ___   _ __  | |  ___  ___ | |
    |  __| \ \/ / / _` || '_ ` _ \ | '_ \ | | / _ \/ __|| |
    | |___  >  < | (_| || | | | | || |_) || ||  __/\__ \|_|
    \____/ /_/\_\ \__,_||_| |_| |_|| .__/ |_| \___||___/(_)
                                | |
                                |_|

Hello robot builder!

Is a basic example to get you up and running. It makes the robot turn and prints
out the codes of the markers which the robot can see.
"""
import robot

R = robot.Robot()

while True:
    R.motors[1] = -90
    R.motors[1] = 90

    markers = R.see()
    for marker in markers:
        print(f"I can see {marker.code}")
