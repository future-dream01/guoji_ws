#!/usr/bin/env python3
# 舵机订阅者节点

import rospy 
from std_msgs.msg import UInt8


x=0     # 0是初值，1代表投递第一个货物，2代表第二个，3代表第三个
y=0     # 0是初值，1代表一次投递完成


class Subscriber_servo_node:
    def __init__(self):
        rospy.init_node("node3",anonymous=True)
        self.sub=rospy.Subscriber("servo_action",UInt8,self.callback)
        self.rate=rospy.Rate(10)        # 一定频率，防止过多占用CPU资源

    def callback(self,msg):
        global x
        #rospy.loginfo(rospy.get_caller_id()+"Now the target is %s",msg.data)
        x=msg.data

def delivery():
    # 舵机指定角度的旋转，完成投递

    # 先顺时针转30度，
    # 延时1秒
    # 逆时针转30度，完成一次投递
    y=1

if __name__=='__main__':
    servo_node=Subscriber_servo_node()
    while not rospy.is_shutdown():
        if x==1 and y==0:       # 第一个货物投递
            delivery()
            y=0
        if x==2 and y==0:       # 第二个货物投递
            delivery()
            y=0
        if x==3 and y==0:       # 第三个货物投递
            delivery()
            y==0
        servo_node.rate.sleep() # 休眠，防止过多占用CPU资源