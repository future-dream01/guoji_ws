#!/usr/bin/env python3
# 无人机飞行主程序节点
# 整体任务逻辑：无人机整体上电->jetson自启 执行leida.sh脚本，激光雷达工作，提供位置信息 yolox识别节点启动准备 main节点执行 具备起飞条件，遥控器切OFFBOARD，无人机一键起飞
import rospy
import time
import serial                                           # UART串口通讯模块
import Jetson.GPIO as GPIO
from main.msg import Yolox_data,Yolox_action
from std_msgs.msg import UInt8
from mavros_msgs.srv import SetMode,CommandBool
from mavros_msgs.msg import State
from geometry_msgs.msg import PoseStamped,Twist
import tf 
from functools import partial

port='/dev/ttyTHS0'                                    # 串口端口,pin8(TXD)->P5(RXD) ； pin10(RXD)->P4(TXD)
baudrate=9600                                          # 波特率
timeout=1
position=[[3,2],[2,4],[4,1],[2,3],[4,4]]               # 靶标所在点[x,y]
target=[1,3,4]                                         # 要投递的目标编号
i=0                                                    # 已遍历点数
box=1                                                  # 需要投放的盒子编号

# 主节点类
class MainNode():
    def __init__(self):
        rospy.init_node("main",anonymous=True)
        # 属性
        self.x=self.y=self.z=0                                                                              # 初始化位置x，y，z,无人机当前自身所处的位置
        self.x_p=self.y_p=self.obj=6                                                                        # 初始化目标位置偏移x_p、y_p、物体类型
        self.rate=rospy.Rate(10)                                                                            # 频率
        self.takeoff_state=False                                                                            # 无人机是否起飞
        self.armed_state=False                                                                              # 无人机是否解锁
        self.mode="AUTO.LOITER"                                                                             # 无人机当前飞行模式 默认为定点模式
        self.timer=None                         # 定义定时器
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
        self.arm_plane_client = rospy.ServiceProxy('/mavros/setmode',CommandBool)                             # 无人机锁定函数
 
    # 无人机状态、模式监听函数
    def state_callback(self,msg):                                                                           
        if msg.armed:                       # 是否解锁
            rospy.loginfo("无人机已解锁")
            self.armed_state=True
        if not msg.armed:
            self.armed_state=False
            rospy.loginfo("无人机未解锁")
        self.mode=msg.mode                  # 获取当前的飞行模式
        rospy.loginfo(f"当前模式为:{msg.mode}")

    # 起飞状态监听函数
    def altitude_callback(self,msg):
        self.z=msg.pose.position.z
        if (self.z>=0.5):
            self.arm_takeoff=True
        else :
            self.arm_takeoff=False

    # 切换无人机飞行模式 最多重试10次
    def set_mode(self, mode):
        rospy.wait_for_service('/mavros/set_mode')
        max_retries = 10  # 设置最大重试次数
        retries = 0
        while retries < max_retries and not rospy.is_shutdown():
            try:
                response = self.set_mode_client(custom_mode=mode)   # 发送指定模式请求
                if response.mode_sent:
                    rospy.loginfo(f"模式成功切换为{mode}")
                    self.mode=mode                                  # 更新模式状态
                    break
                else:
                    retries += 1
                    rospy.logwarn(f"模式切换{mode}失败，正在重新尝试,尝试次数：({retries}/{max_retries})")
            except rospy.ServiceException as e:
                rospy.logerr(f"Service call failed: {e}")
                retries += 1
            self.rate.sleep()  # 避免过于频繁的请求
        if retries == max_retries:
            rospy.logerr(f"经过{max_retries}次尝试后，模式切换为{mode}失败")
    
    # 无人机锁桨函数
    def disarm(self):
        rospy.wait_for_service('/mavros/cmd/arming')
        max_retries=10
        retries = 0
        while retries < max_retries and not rospy.is_shutdown():
            try: 
                response = self.arm_plane_client(False)  # 发送锁桨命令
                if response.success:
                    rospy.loginfo("无人机锁桨成功")
                else:
                    rospy.logwarn(f"无人机锁桨失败，正在尝试重新锁桨,尝试次数：({retries}/{max_retries})")
                    retries += 1
            except rospy.ServiceException as e:
                rospy.logerr("Service call failed: %s" % e)
                retries += 1
            if retries == max_retries:
                rospy.logerr("锁桨失败")
            self.rate.sleep()       # 防止请求过快

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
        try:
            # 获取位置
            self.x = -msg.pose.position.x
            self.y = -msg.pose.position.y
            #self.z = msg.pose.position.z

            # 获取并转换方向
            orientation_q = msg.pose.orientation
            quaternion = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
            euler = tf.transformations.euler_from_quaternion(quaternion)
            roll = euler[0]
            pitch = euler[1]
            yaw = euler[2]

            # 将数据发布到 /mavros/vision_pose/pose
            pose = PoseStamped()
            pose.header.stamp = rospy.Time.now()
            pose.header.frame_id = "map"  # 确保 frame_id 与飞控期望的坐标系一致

            pose.pose.position.x = self.x
            pose.pose.position.y = self.y
            #pose.pose.position.z = self.z

            # 将欧拉角转换回四元数
            quaternion = tf.transformations.quaternion_from_euler(roll, pitch, yaw)
            pose.pose.orientation.x = quaternion[0]
            pose.pose.orientation.y = quaternion[1]
            pose.pose.orientation.z = quaternion[2]
            pose.pose.orientation.w = quaternion[3]

            self.own_position_pub.publish(pose)
            #rospy.loginfo("send")
        except Exception as e:
            rospy.logerr(f"rplidar_callback 发生错误: {e}")
        
    # 发现目标之后开始调整定位 (高度，超时时间)
    def shibie_move_fix(self,z,timeout=60):                                   
        #position=PoseStamped()
        start_time=rospy.Time.now().to_sec()
        x_now=self.x
        y_now=self.y
        #z_now=self.z
        while not rospy.is_shutdown():
            current_time=rospy.Time.now().to_sec()
            if (current_time-start_time)>=timeout:
                rospy.logwarn("识别微调过程超时，直接投递")
                break
            if (abs(self.x_p)<=30 and abs(self.y_p)<=30):
                rospy.loginfo("已经抵达目标中心点正上方，开始投递")
                break
            self.send_aim_posion(x_now+(self.x_p/1000),y_now+(self.y_p/1000),z)
            # position.header.stamp=rospy.Time.now()
            # position.header.frame_id="map"
            # position.pose.position.x=self.x+(self.x_p/1000)              # 目标点的x坐标
            # position.pose.position.y=self.y+(self.y_p/1000)              # 目标点的y坐标
            # position.pose.position.z=z                                   # 目标点的z坐标
            # self.aim_position_pub.publish(position)
            self.rate.sleep()
            rospy.loginfo(f"目标为{self.obj} \n 识别中,正在调整位置 \n x_p:{self.x_p} \n y_p:{self.y_p}")

    # 发送目标点位置信息(x坐标，y坐标，z坐标，最大执行时间)
    def send_aim_posion(self,x,y,z,timeout=40):                               
        position=PoseStamped()
        start_time=rospy.Time.now().to_sec()

        while not rospy.is_shutdown():
            current_time=rospy.Time.now().to_sec()
            if (current_time-start_time)>=timeout:
                rospy.logwarn("前往目标点过程超时")
                break
            if (abs(self.x-x)<=0.05 and abs(self.y-y)<=0.05):
                rospy.loginfo("已到达目标点")
                break
            position.header.stamp=rospy.Time.now()
            position.header.frame_id="map"
            position.pose.position.x=x                             # 目标点的x坐标
            position.pose.position.y=y                             # 目标点的y坐标
            position.pose.position.z=z                             # 目标点的z坐标
            self.aim_position_pub.publish(position)
            rospy.loginfo(f"正在飞往指定点({x},{y},{z})")
            self.rate.sleep()

    # 自动起飞（目标高度，最大执行时间）
    def auto_takeoff(self, altitude, timeout=40):
        position = PoseStamped()
        start_time = rospy.Time.now().to_sec()
        #rospy.loginfo("模式成功切换为OFFBOARD")
        
        while not rospy.is_shutdown():
            #self.set_mode("OFFBOARD")
            current_time = rospy.Time.now().to_sec()
            if (current_time - start_time) > timeout:           # 检查是否超时
                rospy.logwarn("起飞所用时间超时")
                break
            if abs(self.z - altitude) <= 0.05:  # 更严格的高度检查
                rospy.loginfo("成功起飞")
                break
            position.header.stamp = rospy.Time.now()
            position.header.frame_id = "map"
            position.pose.position.x = 0
            position.pose.position.y = 0
            position.pose.position.z = altitude
            self.aim_position_pub.publish(position)
            rospy.loginfo("正在起飞……")
            self.rate.sleep()  # 控制发布频率

    # 全局悬停函数
    def hover(self,x,y,z,time):
        position = PoseStamped()
        start_time = rospy.Time.now().to_sec()          # 开始时间                                
        while not rospy.is_shutdown():
            #self.set_mode("OFFBOARD")
            current_time = rospy.Time.now().to_sec()    # 此刻时间
            if (current_time - start_time) >= time:   # 检查是否超时
                rospy.loginfo("悬停时间已到")
                break
            position.header.stamp = rospy.Time.now()
            position.header.frame_id = "map"
            position.pose.position.x = x
            position.pose.position.y = y
            position.pose.position.z = z
            self.aim_position_pub.publish(position)
            rospy.loginfo("正在悬停……")
            self.rate.sleep()  # 控制发布频率
    

    # 定时器回调函数
    def timer_callback(self, x_now, y_now, z_now, event):
        position = PoseStamped()
        position.header.stamp = rospy.Time.now()
        position.header.frame_id = "map"
        position.pose.position.x = x_now
        position.pose.position.y = y_now
        position.pose.position.z = z_now
        self.aim_position_pub.publish(position)
        rospy.loginfo("正在进行并行任务悬停……")

    # 并行任务状态悬停函数(1:开始悬停，2结束悬停)
    def stay(self,a):
        if a==1:
            x_now=self.x        # 获取当前坐标
            y_now=self.y
            z_now=self.z
            self.timer=rospy.Timer(rospy.Duration(0.1),partial(self.timer_callback, x_now, y_now, z_now)) # 定住函数
        if a==2:
            self.timer.shutdown()


    # 识别数据订阅函数
    def yolox_callback(self,msg):                                  
        self.obj=msg.target                                        # 识别出的物体类别
        self.x_p=msg.y_p                                           # 物体的x偏移量
        self.y_p=-msg.x_p                                          # 物体的y偏移量


    # 着陆函数
    def land(self,x,y):
        while not(self.z<=0.25):
            self.send_aim_posion(x,y,0.18)                          # 发送降落目标点
        while self.armed_state:                                     # 如果是解锁状态
            self.disarm()                                           # 锁桨
        

        

