#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import UInt8

class Rplidar_sub_node:
    def __init__(self,node_name):
        rospy.init_node(node_name,anonymous=True)
        self.sub=rospy.Subscriber("/slam_out_pose",PoseStamped,self.Rp_callback)

    def Rp_callback(self,msg):
        rospy.loginfo("Robot's Position: %s" % str(msg.pose))
        # 这里接接下来的处理程序

    def start_listening(self):
        rospy.spin()

class Publisher_servo_node:
    def __init__(self,node_name):
        rospy.init_node(node_name,anonymous=True)
        self.pub=rospy.Publisher("servo_move",UInt8,queue_size=10)
        self.rate=rospy.Rate(10)

    def start_publish(self):
        while not rospy.is_shutdown():
            rospy.loginfo("now we catch the target!")
            self.pub.publish(1)
            self.rate.sleep()


if __name__=="__main__":
    try:
        rplidar_node=Rplidar_sub_node("node2")
        servo_node=Publisher_servo_node("node3")
        rplidar_node.start_listening()
        servo_node.start_publish()
    except rospy.ROSInterruptException:
        pass

