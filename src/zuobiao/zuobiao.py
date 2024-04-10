#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import PoseStamped
def pose_callback(msg):
    rospy.loginfo("Robot's Position: %s" % str(msg.pose))

if __name__ == '__main__':
    rospy.init_node('zuobiao', anonymous=True)
    rospy.Subscriber("/slam_out_pose", PoseStamped, pose_callback)
    rospy.spin()

