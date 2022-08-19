"""  _____                                 _             _
    |  ___|                               | |           | |
    | |__  __  __  __ _  _ __ ___   _ __  | |  ___  ___ | |
    |  __| \ \/ / / _` || '_ ` _ \ | '_ \ | | / _ \/ __|| |
    | |___  >  < | (_| || | | | | || |_) || ||  __/\__ \|_|
    \____/ /_/\_\ \__,_||_| |_| |_|| .__/ |_| \___||___/(_)
                                | |
                                |_|

Hello robot builder!

Here are some code snippets which you can use. Try and understand how each one
works and think about how you can build upon it to make your robot go.

Not everything which your robot can do is shown bellow. For comprehensive
documentation have a look at the documentation:
https://robocon.uk/docs/
"""
import robot

# This creates robot "object" called `R`.
# `R` is model for the real robot. The RoboCon software keeps the virtual
# robot's state the same as the real-life robot.
R = robot.Robot()

# ------------------------------------------------------------------------------
#  VISION
# ------------------------------------------------------------------------------

# --------------
# Prints all of the infomation about all of the markers that the robot can see
markers = R.see()
print(markers)


# --------------
# Print only the ID and distance of the markers the robot can see
markers = R.see()
for marker in markers:
    print(f"I can see a marker number {marker.code} {marker.dist}m away!")


# --------------
# Print the angle which the robot needs to turn to get to a marker
# The string in the print is split over multiple lines to make it easier to read
markers = R.see()
for marker in markers:
    print(f"To get to marker number {marker.code} I need to turn"
          f" {marker.bearing.y}!")


# --------------
# Print only the distances to the arena markers
# Method 1 - In a random order
markers = R.see()
for marker in markers:
    if marker.species == "arena":
        print(f"There is an arena marker {marker.dist}m away!")


# --------------
# Print only the distances to the arena markers
# Method 2 - Sorted by the ones which are closest

markers = R.see()

# A list of only arena markers
arena_markers = [m for m in markers if m.speicies == "arena"]

def get_marker_dist(marker):
    return marker.dist
sorted_arena_markers = sorted(arena_markers, key=get_marker_dist)

for arena_marker in sorted_arena_markers:
    print(f"I can see a marker {arena_marker.dist}m away!")


# --------------
# Print only the distances to the arena markers
# Method 2 - Sorted by the ones which are closest (a more consise version)
markers = R.see()
arena_markers = [m for m in markers if m.speicies == "arena"]
sorted_arena_markers = sorted(arena_markers, key=lambda m: m.dist)
for arena_marker in sorted_arena_markers:
    print(f"I can see a marker {arena_marker.dist}m away!")


# ------------------------------------------------------------------------------
#  MOTOR CONTROL
# ------------------------------------------------------------------------------

# --------------
# Turn the motors on to 75%
R.motors[1] = 75
R.motors[2] = 75
