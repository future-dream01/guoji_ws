#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import PoseStamped

def slam_out_pose_callback(msg):
    global slam_time
    slam_time = msg.header.stamp
    check_time_sync()

def local_position_callback(msg):
    global local_time
    local_time = msg.header.stamp
    check_time_sync()

def check_time_sync():
    global slam_time, local_time
    if slam_time and local_time:
        time_diff_sec = local_time.secs - slam_time.secs
        time_diff_nsec = local_time.nsecs - slam_time.nsecs
        if time_diff_nsec < 0:
            time_diff_sec -= 1
            time_diff_nsec += 1000000000
        rospy.loginfo(f"Time difference: {time_diff_sec} seconds and {time_diff_nsec} nanoseconds")

if __name__ == '__main__':
    rospy.init_node('time_sync_checker', anonymous=True)
    slam_time = None
    local_time = None
    rospy.Subscriber('/slam_out_pose', PoseStamped, slam_out_pose_callback)
    rospy.Subscriber('/mavros/local_position/pose', PoseStamped, local_position_callback)
    rospy.spin()
