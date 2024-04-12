#!/usr/bin/env python3

# 无人机飞行主程序节点
import rospy
from std_msgs.msg import UInt8
from geometry_msgs.msg import PoseStamped

x,y=0,0     # 初始化位置x，y
# 主程序节点
class MainNode():
    def __init__(self):
        rospy.init_node("main",anonymous=True)
        self.servo_pub=rospy.Publisher("servo_move",UInt8,queue_size=10)                    # 舵机发布者节点
        self.rplidar_sub=rospy.Subscriber("/slam_out_pose",PoseStamped,self.Rp_callback)    # 雷达订阅者节点 
        self.rate=rospy.Rate(10)
    
    def servo_start_pub(self,a):
        rospy.loginfo("now we catch the target!")
        self.servo_pub.publish(a)


    def Rp_callback(self,msg):
        #rospy.loginfo("Robot's Position: %s" % str(msg.pose))
         
        global x,y
        x = msg.pose.position.x
        y = msg.pose.position.y
        pass
    

# 主函数
def main():
    mainnode=MainNode()
    while not rospy.is_shutdown(): 
        #mainnode.servo_start_pub()
        #rospy.loginfo("Robot's Position: %s" % str(msg.pose))
        if x<=1:
            mainnode.servo_start_pub(int(x))
        pass

main()
