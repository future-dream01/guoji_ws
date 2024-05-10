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
        self.x=self.y=self.z=0                                                                              # 初始化位置x，y，z
        self.x_p=self.y_p=self.obj=0                                                                        # 初始化目标位置偏移x_p、y_p、物体类型
        self.rate=rospy.Rate(10)                                                                            # 频率
        self.takeoff_state=False                                                                            # 无人机是否起飞
        self.armed_state=False                                                                              # 无人机是否解锁
        self.is_landing=False                                                                               # 是否正在着陆
        self.is_offboard=False                                                                              # 是否已经切换到offboard模式
        # 话题
        self.servo_pub=rospy.Publisher("servo_action",UInt8,queue_size=10)                                  # 舵机发布者节点
        self.rplidar_sub=rospy.Subscriber("/slam_out_pose",PoseStamped,self.rplidar_callback)               # 雷达订阅者节点 
        self.yolox_pub=rospy.Publisher("yolox_action",Yolox_action,queue_size=10)                           # 识别指令发布者
        self.yolox_sub=rospy.Subscriber("yolox_data",Yolox_data,self.yolox_callback)                        # 识别结果订阅者
        self.own_position_pub=rospy.Publisher('/mavros/vision_pose/pose',PoseStamped,queue_size=10)         # 当前位置发布者
        self.aim_position_pub=rospy.Publisher('/mavros/setpoint_position/local',PoseStamped,queue_size=10)  # 飞行目标点发布者
        self.shibie_move_pub=rospy.Publisher('/mavros/setpoint_position/local',PoseStamped,queue_size=10)   # 识别到目标之后调整位置
        self.own_altitude_sub=rospy.Subscriber('/mavros/local_position/pose',PoseStamped,self.altitude_callback)
        self.state_sub=rospy.Subscriber('/mavros/state',State,self.state_callback)                          # 无人机状态订阅者
        # 服务
        self.set_mode_client = rospy.ServiceProxy('/mavros/set_mode', SetMode)                              # 飞行模式切换服务代理

    # 无人机状态监听函数
    def state_callback(self,msg):                                                                           
        if msg.armed:                       # 是否解锁
            rospy.loginfo("无人机已解锁")
            self.armed_state=True
        if not msg.armed:
            self.armed_state=False
            rospy.loginfo("无人机未解锁")
        if msg.mode=="OFFBOARD":            # 是否切换到OFFBOARD模式
            self.is_offboard=True
        if not msg.mode=="OFFBOARD":
            self.is_offboard=False

    # 起飞状态监听函数
    def altitude_callback(self,msg):
        self.z=msg.pose.positoion.z
        if (self.z>=0.5):
            self.arm_takeoff=True
            rospy.loginfo("无人机已起飞")
        else :
            self.arm_takeoff=False
            rospy.loginfo("无人机未起飞")

    # 设置无人机飞行模式
    def set_mode(self,mode):                                                                               
        rospy.wait_for_service('/mavros/set_mode')
        try:
            response=self.set_mode_client(custom_mode=mode)
            if response.mode_sent:
                rospy.loginfo(f"Mode change to {mode} successful")
                if mode =="AUTO.LAND":
                    self.is_landing==True
            else:
                rospy.loginfo("Mode change failed")
        except rospy.ServiceException as e:
            rospy.logerr("Service call failed: %s" % e)

    # 识别状态发布函数
    def shibie_pub(self,a):                                        
        global tim
        act=Yolox_action()
        tim=time.time()                                           # 记录当前时间
        if a==1:                                                  # 1代表开始识别
            act.action=1 
            for i in range(0,10):
                self.yolox_pub.publish(act)
                self.rate.sleep()
        if a==2:                                                   # 2代表结束识别
            act.action=2 
            for i in range(0,10):
                self.yolox_pub.publish(act)
                self.rate.sleep()

    # 激光雷达位姿数据订阅函数+坐标变换
    def rplidar_callback(self,msg):                                
        vision_pose_msg = PoseStamped()
        
        # 设置时间戳和帧ID
        vision_pose_msg.header.stamp = rospy.Time.now()
        vision_pose_msg.header.frame_id = "map"  # 确保与飞控的参考帧一致
        
        # 重新映射坐标
        vision_pose_msg.pose.position.x = -msg.pose.position.y  # 无人机当前的x位置
        vision_pose_msg.pose.position.y = msg.pose.position.x   # 无人机当前的y位置
        vision_pose_msg.pose.position.z = msg.pose.position.z   # 无人机当前的z位置
        
        # 保持姿态信息
        vision_pose_msg.pose.orientation = msg.pose.orientation
        
        # 发布到 /mavros/vision_pose/pose
        self.own_position_pub.publish(vision_pose_msg)
        
    # 发现目标之后开始调整定位，需给定高度
    def shibie_move_fix(self,z):                                   
        position=PoseStamped()
        while not ((-70<=(self.x_p)<=70) and(70<=(self.y_p)<=70) ):
            position.header.stamp=rospy.Time.now()
            position.header.frame_id="map"
            position.pose.position.x=self.x+self.x_p               # 目标点的x坐标
            position.pose.position.y=self.y+self.y_p               # 目标点的y坐标
            position.pose.position.z=z                             # 目标点的z坐标
            self.aim_position_pub.publish(position)

    # 发送目标点位置信息
    def send_aim_posion(self,x,y,z):                               
        position=PoseStamped()
        while not ((-0.1<=(self.x-x)<=0.1) and(-0.1<=(self.y-y)<=0.1)) :
            position.header.stamp=rospy.Time.now()
            position.header.frame_id="map"
            position.pose.position.x=x                             # 目标点的x坐标
            position.pose.position.y=y                             # 目标点的y坐标
            position.pose.position.z=z                             # 目标点的z坐标
            self.aim_position_pub.publish(position)

    # 自动起飞
    def auto_takeoff(self,a):
        position=PoseStamped()
        while not (-0.1<=(self.z-a)<=0.1):
            position.header.stamp=rospy.Time.now()
            position.header.frame_id="map"
            position.pose.position.x=0                             # 目标点的x坐标
            position.pose.position.y=0                             # 目标点的y坐标
            position.pose.position.z=a                             # 目标点的z坐标
            self.aim_position_pub.publish(position)

    # 识别数据订阅函数
    def yolox_callback(self,msg):                                  
        global tim
        tim2=time.time()
        fps=1/(tim2-tim)                                      # 计算fps
        obj=msg.target                                        # 识别出的物体类别
        x_p=msg.x_p                                           # 物体的x偏移量
        y_p=msg.y_p                                           # 物体的y偏移量
        tim =tim2
        rospy.loginfo(f"obj: {obj} \n x_p:{x_p} \n y_p:{y_p} \n fps: {fps}")   # 日志

    # 着陆函数
    def land(self):
        while not self.is_landing:
            self.set_mode("AUTO.LAND")
        while self.armed_state:
            rospy.loginfo("the plane is landing……")
        rospy.loginfo("the plane landed and poweroffed successfully")

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

    # 舵机运动函数（a=1投第一个货物；a=2投第二个货物;a=3投第三个货物）
    def servo_start(self,a):                
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
    main_node=MainNode()
    servo=UART(port, baudrate,timeout)
    #light=Light()
    #main_node.shibie_pub(1)
    #rospy.sleep(15)
    #servo.servo_start(2)
    while not rospy.is_shutdown(): 
        print(f"当前坐标：\n x:{main_node.x}\n y:{main_node.y}\n z:{main_node.z}")
        #if (main_node.armed_state) and (main_node.is_offboard):                      # 确定无人机是否解锁、切换到OFFBOARD模式
            #main_node.auto_takeoff(0.5)                                              # 一键起飞，设置起飞高度
            #main_node.set_mode("OFFBOARD") 
            #main_node.send_aim_posion(0,0,1)
            #rospy.sleep(10)
            #while not rospy.is_shutdown():
                #main_node.set_mode("OFFBOARD")                                      # 将无人机飞行模式切换到OFFBOARD，由ros程序控制
                #main_node.send_aim_posion(position[i][0],position[i][1],1)          # 前往指定点（）
            #main_node.send_aim_posion(2,2,0.5)                                       # 前往指定点（x,y,z）
            #main_node.land()                                                         # 自动着陆
            #break
                #main_node.shibie_pub(1)                                             # 开始识别
                #time.sleep(4)                                                       # 等待识别开始出结果
                #shibie_toudi(main_node,servo)                                       # 投递函数
    #main_node.shibie_pub(2)

if __name__=='__main__':
    main()