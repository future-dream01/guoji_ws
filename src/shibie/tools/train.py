#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (c) Megvii, Inc. and its affiliates.

import argparse
import random
import warnings
from loguru import logger

import torch
import torch.backends.cudnn as cudnn
import torch
import sys
sys.path.append("E:/vscodeProject/guojisai")
from yolox.core import Trainer, TrainerWithTeacher,launch
from yolox.exp import get_exp
from yolox.utils import configure_module, configure_nccl, configure_omp, get_num_devices

from teacher.teacher_model import Teacher


def make_parser():
    parser = argparse.ArgumentParser("YOLOX train parser")
    parser.add_argument("-expn", "--experiment-name", type=str, default=None)
    parser.add_argument("-n", "--name", type=str, default=None, help="model name")

    # distributed
    parser.add_argument(
        "--dist-backend", default="nccl", type=str, help="distributed backend"
    )
    parser.add_argument(
        "--dist-url",
        default=None,
        type=str,
        help="url used to set up distributed training",
    )
    parser.add_argument("-b", "--batch-size", type=int, default=64, help="batch size")
    parser.add_argument(
        "-d", "--devices", default=None, type=int, help="device for training"
    )
    parser.add_argument(
        "-f",
        "--exp_file",
        default=None,
        type=str,
        help="plz input your experiment description file",
    )
    parser.add_argument(
        "--resume", default=False, action="store_true", help="resume training"
    )
    parser.add_argument("-c", "--ckpt", default=None, type=str, help="checkpoint file")
    parser.add_argument(
        "-e",
        "--start_epoch",
        default=None,
        type=int,
        help="resume training start epoch",
    )
    parser.add_argument(        
        "--num_machines", default=1, type=int, help="num of node for training"
    )                                                               # 训练的计算机数量
    parser.add_argument(
        "--machine_rank", default=0, type=int, help="node rank for multi-node training"
    )
    parser.add_argument(
        "--fp16",
        dest="fp16",
        default=False,
        action="store_true",
        help="Adopting mix precision training.",
    )
    parser.add_argument(
        "--cache",
        dest="cache",
        default=False,
        action="store_true",
        help="Caching imgs to RAM for fast training.",
    )
    parser.add_argument(
        "-distill",
        "--distillation",
        dest="distillation",
        default=False,
        action="store_true",
        help="Use distillation.",
    )
    parser.add_argument(
        "-o",
        "--occupy",
        dest="occupy",
        default=False,
        action="store_true",
        help="occupy GPU memory first for training.",
    )
    parser.add_argument(
        "-l",
        "--logger",
        type=str,
        help="Logger to be used for metrics",
        default="tensorboard"
    )
    parser.add_argument(
        "opts",
        help="Modify config options using the command-line",
        default=None,
        nargs=argparse.REMAINDER,
    )
    return parser


@logger.catch                           # 装饰器，用于捕获main函数中的任何异常并记录
def main(exp, args):                    # 主函数（实验配置参数，命令行参数）

    # 设置种子
    if exp.seed is not None:            # 如果exp对象中定义了一个种子，种子是随机数生成器的初始值，使用种子可以确保每次训练的初始权重参数相同，确保了可复现性
        random.seed(exp.seed)           # 为随机模块设置种子
        torch.manual_seed(exp.seed)     # 为pytorch设置种子，确保模型训练过程可复现
        cudnn.deterministic = True      # 设置CUDA库为确定性模式，保证结果可复现
        warnings.warn(                  # 警告用户关于设置种子可能会导致的性能下降和潜在的复现问题
            "You have chosen to seed training. This will turn on the CUDNN deterministic setting, "
            "which can slow down your training considerably! You may see unexpected behavior "
            "when restarting from checkpoints."
        )

    # 设置环境
    configure_nccl()                    # 配置NVDIA的NCCL，用于GPU间的通信
    configure_omp()                     # 配置OpenMp，一种用于多线程编程的库
    cudnn.benchmark = True              # 启用cudnn自动调优器，根据网络配置自动选择最优算法，提高效率

    # 训练器选择
    if (args.distillation):                      # 使用知识蒸馏
        trainer = TrainerWithTeacher(exp, args)  # 使用带有教师模型的训练器
    else:                                        # 不使用知识蒸馏
        trainer = Trainer(exp, args)             # 使用普通训练器
    trainer.train()                              # 开启训练过程


if __name__ == "__main__":
    configure_module()

    # 设置实验配置文件
    args = make_parser().parse_args()            # 解析命令行参数对象，赋给args
    exp = get_exp(args.exp_file, args.name)      # 根据命令行参数加载配置文件，真正的配置文件应该在yolox_base的EXP类中，yolox_s.py是其简化版
    if (args.distillation):                      # 如果使用知识蒸馏
        exp.use_distillation = True              # 更改配置文件中的参数
    exp.merge(args.opts)                         # 将命令行中的其他选项与实验配置文件合并

    if not args.experiment_name:                 # 如果没有给定实验名称，则使用配置文件中的默认名称
        args.experiment_name = exp.exp_name      

    num_gpu = get_num_devices() if args.devices is None else args.devices # 确定使用的GPU数量
    assert num_gpu <= get_num_devices()                                   # 确保要求的GPU数量不超过实际GPU数量

    dist_url = "auto" if args.dist_url is None else args.dist_url         # 设置分布式训练
    launch(                                                            
        main,                                                             # main函数
        num_gpu,                                                          # GPU数量
        args.num_machines,                                                # 计算机数量
        args.machine_rank,                                                # 计算机序号（多计算机训练）
        backend=args.dist_backend,                                        # 分布式训练后端
        dist_url=dist_url,                                                # 多GPU分布式训练
        args=(exp, args),                                                 # 将实验配置文件和命令行参数传递给main函数
    )                                                                     # 使用launch启动分布式训练