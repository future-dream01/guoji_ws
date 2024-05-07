#!/usr/bin/env python

import time
from demo import *
from shibie.msg import Yolox_action, Yolox_data
import rospy
import cv2
from loguru import logger
action_judge = False


def pre_ide_func():
    # 准备识别
    global cap, vid_writer
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


def identifyCallback(call):
    # 回调函数
    global action_judge
    if call.action == 1:
        action_judge = True
    else:
        action_judge = False



def identify_processor(predictor, vis_folder, args):
    """接收客户端信号，提供识别服务"""
    global cap, vid_writer
    # 初始化ROS节点
    rospy.init_node('identify_node')
    pre_ide_func()

    identify_data_pub = rospy.Publisher('yolox_data', Yolox_data, queue_size = 10)
    data_back = Yolox_data()

    # 创建针对控制节点的订阅者
    rospy.Subscriber('yolox_action', Yolox_action, identifyCallback)
    state_check = 0
    x_pos, y_pos, obj = 0, 0, 6
    while state_check == 0 or state_check == 1:
        while action_judge:         # 判断是否进识别程序段
            state_check = 1
            # x_pos,y_pos,obj=0,0,6
            ret_val, frame = cap.read()
            if ret_val:
                outputs, img_info = predictor.inference(frame)
                result_frame,x_ps,y_ps,obj = predictor.visual(outputs[0], img_info, predictor.confthre)
                if args.save_result:
                    vid_writer.write(result_frame)
                else:
                    cv2.namedWindow("yolox", cv2.WINDOW_NORMAL)
                    cv2.imshow("yolox", result_frame[0])
                ch = cv2.waitKey(1)
                if  not action_judge:
                    state_check = 2
                    break
                if ch == 27 or ch == ord("q") or ch == ord("Q"):
                    break
            else:
                break

            if obj != 6:
                x_pos = x_ps
                y_pos = y_ps
            data_back.target = int(obj)
            data_back.x_p = x_pos
            data_back.y_p = y_pos
            identify_data_pub.publish(data_back)
        #time.sleep(0.1)
        if state_check == 2:
            break


if __name__ == "__main__":
    args = make_parser().parse_args()
    exp = get_exp(args.exp_file, args.name)
    predictor, vis_folder = pre_main(exp, args)
    identify_processor(predictor, vis_folder, args)
    # print("AAA")
