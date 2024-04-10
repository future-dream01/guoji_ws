#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (c) 2014-2021 Megvii Inc. All rights reserved.

# 基于CSP和FPN结构的Backbone骨干网络

import torch
import torch.nn as nn

from .darknet import CSPDarknet
from .network_blocks import BaseConv, CSPLayer, DWConv


class YOLOPAFPN(nn.Module):                         # 以Module类为父类定义YOLOPAFPN类
    def __init__(
        self,
        depth=1.0,                                  # 网络深度因子
        width=1.0,                                  # 网络宽度因子
        in_features=("dark3", "dark4", "dark5"),    # 输入特征层，"dark3", "dark4", "dark5"分别指代较浅、中等、较深的层级
        in_channels=[256, 512, 1024],               # 输入的通道数，有三个通道数，分别对应"dark3", "dark4", "dark5"
        depthwise=True,                            # 是否使用深度可分离卷积
        act="silu",                                 # 激活函数silu
    ):  
        super().__init__()                          # 父类初始化
        self.backbone = CSPDarknet(depth, width, depthwise=depthwise, act=act) # 创建CSPDarknet网络作为主体部分
        self.in_features = in_features              # 创建输入特征层属性
        self.in_channels = in_channels              # 创建输入通道数属性
        Conv = DWConv if depthwise else BaseConv    # depthwise为True:深度卷积；为Fulse：不使用深度卷积

        self.upsample = nn.Upsample(scale_factor=2, mode="nearest") # 创建上采样层，用于特征图尺寸放大
        self.lateral_conv0 = BaseConv(
            int(in_channels[2] * width), int(in_channels[1] * width), 1, 1, act=act
        )                                           # 创建侧边卷积层(输入通道数，输出通道数，卷积核大小，卷积核步长，激活函数)
                                                    # 此卷积层的作用是将来自深层的特征图通道数减小为适合于中层的特征图通道数，以进行FPN操作
        self.C3_p4 = CSPLayer(
            int(2 * in_channels[1] * width),        # 输入通道数
            int(in_channels[1] * width),            # 输出通道数
            round(3 * depth),                       # 结构重复次数
            False,                                  # 是否使用特殊结构（Bottleneck、Res）
            depthwise=depthwise,                    # 是否使用深度卷积
            act=act,                                # 激活函数类型
        )                                           # 创建CSP层 

        self.reduce_conv1 = BaseConv(
            int(in_channels[1] * width), int(in_channels[0] * width), 1, 1, act=act
        )                                           # 创建侧边卷积层(输入通道数，输出通道数，卷积核大小，卷积核步长，激活函数)
        self.C3_p3 = CSPLayer(
            int(2 * in_channels[0] * width),
            int(in_channels[0] * width),
            round(3 * depth),
            False,
            depthwise=depthwise,
            act=act,
        )                                           # 创建CSP层

        self.bu_conv2 = Conv(
            int(in_channels[0] * width), int(in_channels[0] * width), 3, 2, act=act
        )                                           # 创建下采样卷积层，用于将底部特征图尺寸减半                           

        self.C3_n3 = CSPLayer(
            int(2 * in_channels[0] * width),
            int(in_channels[1] * width),
            round(3 * depth),
            False,
            depthwise=depthwise,
            act=act,
        )                                           # 创建CSP层

        self.bu_conv1 = Conv(
            int(in_channels[1] * width), int(in_channels[1] * width), 3, 2, act=act
        )                                           # 创建卷积层，用于将中部特征图尺寸减半

        self.C3_n4 = CSPLayer(
            int(2 * in_channels[1] * width),
            int(in_channels[2] * width),
            round(3 * depth),
            False,
            depthwise=depthwise,
            act=act,
        )                                           # 创建CSP层

    def forward(self, input):                       # YOLOPAFPN结构的的向前传播函数

        ## backbone结构
        # 深度层级主要通过空间分辨率（尺寸）区分
        out_features = self.backbone(input)         # 先用backbone（CSPDarknet）提取特征，输出为不同深度层级的特征图
        features = [out_features[f] for f in self.in_features] # 将三个深度层级的特征图赋给features
        [x2, x1, x0] = features                     # 将x2、x1、x0分别赋为来自三个深度层级"dark3", "dark4", "dark5"的特征图

        ## FPN结构
        # 深层与中层融合到中层
        fpn_out0 = self.lateral_conv0(x0)           # 经过一个侧边卷积层，通道数减半（1024->512），尺寸不变（1/32） 
        f_out0 = self.upsample(fpn_out0)            # 经过一个深-中上采样层，通道数不变（512），尺寸增加（1/16），尺寸数不变
        f_out0 = torch.cat([f_out0, x1], 1)         # 经过一个中层concat融合，与中层特征图x1特征融合，通道数相加（512+512->1024），尺寸不变（1/16)
        f_out0 = self.C3_p4(f_out0)                 # 经过一个CSP层，因为中层输入经过了拼接，所以这里要让通道数减半（1024->512），尺寸不变（1/16）

        # 中层与底层融合到底层，得到第一个融合图pan_out2
        fpn_out1 = self.reduce_conv1(f_out0)        # 继续经过侧边卷积层，通道数减半（512->256），尺寸不变（1/16）
        f_out1 = self.upsample(fpn_out1)            # 继续经过中-底上采样层，通道数不变（256），尺寸增加（1/16->1/8）
        f_out1 = torch.cat([f_out1, x2], 1)         # 继续经过底层concat融合，通道数相加（256->512），尺寸不变（1/8）
        pan_out2 = self.C3_p3(f_out1)               # 继续经过CSP层，让经过拼接的特征图通道数减半（512->256），尺寸不变（1/8）

        # pan_out2再与中层融合，得到第二个融合图pan_out1
        p_out1 = self.bu_conv2(pan_out2)            # 继续经过底-中下采样卷积层，通道数不变（256），尺寸减小(1/8->1/16)
        p_out1 = torch.cat([p_out1, fpn_out1], 1)   # 继续经过中层concat融合，通道数相加（256->512），通道数不变（1/16）
        pan_out1 = self.C3_n3(p_out1)               # 继续经过CSP层，通道数不变（512），尺寸不变（1/16）

        # pan_out1再与深层融合，得到第三个融合图pan_out0
        p_out0 = self.bu_conv1(pan_out1)            # 继续经过中-深下采样卷积层，通道数不变（512）,尺寸减小（1/32)
        p_out0 = torch.cat([p_out0, fpn_out0], 1)   # 继续经过深层concat融合，通道数相加（512->1024），尺寸不变（1/32）
        pan_out0 = self.C3_n4(p_out0)               # 继续经过CSP层，通道数不变（1024），尺寸不变（1/32）

        outputs = (pan_out2, pan_out1, pan_out0)    
        return outputs                              # 输出三个融合过后的特征图
