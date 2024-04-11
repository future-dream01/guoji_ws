#!/usr/bin/env python3
import rospy 
from std_msgs.msg import UInt8

class Subscriber_servo_node:
    def __init__(self,node_name):
        rospy.init_node(node_name,anonymous=True)
        self.node_name=node_name
        self.sub=rospy.Subscriber("servo_move",UInt8,self.callback)

    def callback(self,msg):
        rospy.loginfo(rospy.get_caller_id()+"Now the target is %s",msg.data)
        # 接下来进行舵机程序

    def start_listening(self):
        rospy.spin()

if __name__=='__main__':
    servo_node=Subscriber_servo_node("node")
    servo_node.start_listening()