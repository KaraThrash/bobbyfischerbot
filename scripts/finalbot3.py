#!/usr/bin/env python
# Ref 1: http://wiki.ros.org/rviz/DisplayTypes/Marker
# Ref 2: https://answers.ros.org/question/203782/rviz-marker-line_strip-is-not-displayed/

import rospy
import rosbag
import math
import numpy
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point

from geometry_msgs.msg import Twist,Vector3
from nav_msgs.msg import Odometry
import tf.transformations as transform

from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist,Vector3
grid = []
grida = []
line_points = []
landmarks = [(6.25,26.25),(6.25,16.25),(6.25,6.25),(21.25,6.25),(21.25,16.25),(21.25,26.25) ]
rospy.loginfo('Rviz example')
botrot = 0.0
zplus = 0.0
def display_line_list(points, publisher):
    """
    A function that publishes a set of points as marker line list to Rviz.
    It will draw a line between each pair of points, so 0-1, 2-3, 4-5, ...

    Parameters:
    points (list): Each item in the list is a tuple (x, y) representing a point in xy space.
    publisher (rospy.Publisher): A publisher object used to pubish the marker

    Returns:
    None

    """

    marker = Marker()
    # The coordinate frame in which the marker is publsihed.
    # Make sure "Fixed Frame" under "Global Options" in the Display panel
    # in rviz is "/map"
    marker.header.frame_id = "/map"

    # Mark type (http://wiki.ros.org/rviz/DisplayTypes/Marker)
    # LINE_LIST: It will draw a line between each pair of points, so 0-1, 2-3, 4-5, ...
    marker.type = marker.LINE_LIST

    # Marker action (Set this as ADD)
    marker.action = marker.ADD

    # Marker scale
    marker.scale.x = 0.01
    marker.scale.y = 0.01
    marker.scale.z = 0.01

    # Marker color (Make sure a=1.0 which sets the opacity)
    marker.color.a = 1.0
    marker.color.r = 1.0
    marker.color.g = 1.0
    marker.color.b = 0.0

    # Marker orientaiton (Set it as default orientation in quaternion)
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0

    # Marker position
    # The position of the marker. In this case it the COM of all the points
    # Set this as 0,0,0
    marker.pose.position.x = 0.0
    marker.pose.position.y = 0.0
    marker.pose.position.z = 0.0

    # Marker line points
    marker.points = []


    # zplus = 0.0
    # points2 = [points[len(points) - 1],points[len(points) - 2],points[len(points )- 3],points[len(points )- 4]]
    for point in points:
        global zplus
        marker_point = Point()              # Create a new Point()
        marker_point.x = (point[0] ) * 0.15
        marker_point.y = (point[1] ) * 0.15

        marker.color.b = 1.0
        marker.color.r = 1.0
        marker.color.g = 1.0
        # zplus = zplus + 0.01
        # print(zplus)
        marker.points.append(marker_point) # Append the marker_point to the marker.points list

    # Publish the Marker using the appropirate publisher
    publisher.publish(marker)


def display_cube_list(points, publisher):
    """
    A function that publishes a set of points as marker cubes in Rviz.
    Each point represents the COM of the cube to be displayed.

    Parameters:
    points (list): Each item in the list is a tuple (x, y) representing a point in xy space
                   for the COM of the cube.
    publisher (rospy.Publisher): A publisher object used to pubish the marker

    Returns:
    None

    """

    marker = Marker()
    # The coordinate frame in which the marker is published.
    # Make sure "Fixed Frame" under "Global Options" in the Display panel
    # in rviz is "/map"
    marker.header.frame_id = "/map"

    # Mark type (http://wiki.ros.org/rviz/DisplayTypes/Marker)
    # CUBE_LIST
    marker.type = marker.CUBE_LIST

    # Marker action (Set this as ADD)
    marker.action = marker.ADD

    # Marker scale (Size of the cube)
    marker.scale.x = 0.1
    marker.scale.y = 0.1
    marker.scale.z = 0.1

    # Marker color (Make sure a=1.0 which sets the opacity)
    marker.color.a = 1.0
    marker.color.r = 0.0
    marker.color.g = 1.0
    marker.color.b = 0.0

    # Marker orientation (Set it as default orientation in quaternion)
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0

    # Marker position
    # The position of the marker. In this case it the COM of all the cubes
    # Set this as 0,0,0
    marker.pose.position.x = 0.0
    marker.pose.position.y = 0.0
    marker.pose.position.z = 0.0

    # Marker line points
    marker.points = []

    for point in points:

        marker_point = Point()              # Create a new Point()
        marker_point.x = point[0] * 0.15
        marker_point.y = point[1] * 0.15
        marker_point.z = 0

        marker.points.append(marker_point)  # Append the marker_point to the marker.points list

    # Publish the Marker using the apporopriate publisher
    publisher.publish(marker)