# 信号灯类
class Mark():
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(11,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(12,GPIO.OUT,initial=GPIO.LOW)

    def marking(self,i):                                       # 信号灯指示函数
        if i==1:                                               # 
            GPIO.output(7,GPIO.HIGH)
        if i==2:                                               # 
            GPIO.output(11,GPIO.HIGH)
            rospy.sleep(0.5)
            GPIO.output(11,GPIO.LOW)
        if i==3:                                               # 
           GPIO.output(12,GPIO.HIGH)

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
def shibie_toudi(main_node,servo,mark):                                                          
    global i,box,target
    if main_node.obj==6:                                # 如果没有目标 则要动一动，直到超时或者再次有目标
        position = PoseStamped()
        x_now=main_node.x                               # 获取此刻坐标
        y_now=main_node.y
        z_now=main_node.z
        start_time = rospy.Time.now().to_sec()          # 开始时间
        while not rospy.is_shutdown():
            current_time = rospy.Time.now().to_sec()    # 此刻时间
            if (current_time-start_time)>=15:           # 超时退出
                break
            if main_node.obj!= 6:                       # 有目标了退出
                rospy.loginfo(f"找到了，目标为{main_node.obj}……")
                break
            position.header.stamp = rospy.Time.now()
            position.header.frame_id = "map"
            position.pose.position.x = x_now+0.2
            position.pose.position.y = y_now+0.2
            position.pose.position.z = z_now
            rospy.loginfo("正在该点附近搜索目标……")
    if main_node.obj in target:         # 找到了目标
        main_node.stay(1)               # 并行任务悬停开始
        mark.marking()                  # 蜂鸣器提示
        main_node.stay(2)               # 并行任务悬停结束
        target.remove(main_node.obj)    # 从目标列表中移除当前目标
        main_node.shibie_move_fix(1)    # 开始投递前的修正
        servo.servo_start(box)          # 投递
        box+=1                          # 需要投放的盒子编号+1
        main_node.stay(1)               # 并行任务悬停开始
        rospy.sleep(3)                  # 确保货物落下来
        main_node.stay(2)               # 并行任务悬停结束
        rospy.loginfo("完成投递")
        i+=1                            # 已经去过的点的数量+1
    else:
        i+=1                            # 已经去过的点的数量+1

# 主函数
def main():
    main_node=MainNode()
    servo=UART(port, baudrate,timeout)
    mark=Mark()
    mark.marking(2)
    
   # main_node.shibie_pub(1)
    
    while not rospy.is_shutdown(): 
        #rospy.loginfo(f"物体为：{main_node.obj}\n x偏移量:{main_node.x_p}\n y偏移量:{main_node.y_p}")
        if (main_node.armed_state):

            ######### 测试1: 测试自动降落
            main_node.auto_takeoff(0.5)
            main_node.hover(0 , 0 , 0.5 ,10)
            main_node.land(0 , 0 )
            #########

            ######### 测试2:测试并行悬停指令和舵机
            main_node.auto_takeoff(0.5)
            main_node.hover(0 , 0 , 0.5,10)
            main_node.stay(1)                   # 并行任务悬停开始
            main_node.servo_start(1)            
            rospy.sleep(1)
            main_node.servo_start(2)            
            rospy.sleep(1)
            main_node.servo_start(3)            
            main_node.stay(2)                   # 并行任务悬停结束
            main_node.send_aim_posion(0 , 1 , 0.5)
            main_node.land(0 , 1 )
            #########

            ######### 测试3: 测试画矩形
            main_node.auto_takeoff(0.5)
            main_node.hover(0 , 0 , 0.5 ,10)
            main_node.send_aim_posion(0 , 2 , 0.5)
            main_node.send_aim_posion(2 , 2 , 0.5)
            main_node.send_aim_posion(2 , 0 , 0.5)
            main_node.send_aim_posion(0 , 0 , 0.5)
            main_node.land(0 , 0 )
            #########

            # 需先标定

            ######### 测试4:测试目标识别
            main_node.auto_takeoff(1)
            main_node.hover(0 , 0 , 1 ,10)
            main_node.send_aim_posion(2 , 2 , 1)
            main_node.stay(1)                   # 并行任务悬停开始
            main_node.shibie_pub(1)        
            rospy.sleep(3)
            main_node.stay(2)                   # 并行任务悬停结束
            main_node.send_aim_posion(0 , 1 , 0.5)
            shibie_toudi(main_node,servo,mark)
            main_node.land(0 , 1 )


            #########







            break

if __name__=='__main__':
    main()