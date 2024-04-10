#!/usr/bin/env python

# import sys
# import threading
import time
from demo import *
from shibie.srv import Identify, IdentifyResponse
from std_msgs.msg import String
import rospy 


pubCommand = False
# ide_pub = rospy.Publisher('')


def command_thread():
    """单词循环线程"""
    while True:
        if pubCommand:
            vel_msg = String()
    
        time.sleep(0.05)
        

def identifyCallback(call):
    """回调函数"""
    # 显示请求数据
    rospy.loginfo("Publish command!")
    
    """
    if call != "1":
        return Identify(7, -1, -1)
    """

    # 调用demo.py识别图片
    obj_response,x_p,y_p = main(predictor, vis_folder, args)

    #x_pos_res = 0
    #y_pos_res = 0
    """
    x_pos = str(round(x_pos_res, 2) * 100)
    y_pos = str(round(y_pos_res, 2) * 100)
    target_info = ','.join([obj_response, x_pos, y_pos])
    """
    #print(f"target:{obj_response}\n x_pos:{x_pos_res}\n y_pos:{y_pos_res}")
    # 反馈数据
    return IdentifyResponse(int(obj_response), x_p, y_p)
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