def predictmotion():
    global grida
    global grid
    global landmarks
    count = -1
    count2 = 0
    pos = (0,0,0)
    secondbest = (1,1,3)
    currenthighest = 0
    secondhighest = 0
    tempcount = 0

    while count < 35:
        count = count + 1
        count2 = 0
        tempcount = 0
        while count2 < 35:
 # the 4 possible rotations that could be in the square
            tempcount = grida[count][count2][0] + grida[count][count2][1] + grida[count][count2][2] + grida[count][count2][3]
            if tempcount > currenthighest:
                secondhighest = currenthighest
                currenthighest = tempcount
                secondbest = pos
                pos = (count,count2,0)
                temprotcount = grida[pos[0]][pos[1]][0]
                if grida[pos[1]][pos[1]][1] > temprotcount:
                    temprotcount = grida[pos[1]][pos[1]][1]
                    pos = (pos[0],pos[1], 90)
                if grida[pos[1]][pos[1]][2] > temprotcount:
                    temprotcount = grida[pos[1]][pos[1]][2]
                    pos = (pos[0],pos[1],2 * 90)
                if grida[pos[1]][pos[1]][3] > temprotcount:
                    pos = (pos[0],pos[1],3 * 90)
            count2 = count2 + 1

    # grid = grida
    setgrida()
    # grid[pos[0]][pos[1]][pos[2]] = 1
    line_points.append((pos[0],pos[1]))
    # grid[secondbest[0]][secondbest[1]][secondbest[2]] = 1

    f = open("results.txt", "a")
    f.write("P: ")
    f.write(str(pos))
    #
    f.write("\n")
    # f.write("\n")
    f.close()

def predictobserve():
    global grida
    global grid
    global landmarks
    count = -1
    count2 = 0
    pos = (0,0,0)
    secondbest = (1,1,3)
    currenthighest = 0
    secondhighest = 0
    tempcount = 0

    while count < 35:
        count = count + 1
        count2 = 0
        tempcount = 0
        while count2 < 35:
 # the 4 possible rotations that could be in the square
            tempcount = grida[count][count2][0] + grida[count][count2][1] + grida[count][count2][2] + grida[count][count2][3]
            if tempcount > currenthighest:
                secondhighest = currenthighest
                currenthighest = tempcount
                secondbest = pos
                pos = (count,count2,0)
                temprotcount = grida[pos[0]][pos[1]][0]
                if grida[pos[1]][pos[1]][1] > temprotcount:
                    temprotcount = grida[pos[1]][pos[1]][1]
                    pos = (pos[0],pos[1], 90)
                if grida[pos[1]][pos[1]][2] > temprotcount:
                    temprotcount = grida[pos[1]][pos[1]][2]
                    pos = (pos[0],pos[1],2 * 90)
                if grida[pos[1]][pos[1]][3] > temprotcount:
                    pos = (pos[0],pos[1],3 * 90)
            count2 = count2 + 1


    setgrida()
    grid[pos[0]][pos[1]][pos[2]] = 1

    line_points.append((pos[0],pos[1]))
    # grid[secondbest[0]][secondbest[1]][secondbest[2]] = 1

    f = open("results.txt", "a")
    f.write("U: ")
    f.write(str(pos))
    #
    f.write("\n")
    # f.write("\n")
    f.close()

