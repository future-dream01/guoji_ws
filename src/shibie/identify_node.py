#!/usr/bin/env python

# import sys
# import threading
import time
from demo import *
from shibie.srv import Identify, IdentifyResponse
from shibie.msg import Result
from std_msgs.msg import String
import rospy 


def identifyCallback(call):
    """回调函数"""
    # 显示请求数据
    rospy.loginfo("Publish command!")

    # 调用demo.py识别图片
    obj_response,x_p,y_p = main(predictor, vis_folder, args)

    # print(f"target:{obj_response}\n x_pos:{x_p}\n y_pos:{y_p}")
    
    # 创建发布者并发布数据
    result_pub = rospy.Publisher('identify_result', Result, queue_size=10)
    
    
    # 反馈数据
    return IdentifyResponse("1")
    # return IdentifyResponse(2, 0, 0)

def identify_server(predictor, vis_folder, args):
    """接收客户端信号，提供识别服务"""
    # 初始化ROS节点
    rospy.init_node('identify_server')

    # 创建名为identify_server的服务器，注册回调函数identifyCallback
    ide_server = rospy.Service('identify_server', Identify, identifyCallback)

    # 循环等待回调函数
    print("Ready to receive identification")
    # t = threading.Thread(target=command_thread)
    rospy.spin()


if __name__ == "__main__":
    args = make_parser().parse_args()
    exp = get_exp(args.exp_file, args.name)
    predictor, vis_folder = pre_main(exp, args)
    identify_server(predictor, vis_folder, args)
