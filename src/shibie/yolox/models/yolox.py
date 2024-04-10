#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (c) 2014-2021 Megvii Inc. All rights reserved.

# yolox网络结构

import torch.nn as nn                   # 从pytorch机器学习库中导入神经网络模块

from .yolo_head import YOLOXHead        # 解耦头（prediction）
from .yolo_pafpn import YOLOPAFPN       # backbone(CSP结构为主体)


class YOLOX(nn.Module):                 # 以nn模块中的Module类为父类创建YOLOX类
    """
    YOLOX model module. The module list is defined by create_yolov3_modules function.
    The network returns loss values from three YOLO layers during training
    and detection results during test.
    """

    def __init__(self, backbone=None, head=None):
        super().__init__()
        if backbone is None:
            backbone = YOLOPAFPN()      # 默认使用YOLOPAFPN类实例作为backbone
        if head is None:
            head = YOLOXHead(80)        # 默认使用YOLOXHead类实例作为head

        self.backbone = backbone        # 将backbone属性赋为backbone
        self.head = head                # 将head属性赋为head

    def forward(self, x, targets=None): # 定义前向传播函数，接受输入值x、目标值targets
        # fpn output content features of [dark3, dark4, dark5]
        fpn_outs = self.backbone(x)     # 骨干网络处理输入数据x，得到FPN的输出

        if self.training:               # 如果处于训练状态，计算损失，返回损失值字典
            
            assert targets is not None
            loss, reg_loss, conf_loss, cls_loss, l1_loss, num_fg = self.head(
                fpn_outs, targets, x
            )                           # 这里直接将实例head作为函数使用，其实是调用了YOLOXHead类父类中的__call__方法，
                                        # 即调用YOLOXHead的forward()方法，输入fpn_outs，输出损失
            outputs = {
                "total_loss": loss,
                "reg_loss": reg_loss,
                "l1_loss": l1_loss,
                "conf_loss": conf_loss,
                "cls_loss": cls_loss,
                #"colors_loss":colors_loss,
                "num_fg": num_fg,
            }                           # 训练模式下，输出为包含各损失的字典
        else:
            outputs = self.head(fpn_outs)# 推理模式下，直接返回解耦头的输出

        return outputs                  # 返回输出