# reset grid a to use to sum probabilities
def setgrida():
    global grida
    count = -1
    count2 = 0

    gridd = []

    # NOTE: for movement multiople translation by 5, result in numbert of squares distance
    while count < 35:
        gridb = []
        gridd.append(gridb)
        count = count + 1
        count2 = 0
        while count2 < 35:
 # the 4 possible rotations that could be in the square
            gridc = [0,0,0,0]
            gridb.append(gridc)
            # grid[count][count2] = [grida[count][count2][0],grida[count][count2][1],grida[count][count2][2],grida[count][count2][3]]
            grida[count][count2] = [0,0,0,0]
            # grid[count][count2] = [0,0,0,0]
            count2 = count2 + 1
    # grida = gridd

def bayesobserve(msg):
    global grid
    global grida
    global landmarks
    count = -1
    count2 = 0

    while count < 35:
        count = count + 1
        count2 = 0
        # while count2 < 35:
        #     if  abs(math.sqrt( ( count - landmarks[msg.tagNum][0])**2 + ( count2  - landmarks[msg.tagNum][1])**2 ) - (msg.range * 5)) > 0.2:
        #         grida[count][count2][0] = grida[count][count2][0] * 2
        #         grida[count][count2][1] = grida[count][count2][1] * 2
        #         grida[count][count2][2] = grida[count][count2][2] * 2
        #         grida[count][count2][3] = grida[count][count2][3] * 2
            # else:
            #     grida[count][count2][0] = grida[count][count2][0] * 0.2
            #     grida[count][count2][1] = grida[count][count2][1] * 0.2
            #     grida[count][count2][2] = grida[count][count2][2] * 0.2
            #     grida[count][count2][3] = grida[count][count2][3] * 0.2
            # count2 = count2 + 1
