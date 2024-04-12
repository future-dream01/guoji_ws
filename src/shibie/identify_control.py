#!/usr/bin/env python

import rospy
import time
from shibie.srv import Identify, IdentifyRequest
from std_msgs.msg import String


def target_identify():
    """向服务器发出信号并接收识别结果"""
    # ROS节点初始化
    rospy.init_node("target_identify")

    #发现identify_server服务，创建客户端，连接服务
    rospy.wait_for_service('identify_server')
    try:
        add_ide = rospy.ServiceProxy('identify_server', Identify)
        # 请求服务调用，输入请求数据
        response = add_ide("1")
        return response

    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)


if __name__ == "__main__":
    # 服务器调用并显示结果
    # t1 = time.perf_counter()
    response = target_identify()
    # t2 = time.perf_counter()


