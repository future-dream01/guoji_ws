#!/usr/bin/env python3
# 无人机飞行主程序节点

import rospy
import Jetson.GPIO as GPIO
import time
from std_msgs.msg import UInt8
from geometry_msgs.msg import PoseStamped

x,y=0,0                   # 初始化位置x，y
obj,x_p,y_p=0,0,0         # 初始化目标位置偏移x_p、y_p

# 初始化GPIO引脚
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(19,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(20,GPIO.OUT,initial=GPIO.LOW)

class MainNode():
    def __init__(self):
        rospy.init_node("main",anonymous=True)
        self.servo_pub=rospy.Publisher("servo_action",UInt8,queue_size=10)                      # 舵机发布者节点
        self.rplidar_sub=rospy.Subscriber("/slam_out_pose",PoseStamped,self.rplidar_callback)   # 雷达订阅者节点 
        self.yolox_pub=rospy.Publisher("yolox_action",UInt8,queue_size=10)                      # 识别指令发布者
        self.yolox_sub=rospy.Subscriber("yolox_data",PoseStamped,self.yolox_callback)           # 识别结果订阅者
        self.rate=rospy.Rate(10)                                                                # 频率
    
    def servo_start_pub(self,a):
        rospy.loginfo("now we catch the target!")
        self.servo_pub.publish(a)

    def shibie_prepare_pub(self):       # 识别准备工作启动函数
        for i in range(0,10):
            self.yolox_pub(0)

    def shibie_start_pub(self):         # 开始识别函数
        for i in range(0,10):
            self.yolox_pub(1)   

    def shibie_stop_pub(self):          # 识别停止函数
        for i in range(0,10):
            self.yolox_pub(2)

    def rplidar_callback(self,msg):     # 激光雷达位姿数据订阅函数
        global x,y
        x = msg.pose.position.x         # 无人机当前的x位置
        y = msg.pose.position.y         # 无人机当前的y位置
        pass


    def yolox_callback(self,msg):       # 识别数据订阅函数
        global obj,x_p,y_p
        obj=msg.data.                   # 识别出的物体类别
        x_p=msg.data.                   # 物体的x偏移量
        y_p=msg.data.                   # 物体的y偏移量

def ryg_lights(light):
    if light==1:                        # 黄灯亮，代表雷达有数据出来，位姿数据正常
        GPIO.output(18,GPIO.HIGH)
    if light==2:                        # 绿灯亮，代表所有节点启动完毕，可以起飞
        GPIO.output(19,GPIO.HIGH)
    if light==3:                        # 红灯亮，代表识别有数据传出
        GPIO.output(20,GPIO.HIGH)


# 主函数
def main():
    mainnode=MainNode()
    while not rospy.is_shutdown(): 
        if x<=1:
            mainnode.servo_start_pub(int(x))
        pass


if __name__=='__main__':
    main()