def bayesmotion(msg):
    global grid
    global grida
    global landmarks
    quaternion = (msg.rotation1.x,msg.rotation1.y,msg.rotation1.z,msg.rotation1.w)
    euler = transform.euler_from_quaternion(quaternion)

    degrees = numpy.degrees(euler)
    gausrots =  numpy.random.normal(degrees[2], 45, 100) #rot1
    # NOTE: for movement multiople translation by 5, result in numbert of squares distance
    sortedrots = [0,0,0,0]
    for normalrot in gausrots:
        if normalrot < 45 and normalrot > -45:
            sortedrots[0] = sortedrots[0] + 1
        elif normalrot < 135 and normalrot > 0:
            sortedrots[1] = sortedrots[1] + 1
        elif normalrot < -45 and normalrot > -135 :
            sortedrots[3] = sortedrots[3] + 1
        else:
            sortedrots[2] = sortedrots[2] + 1


    quaternion2 = (msg.rotation2.x,msg.rotation2.y,msg.rotation2.z,msg.rotation2.w)
    euler2 = transform.euler_from_quaternion(quaternion2)
    degrees2 = numpy.degrees(euler2)
    gausrots2 = numpy.random.normal(degrees2[2], 45, 100) #rot2
    sortedrots2 = [0,0,0,0]
    for normalrot2 in gausrots2:
        if normalrot2 < 45 and normalrot2 > -45:
            sortedrots2[0] = sortedrots2[0] + 1
        elif normalrot2 < 135 and normalrot2 > 0:
            sortedrots2[1] = sortedrots2[1] + 1
        elif normalrot2 < -45 and normalrot2 > -135 :
            sortedrots2[3] = sortedrots2[3] + 1
        else:
            sortedrots2[2] = sortedrots2[2] + 1

    travelnormal = numpy.random.normal((msg.translation * 20), 0.5, 100) # translation
    rowcount = -1
    colcount = -1

    # go through each square and if there is probabikity that the bot is there
    # Then set the values on the OTHER grid, resulting in the sum of all possible ecurrent states
    while rowcount < 35:
        # print("row: ",rowcount)
        rowcount = rowcount + 1
        colcount = -1
        while colcount < 35:
            colcount = colcount + 1
            col = grid[rowcount][colcount]

    # NOTE: for movement multiople translation by 5, result in numbert of squares distance
            for distnotrounded in travelnormal:
                dist = 0
                dist = int(round(distnotrounded))
                # NOTE: iterate through each possible rotation and current rotation in square to check if moving the distance is on the map
                if col[0] > 0: # right
                    if colcount + dist <= 35:
                        grida[rowcount][colcount + dist][0] = grida[rowcount][colcount + dist][0] + (col[0] * sortedrots2[0] * sortedrots2[0])
                        grida[rowcount][colcount + dist][1] = grida[rowcount][colcount + dist][1] + (col[0] * sortedrots2[0] * sortedrots2[1])
                        grida[rowcount][colcount + dist][2] = grida[rowcount][colcount + dist][2] + (col[0] * sortedrots2[0] * sortedrots2[2])
                        grida[rowcount][colcount + dist][3] = grida[rowcount][colcount + dist][3] + (col[0] * sortedrots2[0] * sortedrots2[3])
                    if colcount - dist >= 0:
                        grida[rowcount][colcount - dist][2] = grida[rowcount][colcount - dist][0] + (col[0] * sortedrots2[2] * sortedrots2[0])
                        grida[rowcount][colcount - dist][3] = grida[rowcount][colcount - dist][1] + (col[0] * sortedrots2[2] * sortedrots2[1])
                        grida[rowcount][colcount - dist][0] = grida[rowcount][colcount - dist][2] + (col[0] * sortedrots2[2] * sortedrots2[2])
                        grida[rowcount][colcount - dist][1] = grida[rowcount][colcount - dist][3] + (col[0] * sortedrots2[2] * sortedrots2[3])
                    if rowcount - dist >= 0:
                        grida[rowcount- dist][colcount ][1] = grida[rowcount - dist][colcount ][0] + (col[0] * sortedrots2[1] * sortedrots2[0])
                        grida[rowcount - dist][colcount ][2] = grida[rowcount - dist][colcount ][1] + (col[0] * sortedrots2[1] * sortedrots2[1])
                        grida[rowcount - dist][colcount ][3] = grida[rowcount - dist][colcount ][2] + (col[0] * sortedrots2[1] * sortedrots2[2])
                        grida[rowcount - dist][colcount ][0] = grida[rowcount - dist][colcount ][3] + (col[0] * sortedrots2[1] * sortedrots2[3])
                    if rowcount + dist <= 35:
                        grida[rowcount+ dist][colcount][3] = grida[rowcount + dist][colcount ][0] + (col[0] * sortedrots2[3] * sortedrots2[0])
                        grida[rowcount+ dist][colcount ][0] = grida[rowcount + dist][colcount ][1] + (col[0] * sortedrots2[3] * sortedrots2[1])
                        grida[rowcount+ dist][colcount ][1] = grida[rowcount + dist][colcount ][2] + (col[0] * sortedrots2[3] * sortedrots2[2])
                        grida[rowcount+ dist][colcount ][2] = grida[rowcount + dist][colcount ][3] + (col[0] * sortedrots2[3] * sortedrots2[3])

                    # rot 1: the bot current facing up
                if col[1] > 0: # up
                    if colcount + dist <= 35:
                        grida[rowcount][colcount + dist][0] = grida[rowcount][colcount + dist][0] + (col[1] * sortedrots2[3] * sortedrots2[0])
                        grida[rowcount][colcount + dist][1] = grida[rowcount][colcount + dist][1] + (col[1] * sortedrots2[3] * sortedrots2[1])
                        grida[rowcount][colcount + dist][2] = grida[rowcount][colcount + dist][2] + (col[1] * sortedrots2[3] * sortedrots2[2])
                        grida[rowcount][colcount + dist][3] = grida[rowcount][colcount + dist][3] + (col[1] * sortedrots2[3] * sortedrots2[3])
                    if colcount - dist >= 0:
                        grida[rowcount][colcount - dist][2] = grida[rowcount][colcount - dist][0] + (col[1] * sortedrots2[0] * sortedrots2[0])
                        grida[rowcount][colcount - dist][3] = grida[rowcount][colcount - dist][1] + (col[1] * sortedrots2[0] * sortedrots2[1])
                        grida[rowcount][colcount - dist][0] = grida[rowcount][colcount - dist][2] + (col[1] * sortedrots2[0] * sortedrots2[2])
                        grida[rowcount][colcount - dist][1] = grida[rowcount][colcount - dist][3] + (col[1] * sortedrots2[0] * sortedrots2[3])
                    if rowcount - dist >= 0:
                        grida[rowcount - dist][colcount ][1] = grida[rowcount - dist][colcount ][0] + (col[1] * sortedrots2[1] * sortedrots2[0])
                        grida[rowcount - dist][colcount ][2] = grida[rowcount - dist][colcount ][1] + (col[1] * sortedrots2[1] * sortedrots2[1])
                        grida[rowcount - dist][colcount ][3] = grida[rowcount - dist][colcount ][2] + (col[1] * sortedrots2[1] * sortedrots2[2])
                        grida[rowcount - dist][colcount ][0] = grida[rowcount - dist][colcount ][3] + (col[1] * sortedrots2[1] * sortedrots2[3])
                    if rowcount + dist <= 35:
                        grida[rowcount + dist][colcount][3] = grida[rowcount + dist][colcount ][0] + (col[1] * sortedrots2[2] * sortedrots2[0])
                        grida[rowcount + dist][colcount ][0] = grida[rowcount + dist][colcount ][1] + (col[1] * sortedrots2[2] * sortedrots2[1])
                        grida[rowcount + dist][colcount ][1] = grida[rowcount + dist][colcount ][2] + (col[1] * sortedrots2[2] * sortedrots2[2])
                        grida[rowcount + dist][colcount ][2] = grida[rowcount + dist][colcount ][3] + (col[1] * sortedrots2[2] * sortedrots2[3])
                if col[2] > 0: # left
                    if colcount + dist <= 35:
                        grida[rowcount][colcount + dist][0] = grida[rowcount][colcount + dist][0] + (col[2] * sortedrots2[2] * sortedrots2[0])
                        grida[rowcount][colcount + dist][1] = grida[rowcount][colcount + dist][1] + (col[2] * sortedrots2[2] * sortedrots2[1])
                        grida[rowcount][colcount + dist][2] = grida[rowcount][colcount + dist][2] + (col[2] * sortedrots2[2] * sortedrots2[2])
                        grida[rowcount][colcount + dist][3] = grida[rowcount][colcount + dist][3] + (col[2] * sortedrots2[2] * sortedrots2[3])
                    if colcount - dist >= 0:
                        grida[rowcount][colcount - dist][2] = grida[rowcount][colcount - dist][0] + (col[2] * sortedrots2[0] * sortedrots2[0])
                        grida[rowcount][colcount - dist][3] = grida[rowcount][colcount - dist][1] + (col[2] * sortedrots2[0] * sortedrots2[1])
                        grida[rowcount][colcount - dist][0] = grida[rowcount][colcount - dist][2] + (col[2] * sortedrots2[0] * sortedrots2[2])
                        grida[rowcount][colcount - dist][1] = grida[rowcount][colcount - dist][3] + (col[2] * sortedrots2[0] * sortedrots2[3])
                    if rowcount - dist >= 0:
                        grida[rowcount - dist][colcount ][1] = grida[rowcount - dist][colcount ][0] + (col[2] * sortedrots2[3] * sortedrots2[0])
                        grida[rowcount - dist][colcount ][2] = grida[rowcount - dist][colcount ][1] + (col[2] * sortedrots2[3] * sortedrots2[1])
                        grida[rowcount - dist][colcount ][3] = grida[rowcount - dist][colcount ][2] + (col[2] * sortedrots2[3] * sortedrots2[2])
                        grida[rowcount - dist][colcount][0] = grida[rowcount - dist][colcount ][3] + (col[2] * sortedrots2[3] * sortedrots2[3])
                    if rowcount + dist <= 35:
                        grida[rowcount + dist][colcount ][3] = grida[rowcount + dist][colcount ][0] + (col[2] * sortedrots2[1] * sortedrots2[0])
                        grida[rowcount + dist][colcount ][0] = grida[rowcount + dist][colcount ][1] + (col[2] * sortedrots2[1] * sortedrots2[1])
                        grida[rowcount + dist][colcount ][1] = grida[rowcount + dist][colcount ][2] + (col[2] * sortedrots2[1] * sortedrots2[2])
                        grida[rowcount + dist][colcount ][2] = grida[rowcount + dist][colcount ][3] + (col[2] * sortedrots2[1] * sortedrots2[3])
                if col[3] > 0: # down
                    if colcount + dist <= 35:
                        grida[rowcount][colcount + dist][0] = grida[rowcount][colcount + dist][0] + (col[3] * sortedrots2[1] * sortedrots2[0])
                        grida[rowcount][colcount + dist][1] = grida[rowcount][colcount + dist][1] + (col[3] * sortedrots2[1] * sortedrots2[1])
                        grida[rowcount][colcount + dist][2] = grida[rowcount][colcount + dist][2] + (col[3] * sortedrots2[1] * sortedrots2[2])
                        grida[rowcount][colcount + dist][3] = grida[rowcount][colcount + dist][3] + (col[3] * sortedrots2[1] * sortedrots2[3])
                    if colcount - dist >= 0:
                        grida[rowcount][colcount - dist][2] = grida[rowcount][colcount - dist][0] + (col[3] * sortedrots2[3] * sortedrots2[0])
                        grida[rowcount][colcount - dist][3] = grida[rowcount][colcount - dist][1] + (col[3] * sortedrots2[3] * sortedrots2[1])
                        grida[rowcount][colcount - dist][0] = grida[rowcount][colcount - dist][2] + (col[3] * sortedrots2[3] * sortedrots2[2])
                        grida[rowcount][colcount - dist][1] = grida[rowcount][colcount - dist][3] + (col[3] * sortedrots2[3] * sortedrots2[3])
                    if rowcount - dist >= 0:
                        grida[rowcount- dist][colcount ][1] = grida[rowcount - dist][colcount ][0] + (col[3] * sortedrots2[2] * sortedrots2[0])
                        grida[rowcount- dist][colcount ][2] = grida[rowcount - dist][colcount ][1] + (col[3] * sortedrots2[2] * sortedrots2[1])
                        grida[rowcount- dist][colcount ][3] = grida[rowcount - dist][colcount ][2] + (col[3] * sortedrots2[2] * sortedrots2[2])
                        grida[rowcount- dist][colcount ][0] = grida[rowcount - dist][colcount ][3] + (col[3] * sortedrots2[2] * sortedrots2[3])
                    if rowcount + dist <= 35:
                        grida[rowcount+ dist][colcount ][3] = grida[rowcount + dist][colcount ][0] + (col[3] * sortedrots2[0] * sortedrots2[0])
                        grida[rowcount+ dist][colcount ][0] = grida[rowcount + dist][colcount ][1] + (col[3] * sortedrots2[0] * sortedrots2[1])
                        grida[rowcount+ dist][colcount ][1] = grida[rowcount + dist][colcount ][2] + (col[3] * sortedrots2[0] * sortedrots2[2])
                        grida[rowcount+ dist][colcount ][2] = grida[rowcount + dist][colcount ][3] + (col[3] * sortedrots2[0] * sortedrots2[3])




