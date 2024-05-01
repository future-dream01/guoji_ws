#!/usr/bin/env python3
# 无人机飞行主程序节点

import rospy
import time
import serial                                           # UART串口通讯模块
#import Jetson.GPIO as GPIO
from main.msg import Yolox_data,Yolox_action
from std_msgs.msg import UInt8
from mavros_msgs.srv import SetMode
from mavros_msgs.msg import State
from geometry_msgs.msg import PoseStamped,Twist

port='/dev/ttyTHS0'                                    # 串口端口,pin8(TXD)->P5(RXD) ； pin10(RXD)->P4(TXD)
baudrate=9600                                          # 波特率
timeout=1
position=[[3,2],[2,4],[4,1],[2,3],[4,4]]               # 靶标所在点
i=0                                                    # 已遍历点数
tim=0
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
        self.yolox_pub=rospy.Publisher("yolox_action",Yolox_action,queue_size=10)                                  # 识别指令发布者
        self.yolox_sub=rospy.Subscriber("yolox_data",Yolox_data,self.yolox_callback)                       # 识别结果订阅者
        self.own_position_pub=rospy.Publisher('/mavros/vision_pose/pose',PoseStamped,queue_size=10)         # 当前位置发布者
        self.aim_position_pub=rospy.Publisher('/mavros/setpoint_position/local',PoseStamped,queue_size=10)  # 飞行目标点发布者
        self.shibie_move_pub=rospy.Publisher('/mavros/setpoint_position/local',PoseStamped,queue_size=10)   # 识别到目标之后调整位置
        self.state_sub=rospy.Subscriber('/mavros/state',State,self.state_callback)                          # 无人机状态订阅者
        # 服务
        #rospy.wait_for_service('/mavros/set_mode')                                                          # 确保服务可用
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
            
    def shibie_pub(self,a):                                        # 识别状态发布函数
        global tim
        act=Yolox_action()
        tim=time.time()                                           # 记录当前时间
        if a==1:                                                  # 1代表开始识别
            act.action=1 
            for i in range(0,10):
                self.yolox_pub.publish(act)
                #rospy.loginfo(act)
                self.rate.sleep()
                
        if a==2:                                                   # 2代表结束识别
            act.action=2 
            for i in range(0,10):
                self.yolox_pub.publish(act)
                self.rate.sleep()

    def rplidar_callback(self,msg):                                # 激光雷达位姿数据订阅函数
        self.x = msg.pose.position.x                               # 无人机当前的x位置
        self.y = msg.pose.position.y                               # 无人机当前的y位置
        self.own_position_pub.publish(msg)                         # 向飞控发布坐标信息

    def shibie_move_fix(self,z):                                   # 发现目标之后开始调整定位，需给定高度
        position=PoseStamped()
        while not ((-70<=(self.x_p)<=70) and(70<=(self.y_p)<=70) ):
            position.header.stamp=rospy.Time.now()
            position.header.frame_id="map"
            position.pose.position.x=self.x+self.x_p               # 目标点的x坐标
            position.pose.position.y=self.y+self.y_p               # 目标点的y坐标
            position.pose.position.z=z                             # 目标点的z坐标
            self.aim_position_pub.publish(position)

        
    def send_aim_posion(self,x,y,z):                               # 发送目标点位置信息
        position=PoseStamped()
        while not ((-0.1<=(self.x-x)<=0.1) and(-0.1<=(self.y-y)<=0.1)) :
            position.header.stamp=rospy.Time.now()
            position.header.frame_id="map"
            position.pose.position.x=x                             # 目标点的x坐标
            position.pose.position.y=y                             # 目标点的y坐标
            position.pose.position.z=z                             # 目标点的z坐标
            self.aim_position_pub.publish(position)

    def yolox_callback(self,msg):                                  # 识别数据订阅函数
        global tim
        tim2=time.time()
        fps=1/(tim2-tim)                                         # 计算fps
        obj=msg.target                                        # 识别出的物体类别
        x_p=msg.x_p                                           # 物体的x偏移量
        y_p=msg.y_p                                           # 物体的y偏移量
        tim =tim2
        rospy.loginfo(f"obj: {obj} \n x_p:{x_p} \n y_p:{y_p} \n fps: {fps}")   # 日志

# 信号灯类
#class Light():
    #def __init__(self):
        #GPIO.setmode(GPIO.BOARD)
        #GPIO.setup(24,GPIO.OUT,initial=GPIO.LOW)
        #GPIO.setup(26,GPIO.OUT,initial=GPIO.LOW)
        #GPIO.setup(28,GPIO.OUT,initial=GPIO.LOW)

    #def ryg_lights(self,light):                                    # 信号灯指示函数
        #if light==1:                                               # 黄灯亮，代表雷达有数据出来，位姿数据正常
            #GPIO.output(24,GPIO.HIGH)
        #if light==2:                                               # 绿灯亮，代表所有节点启动完毕，可以起飞
            #GPIO.output(26,GPIO.HIGH)
       # if light==3:                                               # 红灯亮，代表识别有数据传出
           # GPIO.output(28,GPIO.HIGH)

#串口通信类
class UART(serial.Serial):                       
    def __init__(self, port, baudrate,timeout):
        super(UART, self).__init__(port=port, baudrate=baudrate, timeout=timeout)

    def servo_start(self,a):                # 舵机开始运动,a=1:投第一个货物；a=2:投第二个货物;a=3:投第三个货物
        for i in range(0,10): 
            command = a.to_bytes(1, 'little')             
            self.write(command)
            rospy.sleep(0.1)

# 识别投递功能函数
def shibie_toudi(main_node,servo):                                                          
    global i
    if main_node.obj==1 or main_node.obj==2 or main_node.obj==5 :
        main_node.shibie_move_fix(1)
        servo.servo_start(1)
        rospy.sleep(2)
        i+=1
    if main_node.obj==0:
        pass
    else:
        i+=1
        
# 主函数

def main():
    b=0
    main_node=MainNode()
    servo=UART(port, baudrate,timeout)
    #light=Light()
    #main_node.shibie_pub(1)
    #rospy.sleep(15)
    servo.servo_start(1)
    while not rospy.is_shutdown(): 
        pass
        # if main_node.state:                                                     # 确定无人机是起飞状态
        #     main_node.set_mode("OFFBOARD")                                      # 将无人机飞行模式切换到OFFBOARD，由ros程序控制
        #     time.sleep(1)
        #     main_node.send_aim_posion(position[i][0],position[i][1],1)          # 前往指定点
        #     main_node.shibie_pub(1)                                             # 开始识别
        #     time.sleep(4)                                                       # 等待识别开始出结果
        #     shibie_toudi(main_node,servo)                                       # 投递函数
   # main_node.shibie_pub(2)

if __name__=='__main__':
    main()