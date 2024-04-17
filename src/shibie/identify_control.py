#!/usr/bin/env python

import rospy
import time
from shibie.msg import Yolox_action, Yolox_data
action_judge = True
back_judge = False


def identify_data_callback(msg):
    # 接受并输出识别结果
    global back_judge
    rospy.loginfo(f"Taregt:{msg.target} \n X_postion:{msg.x_p} \n Y_postion:{msg.y_p}")
    back_judge = True


def back_judge_control(msg):
    # 接受并输出识别结果
    global back_judge
    back_judge = True



def identify_call():
    # 向服务器发出信号并接收识别结果

    """
    此处定义全局变量action_bool，用于控制接收循环是否停止，
    当主程序判定循环应当停止时，更改action_bool为False，则该节点停止订阅yolox_back的内容，并向identify_node发出停止的信号。
    """
    global action_judge, back_judge

    # ROS节点初始化
    rospy.init_node("identify_control")
    #创建名为identify_control的Publisher，发布名为yolox_call的topic, 消息类型为Yolox_action，队列长度为5
    identify_control = rospy.Publisher('yolox_call', Yolox_action, queue_size = 5)
    print("checkpoint1")
    control_cmd = Yolox_action()
    control_cmd.action = 1
    print("checkpoint2")
    while not back_judge:
        identify_control.publish(control_cmd)
        rospy.Subscriber('yolox_back', Yolox_data, back_judge_control)
        

    t1 = time.perf_counter()
    while action_judge:
        rospy.Subscriber('yolox_back', Yolox_data, identify_data_callback)

        t2 = time.perf_counter()
        if (t2 - t1) >= 60:
            action_judge = False
        rospy.spin()

    # 跳出循环后，发布停止消息
    control_cmd.action = 0
    identify_control.publish(control_cmd)


if __name__ == "__main__":
    # 服务器调用并显示结果
    # t1 = time.perf_counter()
    identify_call()
    # t2 = time.perf_counter()