if __name__ == "__main__":
    global botrot
    global grid
    global grida
    global line_points
    global landmarks
    rospy.init_node('toaster3')

    pub_line_list = rospy.Publisher('line_list', Marker, queue_size=10)
    pub_cube_list = rospy.Publisher('cube_list', Marker, queue_size=10)
    line_points = [(13,26)]
    botspots = [(2,2,0),(0,0,0,0)]
    cube_points = [(6.25,26.25), (6.25,16.25), (6.25,6.25), (21.25,6.25) , (21.25,16.25), (21.25,26.25)]
    count = 0
    count2 = 0
    bag = rosbag.Bag('grid.bag')
    botpos = [(0,0)]

    count = 0
    grid = []
    grida = []

    # NOTE: for movement multiople translation by 5, result in numbert of squares distance
    while count < 36:
        grid2 = []
        grid.append(grid2)
        gridb = []
        grida.append(gridb)
        count = count + 1
        count2 = 0
        while count2 < 36:
            grid3 = [0,0,0,0] # the 4 possible rotations that could be in the square
            gridc = [0,0,0,0]
            grid2.append(grid3)
            gridb.append(gridc)
            count2 = count2 + 1

    grid[11][27][3] = 1
    for topic, msg, t in bag.read_messages(topics=[ 'Observations','Movements']):
        if topic == 'Movements':
            # print("movements")
            # setgrida()
            bayesmotion(msg)
            predictmotion()
        # if topic == 'Observations':
            # print("Observations")
            # bayesobserve(msg)
            # predictobserve()
            # grid = grida
            # setgrida()
            # test(msg)
            # predict()

    while not rospy.is_shutdown():
        display_line_list(line_points, pub_line_list)
        display_cube_list(cube_points, pub_cube_list)
