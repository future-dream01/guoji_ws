#!/usr/bin/env python3
# 无人机飞行主程序节点

import rospy
import time
import Jetson.GPIO as GPIO
from main.msg import Result
from std_msgs.msg import UInt8
from mavros_msgs.srv import SetMode
from mavros_msgs.msg import State
from geometry_msgs.msg import PoseStamped,Twist


# 主节点类
class MainNode():
    def __init__(self):
        rospy.init_node("main",anonymous=True)
        # 属性
        self.x=self.y=self.z=0                                                                              # 初始化位置x，y
        self.x_p=self.y_p=self.obj=0                                                                        # 初始化目标位置偏移x_p、y_p、物体类型
        self.state=False                                                                                    # 无人机是否已起飞
        self.rate=rospy.Rate(10)                                                                            # 频率
        # 话题
        self.servo_pub=rospy.Publisher("servo_action",UInt8,queue_size=10)                                  # 舵机发布者节点
        self.rplidar_sub=rospy.Subscriber("/slam_out_pose",PoseStamped,self.rplidar_callback)               # 雷达订阅者节点 
        self.yolox_pub=rospy.Publisher("yolox_action",UInt8,queue_size=10)                                  # 识别指令发布者
        self.yolox_sub=rospy.Subscriber("yolox_data",PoseStamped,self.yolox_callback)                       # 识别结果订阅者
        self.own_position_pub=rospy.Publisher('/mavros/vision_pose/pose',PoseStamped,queue_size=10)         # 当前位置发布者
        self.aim_position_pub=rospy.Publisher('/mavros/setpoint_position/local',PoseStamped,queue_size=10)  # 飞行目标点发布者
        self.state_sub=rospy.Subscriber('/mavros/state',State,self.state_callback)                               # 无人机状态订阅者
        # 服务
        rospy.wait_for_service('/mavros/set_mode')                                                          # 确保服务可用
        self.set_mode_client = rospy.ServiceProxy('/mavros/set_mode', SetMode)                              # 飞行模式切换服务代理

    def state_callback(self,msg):                                                                           # 监听无人机是否已起飞
        if msg.armed:
            rospy.loginfo("无人机已正常起飞")
            self.state=True
        else:
            rospy.loginfo("无人机未起飞")

    def set_mode(self,mode):                                                                                # 设置无人机飞行模式
        try:
            response=self.set_mode_client(custom_mode=mode)
            if response.mode_sent:
                rospy.loginfo("Mode change to OFFBOARD successful")
            else:
                rospy.loginfo("Mode change failed")
        except rospy.ServiceException as e:
            rospy.logerr("Service call failed: %s" % e)
            
    def servo_start_pub(self,a):
        rospy.loginfo("now we catch the target!")
        self.servo_pub.publish(a)

    def shibie_pub(self,a):                      # 识别状态发布函数
        if a==1:                                 # 1代表开始识别
            for i in range(0,10):
                self.yolox_pub(1)
        if a==2:                                 # 2代表结束识别
            for i in range(0,10):
                self.yolox_pub(2)

    def rplidar_callback(self,msg):              # 激光雷达位姿数据订阅函数
        self.x = msg.pose.position.x             # 无人机当前的x位置
        self.y = msg.pose.position.y             # 无人机当前的y位置
        self.own_position_pub.publish(msg)       # 向飞控发布坐标信息

    def send_aim_posion(self,x,y,z):             # 发送目标点位置信息
        position=PoseStamped()
        position.header.stamp=rospy.Time.now()
        position.header.frame_id="map"
        position.pose.position.x=x               # 目标点的x坐标
        position.pose.position.y=y               # 目标点的y坐标
        position.pose.position.z=z               # 目标点的z坐标
        self.aim_position_pub.publish(position)

    def yolox_callback(self,msg):                # 识别数据订阅函数
        obj=msg.data.target                      # 识别出的物体类别
        x_p=msg.data.x_p                         # 物体的x偏移量
        y_p=msg.data.y_p                         # 物体的y偏移量

# 信号灯类
class Light():
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(24,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(26,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(28,GPIO.OUT,initial=GPIO.LOW)

    def ryg_lights(self,light):             # 信号灯指示函数
        if light==1:                        # 黄灯亮，代表雷达有数据出来，位姿数据正常
            GPIO.output(24,GPIO.HIGH)
        if light==2:                        # 绿灯亮，代表所有节点启动完毕，可以起飞
            GPIO.output(26,GPIO.HIGH)
        if light==3:                        # 红灯亮，代表识别有数据传出
            GPIO.output(28,GPIO.HIGH)

# 主函数
def main():
    mainnode=MainNode()
    #light=Light()
    mainnode.set_mode("OFFBOARD")
    while not rospy.is_shutdown(): 
        #mainnode.send_aim_posion(100,100,10)
        pass

if __name__=='__main__':
    main()