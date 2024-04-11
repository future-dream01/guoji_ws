#!/usr/bin/env python3
# 舵机订阅者节点

import rospy 
from std_msgs.msg import UInt8


class Subscriber_servo_node:
    def __init__(self):
        rospy.init_node("node3",anonymous=True)
        self.sub=rospy.Subscriber("servo_move",UInt8,self.callback)

    def callback(self,msg):
        rospy.loginfo(rospy.get_caller_id()+"Now the target is %s",msg.data)
        # 接下来进行舵机程序

    def start_listening(self):
        rospy.spin()

if __name__=='__main__':
    servo_node=Subscriber_servo_node()
    while True:
        pass
    #servo_node.start_listening()