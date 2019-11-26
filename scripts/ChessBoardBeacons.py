#!/usr/bin/env python
import rospy

from visualization_msgs.msg import Marker
from geometry_msgs.msg import PoseArray, Pose

# Square width and height in inches
SQUARE_WIDTH = 1
SQUARE_HEIGHT = 1

# Square width and height scalar
# it should be the conversion rate of inches to meters
SCALAR = 0.0254

XOFFSET = 10
YOFFSET = -3.5

FRAME = "/panda_link0"

def publishBeacons(publisher):
    ''' Publishes all the beacons.
    '''

    chessPoses = PoseArray()

    chessPoses.header.frame_id = FRAME

    # Get the coordinates of each of the squares
    for row in range (0, 8):
        for col in range(0, 8):
            currentSquare = Pose()
            currentSquare.position.x = row * SQUARE_WIDTH * SCALAR + XOFFSET * SCALAR
            currentSquare.position.y = col * SQUARE_HEIGHT * SCALAR + YOFFSET * SCALAR
            currentSquare.position.z = 4 * SCALAR
            chessPoses.poses.append(currentSquare)

    publisher.publish(chessPoses)


def spawnBeacons():
    ''' Defines the beacons for each of the chess board
    squares. A total of 64 beacons will be made.
    '''
    # Initialize the node
    rospy.init_node("ChessBoardBeacon", anonymous=True)

    # Publisher for the beacons
    publisher = rospy.Publisher("ChessBoardBeacons", PoseArray, queue_size=10)

    # Publisher rate at 1 Hz
    # The beacons never change so
    # it does not make sense to
    # update more than once per second
    publisherRate = rospy.Rate(1)

    while not rospy.is_shutdown():
        # Publish the beacons
        publishBeacons(publisher)

        # Sleep until next publish
        publisherRate.sleep()

# Main Function
if __name__ == "__main__":
    try:
        spawnBeacons()
    except rospy.ROSInterruptException:
        pass
