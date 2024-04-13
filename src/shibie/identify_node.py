#!/usr/bin/env python

# import sys
# import threading
import time
from demo import *
from shibie.msg import Result
# from std_msgs.msg import String
import rospy
import cv2
from loguru import logger

"""
def identifyCallback(call):
    # 回调函数
    # 显示请求数据
    rospy.loginfo("Publish command!")

    # 调用demo.py识别图片
    obj_response, x_p, y_p = main(predictor, vis_folder, args)
    # print(f"target:{obj_response}\n x_pos:{x_p}\n y_pos:{y_p}")
    
    # 创建发布者并发布数据
    result_pub = rospy.Publisher('identify_result', Result, queue_size=10)
"""


def identify_server(predictor, vis_folder, args):
    """接收客户端信号，提供识别服务"""
    # 初始化ROS节点
    rospy.init_node('identify_server')

    # 创建针对识别结果数据信息的发布者节点
    identify_info_pub = rospy.Publisher('identify_info', Result, queue_size=10)

    current_time = time.localtime()
    cap = cv2.VideoCapture(args.path if args.demo == "video" else args.camid)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float
    fps = cap.get(cv2.CAP_PROP_FPS)
    if args.save_result:
        save_folder = os.path.join(
            vis_folder, time.strftime("%Y_%m_%d_%H_%M_%S", current_time)
        )
        os.makedirs(save_folder, exist_ok=True)
        if args.demo == "video":
            save_path = os.path.join(save_folder, args.path.split("/")[-1])
        else:
            save_path = os.path.join(save_folder, "camera.mp4")
        logger.info(f"video save_path is {save_path}")
        vid_writer = cv2.VideoWriter(
            save_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (int(width), int(height))
        )

    judge = True
    while judge:
        ret_val, frame = cap.read()
        if ret_val:
            outputs, img_info = predictor.inference(frame)
            result_frame = predictor.visual(outputs[0], img_info, predictor.confthre)
            if args.save_result:
                vid_writer.write(result_frame)
            else:
                cv2.namedWindow("yolox", cv2.WINDOW_NORMAL)
                cv2.imshow("yolox", result_frame[0])
            ch = cv2.waitKey(1)
            if ch == 27 or ch == ord("q") or ch == ord("Q"):
                break
        else:
            break
        identify_result = Result()
        identify_result.target = obj
        identify_result.x_p = x_p
        identify_result.y_p = y_p


if __name__ == "__main__":
    args = make_parser().parse_args()
    exp = get_exp(args.exp_file, args.name)
    predictor, vis_folder = pre_main(exp, args)
    identify_server(predictor, vis_folder, args)
    # print("AAA")
