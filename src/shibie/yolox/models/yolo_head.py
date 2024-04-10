#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (c) 2014-2021 Megvii Inc. All rights reserved.

# yolox检测头部分

from pickletools import int4
import cv2                                  # 导入opencv

import math
from loguru import logger                   # 日志库

import numpy as np

import torch
from torch._C import device
from torch.functional import Tensor
import torch.nn as nn                       # 导入神经网络模块
import torch.nn.functional as F

from yolox.utils import bboxes_iou
from yolox.utils.boxes import min_rect
from .losses import PolyIOUloss,WingLoss,FocalLoss

from .network_blocks import BaseConv, DWConv     # 导入普通卷积层类、深度卷积层类


class YOLOXHead(nn.Module):                 # 基于父类Module创建YOLOXHead类
    def __init__(
        self,
        num_apexes,                         # 特征点数
        num_classes,                        # 目标类别数
        #num_colors,                         # 目标颜色数
        width=1.0,
        strides=[8, 16, 32],                # 步长
        in_channels=[256, 512, 1024],
        act="silu",
        depthwise=True,                    # 深度可分离卷积
    ):
        """
        Args:
            act (str): activation type of conv. Defalut value: "silu".
            depthwise (bool): whether apply depthwise conv in conv branch. Defalut value: False.
        """
        super().__init__()
        self.n_anchors = 1                  # 每个网格上的预测框数量
        self.num_apexes = num_apexes        # 特征点属性
        self.num_classes = num_classes      # 类别数属性
        #self.num_colors = num_colors        # 颜色属性    
        self.decode_in_inference = True     # for deploy, set to False
        self.cls_convs = nn.ModuleList()    # 创建模块列表，存放类别特征提取卷积层
        self.reg_convs = nn.ModuleList()    # 创建模块列表，存放预测框回归卷积层
        self.cls_preds = nn.ModuleList()    # 创建模块列表，存放类别预测卷积层
        #self.color_preds = nn.ModuleList()  # 创建模块列表，存放
        self.reg_preds = nn.ModuleList()    # 创建模块列表，存放预测框回归卷积层
        self.obj_preds = nn.ModuleList()    # 创建模块列表，存放前景预测卷积层
        self.in_channels = in_channels      # 输入通道数属性
        self.stem_channels = [int(256 * width), int(256 * width), int(256 * width)] # 检测头基本通道数
        self.stems = nn.ModuleList()        # 
        Conv = DWConv if depthwise else BaseConv # depthwise为真则使用深度可分离卷积，为假则使用基本卷积
        for i in range(len(in_channels)):               # 为每个输入通道数创建独立卷积层
            self.stems.append(
                BaseConv(
                    in_channels=int(in_channels[i]),    # 输入通道数
                    out_channels=int(256 * width),      # 输入通道数
                    ksize=1,                            # 卷积核尺寸
                    stride=1,                           # 卷积核步长
                    act=act,                            # 激活函数
                )
            )     

            # 类别特征提取卷积层
            self.cls_convs.append(
                nn.Sequential(                          # Sequential用于顺序地创建两个卷积层的序列，作为一整个元素加入到cls_convs列表中
                    *[                                  # 解包，将列表中的元素作为独立参数传递给Sequential
                        Conv(                           # 创建卷积层
                            in_channels=int(256 * width),
                            out_channels=int(256 * width),
                            ksize=5,
                            stride=1,
                            act=act,
                        ),
                        Conv(
                            in_channels=int(256 * width),
                            out_channels=int(256 * width),
                            ksize=5,
                            stride=1,
                            act=act,
                        ),
                    ]
                )
            )

            # 预测框回归卷积层
            self.reg_convs.append(                      # 同理，创建两个卷积层加入到reg_convs
                nn.Sequential(
                    *[
                        Conv(
                            in_channels=int(256 * width),
                            out_channels=int(256 * width),
                            ksize=5,
                            stride=1,
                            act=act,
                        ),
                        Conv(
                            in_channels=int(256 * width),
                            out_channels=int(256 * width),
                            ksize=5,
                            stride=1,
                            act=act,
                        ),
                    ]
                )
            )

            # 类别预测卷积层
            self.cls_preds.append(
                nn.Conv2d(                                          # 同理，使用nn模块中的普通不含激活函数的卷积层加入到cls_preds中
                    in_channels=int(256 * width),
                    out_channels=self.n_anchors * self.num_classes, # 输出通道数=每个网格中预测框数*类别数
                    kernel_size=1,                                  # 卷积核大小
                    stride=1,                                       # 步长
                    padding=0,                                      # 周围不填充
                )
            )

            # 颜色预测卷积层
           # self.color_preds.append(
               # nn.Conv2d(
                    #in_channels=int(256 * width),
                    #out_channels=self.n_anchors * self.num_colors,
                    #kernel_size=1,
                    #stride=1,
                    #padding=0,
               # )
           # )

            # 预测框预测卷积层
            self.reg_preds.append(
                nn.Conv2d(
                    in_channels=int(256 * width),
                    out_channels=self.num_apexes * 2,   # 输出通道数=特征点数*2 特征点的预测方式是预测点的坐标
                    kernel_size=1,
                    stride=1,
                    padding=0,
                )
            )

            # 前景预测卷积层
            self.obj_preds.append(
                nn.Conv2d(
                    in_channels=int(256 * width),
                    out_channels=self.n_anchors * 1, # 输出通道数=每个网格预测框数量
                    kernel_size=1,
                    stride=1,
                    padding=0,
                )
            )

        #TODO:根据样本数量调整alpha权值
        self.use_l1 = False                         # 是否使用l1损失
        self.use_distill = False                    # 是否使用知识蒸馏
        self.l1_loss = nn.L1Loss(reduction="none")  # 定义l1损失函数
        self.bcewithlog_loss = nn.BCEWithLogitsLoss(reduction="none")        # 定义二元交叉熵损失函数，结合了sigmoid层和BCELoss
        # self.bcewithlog_loss_cls = nn.BCEWithLogitsLoss(pos_weight=self.alpha_cls, reduction="none")
        # self.bcewithlog_loss_colors = nn.BCEWithLogitsLoss(pos_weight=self.alpha_cls_colors, reduction="none")
        self.bcewithlog_loss_cls = nn.BCEWithLogitsLoss(reduction="none")    # 定义类别损失函数，结合了sigmoid层和BCELoss
        #self.bcewithlog_loss_colors = nn.BCEWithLogitsLoss(reduction="none") # 定义颜色损失函数，结合了sigmoid层和BCELoss
        # self.focal_loss_obj = FocalLoss(alpha=0.25, gamma=2)
        # self.focal_loss_cls = FocalLoss(alpha=self.alpha_cls, gamma=2, num_classes=self.num_classes)
        # self.focal_loss_colors = FocalLoss(alpha=self.alpha_cls_colors, gamma=2, num_classes=self.num_colors)
        self.l1 = nn.L1Loss(reduction="none")                   # 
        self.wing_loss = WingLoss()                             # 
        self.strides = strides                                  # 
        self.grids = [torch.zeros(1)] * len(in_channels)        # 

    def initialize_biases(self, prior_prob):                    # 初始化偏置项     
        for conv in self.cls_preds:
            b = conv.bias.view(self.n_anchors, -1)
            b.data.fill_(-math.log((1 - prior_prob) / prior_prob))
            conv.bias = torch.nn.Parameter(b.view(-1), requires_grad=True)

        #for conv in self.color_preds:
            #b = conv.bias.view(self.n_anchors, -1)
            #b.data.fill_(-math.log((1 - prior_prob) / prior_prob))
            #conv.bias = torch.nn.Parameter(b.view(-1), requires_grad=True)

        for conv in self.obj_preds:
            b = conv.bias.view(self.n_anchors, -1)
            b.data.fill_(-math.log((1 - prior_prob) / prior_prob))
            conv.bias = torch.nn.Parameter(b.view(-1), requires_grad=True)

    def forward(self, xin, labels=None, imgs=None):      # 前向传播函数   
        # 初始化各种列表 
        outputs = []            # 输出特征图列表
        origin_preds = []       # 存储原始预测
        x_shifts = []           # 网格在原始图片中的x坐标
        y_shifts = []           # 网格在原始图片中的y坐标
        expanded_strides = []   # 步长信息，影响特征图上的坐标到原始图片坐标的对应关系
        for k, (cls_conv, reg_conv, stride_this_level, x) in enumerate(
            zip(self.cls_convs, self.reg_convs, self.strides, xin)
        ):
            x = self.stems[k](x)                        # 使用stems中的第k个卷积层先对x进行卷积操作
            cls_x = x                                   # 卷积结果x被用于之后的类别特征提取卷积
            reg_x = x                                   # 卷积结果x被用于之后的预测框回归卷积
            
            # 类别
            cls_feat = cls_conv(cls_x)                  # 对x使用 类别特征提取卷积层
            cls_output = self.cls_preds[k](cls_feat)    # 使用 类别预测卷积层 对 类别特征提取卷积操作 的结果进行卷积

            # 颜色
            #color_output = self.color_preds[k](cls_feat)# 使用 颜色预测卷积层 对 类别特征提取卷积操作 的结果进行卷积

            # 预测框
            reg_feat = reg_conv(reg_x)                  # 使用 预测框框回归卷积层 对 reg_x 进行卷积
            reg_output = self.reg_preds[k](reg_feat)    # 使用 预测框预测卷积层 对 预测框回归卷积层 的结果进行卷积

            # 前景
            obj_output = self.obj_preds[k](reg_feat)    # 使用 前景预测卷积层 对 预测框回归卷积层 的结果进行卷积

            # 如果处于训练模式，重塑output、grid、reg_output
            if self.training:                           
                output = torch.cat([reg_output, obj_output, cls_output], 1) # 将预测框(10)、前景(1)、颜色(4)、类别(3)的卷积预测结果进行concat操作，深度上连接
                                                                                          # 特征图形状一般是[批次图片数量，通道数，高度，宽度]
                output, grid = self.get_output_and_grid(
                    output, k, stride_this_level, xin[0].type()
                )                                       # 将output内部重新排列 [批次图片数量,每个网格预测框数*高度*宽度（预测框总数），-1（表示所有预测特征）]
                                                        # grid张量存放特征图的每个锚点/预测框对应在此特征图中的坐标 [1(每个特征图都相同),特征图高度*宽度(网格数)，2(表示两个坐标x、y)]

                x_shifts.append(grid[:, :, 0])          # 将grid张量中所有网格的x坐标赋给x_shifts列表
                y_shifts.append(grid[:, :, 1])          # 将grid张量中所有网格的y坐标赋给y_shifts列表
                expanded_strides.append(
                    torch.zeros(1, grid.shape[1])       # 创建一个形状为[1,特征图数]的矩阵
                    .fill_(stride_this_level)           # 用网格所在特征图的步长信息填充每个位置
                    .type_as(xin[0])
                )                                       # 对于一个同一层级的特征图，步长矩阵形状为[1，特征图数]

                # 如果使用的是l1损失函数（针对预测框预测），将reg_output重塑为[批次大小，-1（所有预测框），特征点坐标]
                if self.use_l1:                         
                    batch_size = reg_output.shape[0]    # 获取预测框预测特征图的批次数，reg_output形状为[批次数，特征点数*2，高度，宽度]
                    hsize, wsize = reg_output.shape[-2:]# 将reg_output张量中的第2、3维度信息(高度、宽度)提取到hsize, wsize
                    reg_output = reg_output.view(       
                        batch_size, self.n_anchors, self.num_apexes * 2, hsize, wsize
                    )                                   # 重塑张量形状 [批次数，每个网格预测框数，特征点数*2，高度，宽度]
                    reg_output = reg_output.permute(0, 1, 3, 4, 2).reshape( # permute(0, 1, 3, 4, 2)：调整张量顺序
                        batch_size, -1, self.num_apexes * 2                 # reshape()调整张量形状 
                    )                                   # 此代码将reg_output张量重塑为 [批次大小，-1（所有预测框），特征点坐标]
                    origin_preds.append(reg_output.clone()) # 将reg_output张量储存到原始预测列表origin_preds中

            # 如果是推理模式，直接将预测框预测特征图、前景预测特征图、颜色预测特征图、类别预测特征图融合在一起
            else:                                       
                output = torch.cat(
                    [reg_output, obj_output.sigmoid(), cls_output.sigmoid()], 1
                )                                       # 使用concat操作融合

            outputs.append(output)                      # 将output加入到outputs中去

        # 如果处于训练模式，返回损失值
        if self.training:                               
            if not self.use_distill:                    # 如果没有使用知识蒸馏
                return self.get_losses(                 # 使用一般的损失函数
                    imgs,                               # 原始图片
                    x_shifts,                           # 锚点/预测框相对于所在特征图左上角(原点)的x偏移量(坐标x)
                    y_shifts,                           # 锚点/预测框相对于所在特征图左上角(原点)的y偏移量(坐标y)
                    expanded_strides,                   # 锚点/预测框所在特征图相对于原图的缩放比例信息
                    labels,                             # 标签，包含真值框类别信息、坐标信息等
                    torch.cat(outputs, 1),              # 将重塑后的outputs列表中的所有特征图在预测框数量上拼接在一起
                    origin_preds,                       # 原始预测列表
                    dtype=xin[0].dtype,                 # 指定用于损失计算的数据类型，和输入xin相同
                )                                       # 返回各损失值
            
            else:                                       # 如果使用知识蒸馏
                return self.get_losses_distill(         # 使用知识蒸馏专用损失函数
                    imgs,                               
                    x_shifts,
                    y_shifts,
                    expanded_strides,
                    labels,
                    torch.cat(outputs, 1),
                    origin_preds,
                    dtype=xin[0].dtype,
                )
            
        # 如果是推理模式，直接返回outputs
        else:                                                               
            self.hw = [x.shape[-2:] for x in outputs]                       # outputs中是每个深度层级的所有特征图，对于里面的每一项output的后两个维度：高度、宽度，加入到hw列表中
            outputs = torch.cat(
                [x.flatten(start_dim=2) for x in outputs], dim=2            # 将每个output特征图通道的第3、4个维度，即高度和宽度压缩成一个维度，再在第2个维度，即通道数上进行拼接
            ).permute(0, 2, 1)                                              # permute(): 将张量维度重新排序，现在是[批次总数，一张特征图网格数，通道数]
            if self.decode_in_inference:                                    # 如果需要解码
                return self.decode_outputs(outputs, dtype=xin[0].type())    
            else:
                return outputs
    #Transform
    def get_output_and_grid(self, output, k, stride, dtype):        # 重塑output张量，使得其包含实际图像中的位置信息
        grid = self.grids[k]                                       
        batch_size = output.shape[0]
        n_ch = 1 + self.num_apexes * 2 + self.num_classes 
        hsize, wsize = output.shape[-2:]
        if grid.shape[2:4] != output.shape[2:4]:
            #Generate grid
            yv, xv = torch.meshgrid([torch.arange(hsize), torch.arange(wsize)])
            grid = torch.stack((xv, yv), 2).view(1, 1, hsize, wsize, 2).type(dtype)
            self.grids[k] = grid
        output = output.view(batch_size, self.n_anchors, n_ch, hsize, wsize)
        output = output.permute(0, 1, 3, 4, 2).reshape(
            batch_size, self.n_anchors * hsize * wsize, -1
        )
        grid = grid.view(1, -1, 2)

        for i in range(self.num_apexes):
            output[..., 2 * i:2 * (i + 1)] = (output[..., 2 * i:2 * (i + 1)] + grid) * stride

        return output, grid

    def decode_outputs(self, outputs, dtype):       # 将原始输出outputs(类别得分、预测框偏移量等)转换成更直观的形式(标记类别、修正后的预测框坐标)
        grids = []
        strides = []
        for (hsize, wsize), stride in zip(self.hw, self.strides):
            yv, xv = torch.meshgrid([torch.arange(hsize), torch.arange(wsize)])
            grid = torch.stack((xv, yv), 2).view(1, -1, 2)
            grids.append(grid)
            shape = grid.shape[:2]
            strides.append(torch.full((*shape, 1), stride))

        grids = torch.cat(grids, dim=1).type(dtype)
        strides = torch.cat(strides, dim=1).type(dtype)

        for i in range(self.num_apexes):
            outputs[..., 2 * i:2 * (i + 1)] = (outputs[..., 2 * i:2 * (i + 1)] + grids) * strides
        return outputs

    # 知识蒸馏损失函数
    def get_losses_distill(
        self,
        imgs,
        x_shifts,
        y_shifts,
        expanded_strides,
        labels,
        outputs,
        origin_preds,
        dtype,
    ):

        # # Cut feature map into bbox,obj,color,cls
        bbox_preds = outputs[:, :, :self.num_apexes * 2].contiguous()  # [batch, n_anchors_all, self.num_apexes * 2]
        obj_preds = outputs[:, :, self.num_apexes * 2].contiguous()  # [batch, n_anchors_all, 1]
       # color_preds = outputs[:, :, self.num_apexes * 2 + 1 :self.num_apexes * 2 + 1 + self.num_colors].contiguous()  # [batch, n_anchors_all, n_color]
        cls_preds = outputs[:, :, self.num_apexes * 2 + 1 :].contiguous()  # [batch, n_anchors_all, n_cls]

        bbox_teacher = labels[:, :, :self.num_apexes * 2].contiguous()  # [batch, n_anchors_all, self.num_apexes * 2]
        obj_teacher = labels[:, :, self.num_apexes * 2].contiguous()  # [batch, n_anchors_all, 1]
        #color_teacher = labels[:, :, self.num_apexes * 2 + 1:self.num_apexes * 2 + 1 + self.num_colors].contiguous()  # [batch, n_anchors_all, n_color]
        cls_teacher = labels[:, :, self.num_apexes * 2 + 1 :].contiguous()  # [batch, n_anchors_all, n_cls]

        x_shifts = torch.cat(x_shifts, 1)  # [1, n_anchors_all]
        y_shifts = torch.cat(y_shifts, 1)  # [1, n_anchors_all]
        # expanded_strides = torch.cat(expanded_strides, 1)
        # if True:
        #     origin_preds = torch.cat(origin_preds, 1)

        gt_masks = (obj_teacher > 0.3)
        num_postive = (int)(obj_teacher.sum())
        l1_targets = []

        loss_reg = (
        self.wing_loss(bbox_preds[gt_masks], bbox_teacher[gt_masks])
        ).sum()  / num_postive

        loss_obj = (
            self.bcewithlog_loss(obj_preds, obj_teacher)
        ).sum()  / num_postive

        loss_cls = (
            self.bcewithlog_loss_cls(cls_preds[gt_masks].view(-1, self.num_classes), cls_teacher[gt_masks].view(-1, self.num_classes))
        ).sum() / num_postive

        #loss_colors = (
            #self.bcewithlog_loss_colors(
                #color_preds[gt_masks].view(-1, self.num_colors), color_teacher[gt_masks].view(-1, self.num_colors)
            #)
       # ).sum() / num_postive

        if self.use_l1:
            loss_l1 = (
                self.l1_loss(bbox_preds[gt_masks].view(-1, self.num_apexes * 2), bbox_teacher[gt_masks].view(-1, self.num_apexes * 2))
            ).sum() / num_postive
        else:
            loss_l1 = 0.0

        reg_weight = 100
        conf_weight = 1
        #clr_weight = 1
        cls_weight = 1
        loss = reg_weight * loss_reg + conf_weight * loss_obj + cls_weight * loss_cls  + 0.1 * loss_l1

        return (
            loss,
            reg_weight * loss_reg,
            conf_weight * loss_obj,
            cls_weight * loss_cls,
            #clr_weight * loss_colors,
            0.1 * loss_l1,
            1,
        )

    # 普通损失函数
    def get_losses(                 
        self,               
        imgs,                   # 原始图像
        x_shifts,
        y_shifts,
        expanded_strides,
        labels,                 # 标签
        outputs,
        origin_preds,
        dtype,
    ):
        # 将特征图切分成bbox,obj,color,cls
        # 特征图结构：特征点坐标，前景，颜色，类别
        bbox_preds = outputs[:, :, :self.num_apexes * 2]                          # 获取outputs中的有关预测框回归的信息
        obj_preds = outputs[:, :, self.num_apexes * 2].unsqueeze(-1)              # 获取outputs中的有关置信度预测的信息
        #color_preds = outputs[:, :, self.num_apexes * 2 + 1:self.num_apexes * 2 + 1 + self.num_colors]  # 获取outputs中的有关颜色预测的信息
        cls_preds = outputs[:, :, self.num_apexes * 2 + 1:]     # 获取outputs中的有关类别预测的信息

        nlabel = (labels.sum(dim=2) > 0).sum(dim=1)               # 

        total_num_anchors = outputs.shape[1]                      # 总预测框数
        x_shifts = torch.cat(x_shifts, 1)                         # x坐标向量，第二维度网格数上拼接
        y_shifts = torch.cat(y_shifts, 1)                         # y坐标向量，第二维度网格数上拼接
        expanded_strides = torch.cat(expanded_strides, 1)         # 步长值矩阵，三个矩阵在网格数维度上拼接，一个批次用里面的一张图片信息代替
        if self.use_l1:                                           # 如果使用l1损失
            origin_preds = torch.cat(origin_preds, 1)             # 得到原始的只包含预测框回归有关参数的张量

        cls_targets = []                                          # 类别类型目标信息
        #colors_targets = []                                       # 颜色类型目标信息
        reg_targets = []                                          # 预测框类型目标信息
        l1_targets = []                                           # l1类型目标信息
        obj_targets = []                                          # 前景类型目标信息
        fg_masks = []

        num_fg = 0.0                                              # 前景框总数量
        num_gts = 0.0                                             # 真值框总数

        for batch_idx in range(outputs.shape[0]):                          # 批次中的每张图片
            num_gt = int(nlabel[batch_idx])                                # 当前图片中真值框数量
            num_gts += num_gt                                              # 真值框数累加
            if num_gt == 0:                                                # 如果没有目标，创建一系列空列表
                cls_target = outputs.new_zeros((0, self.num_classes))      
                #colors_target = outputs.new_zeros((0, self.num_colors))     
                reg_target = outputs.new_zeros((0, self.num_apexes * 2))
                l1_target = outputs.new_zeros((0, self.num_apexes * 2))
                obj_target = outputs.new_zeros((total_num_anchors, 1))
                fg_mask = outputs.new_zeros(total_num_anchors).bool()
            else:                                                          # 存在目标
                gt_bboxes_per_image = labels[batch_idx, :num_gt, 2:2 + self.num_apexes * 2] # 提取真值框的位置目标信息，二维张量
                                                                                            # `2:2 + self.num_apexes * 2`:从第2个位置到第(2+5*2)个位置，即所有坐标信息
                gt_classes = labels[batch_idx, :num_gt, 0]                                  # 提取真值框所属的类别信息
                #gt_colors = labels[batch_idx, :num_gt, 1]                                   # 提真值框所属的颜色信息

                bboxes_preds_per_image = bbox_preds[batch_idx]                              # 预测框的位置信息
                gt_rect_bboxes_per_image = min_rect(gt_bboxes_per_image)                    # min_rect()函数生成一个包含真值关键点的最小边界框，可以用于NMS、定位、分类、多任务学习等
                rect_bboxes_preds_per_image = min_rect(bboxes_preds_per_image)              # min_rect()函数生成一个包含预测关键点的最小边界框

                # 为每个真值框分配合适的预测框
                try:                        
                    (
                    gt_matched_classes,         # 被选中的预测框分别的真实类别
                    #gt_matched_colors,          # 被选中的预测框分别的真实颜色
                    fg_mask,                    # 前景掩码，长度等于所有预测框个数，每个如果包含了感兴趣物体，则置True，否则置Falth
                    pred_ious_this_matching,    # 被选中的预测框分别相对于真值框的交占比IOU
                    matched_gt_inds,            # 被选中的预测框分别对应的真值框的索引
                    num_fg_img,                 # 前景数量，表示有多少个预测框被认为包含感兴趣物体
                ) = self.get_assignments(       # get_assignments()函数返回所有预测框中最后选定的最接近每个真值框的几个预测框
                    batch_idx,                  # 每张图片在批次内的id
                    num_gt,                     # 每张图片中的真值框数
                    total_num_anchors,          # 每张图片中的总预测框数
                    gt_rect_bboxes_per_image,   # 每张图片中的真值框的位置大小信息(关键点检测中，是包含所有关键点的最小矩形框)
                    gt_classes,                 # 每张图中所有真值框分别所属的类别
                    #gt_colors,                  # 每张图中所有真值框分别所属的颜色
                    rect_bboxes_preds_per_image,# 每张图中所有预测框的位置大小信息(关键点检测中，是包含所有关键点的最小矩形框)
                    expanded_strides,           # 缩放比例信息
                    x_shifts,                   # 每个网格在原图中的x坐标
                    y_shifts,                   # 每个网格在原图中的y坐标
                    cls_preds,                  # 预测框有关类别的预测结果
                    #color_preds,                # 预测框有关颜色的预测结果
                    bbox_preds,                 # 预测框有关位置信息的预测结果
                    obj_preds,                  # 预测框有关前景信息的预测结果
                    labels,                     # 标签
                    imgs,                       # 原图
                )
                except RuntimeError:        # 如果显存不够，在CPU上重新进行
                    logger.error(
                        "OOM RuntimeError is raised due to the huge memory cost during label assignment. \
                           CPU mode is applied in this batch. If you want to avoid this issue, \
                           try to reduce the batch size or image size."
                    )
                    # torch.cuda.empty_cache()
                    (
                        gt_matched_classes,
                        #gt_matched_colors,
                        fg_mask,
                        pred_ious_this_matching,
                        matched_gt_inds,
                        num_fg_img,
                    ) = self.get_assignments(
                        batch_idx,              
                        num_gt,                 
                        total_num_anchors,      
                        gt_rect_bboxes_per_image,   
                        gt_classes,           
                        #gt_colors,
                        rect_bboxes_preds_per_image,
                        expanded_strides,
                        x_shifts,
                        y_shifts,
                        cls_preds,
                        #color_preds,
                        bbox_preds,
                        obj_preds,
                        labels,
                        imgs,
                        "cpu",
                    )

                torch.cuda.empty_cache()                        # 清空CUDA缓存
                num_fg += num_fg_img                            # 前景框数累加

                cls_target = F.one_hot(                         # 将预测框的真实类别写成one-hot编码的格式，再于预测框的IOU值相乘，组成加权one-hot编码，区分不同的匹配程度；扩维
                    gt_matched_classes.to(torch.int64), self.num_classes
                ) * pred_ious_this_matching.unsqueeze(-1)
                #colors_target = F.one_hot(                      # 颜色类别同理，组成加权one-hot编码
                    #gt_matched_colors.to(torch.int64), self.num_colors
                #) * pred_ious_this_matching.unsqueeze(-1)
                # print(cls_target)
                # print(pred_ious_this_matching.unsqueeze(-1))
                # cls_target = gt_matched_classes.to(torch.int64) * pred_ious_this_matching.unsqueeze(-1)
                # colors_target = gt_matched_colors.to(torch.int64) * pred_ious_this_matching.unsqueeze(-1)
                obj_target = fg_mask.unsqueeze(-1)               # 给前景掩码扩维
                reg_target = gt_bboxes_per_image[matched_gt_inds]# 根据matched_gt_inds索引找到每个被选中的预测框对应的真值框的关键点信息
                if self.use_l1:                                  # 如果使用l1损失
                    l1_target = self.get_l1_target(
                        outputs.new_zeros((num_fg_img, self.num_apexes * 2)),
                        gt_bboxes_per_image[matched_gt_inds],
                        expanded_strides[0][fg_mask],
                        x_shifts=x_shifts[0][fg_mask],
                        y_shifts=y_shifts[0][fg_mask],
                    )


            cls_targets.append(cls_target)                      # 被选中的预测框的加权类别one-hot编码
            #colors_targets.append(colors_target)                # 被选中的预测框的加权颜色one-hot编码
            reg_targets.append(reg_target)                      # 被选中的预测框对应的真值框的关键点信息列表
            obj_targets.append(obj_target.to(dtype))            # 所有预测框的前景编码(扩维后)
            fg_masks.append(fg_mask)                            # 所有预测框的前景编码(扩维前)
            if self.use_l1:                                     # 如果使用l1损失
                l1_targets.append(l1_target)                    # 将l1_target加入l1_targets中

        cls_targets = torch.cat(cls_targets, 0)                 # 将cls_targets在预测框个数上合并，包含一整个批次内的所有被选中预测框的加权类别one-hot编码
        #colors_targets = torch.cat(colors_targets, 0)           # 将colors_targets在预测框个数上合并，包含一整个批次内的所有被选中预测框的加权颜色one-hot编码
        reg_targets = torch.cat(reg_targets, 0)                 # 将reg_targets在预测框个数上合并，包含一整个批次内的所有被选中的预测框对应的真值框的关键点坐标
        obj_targets = torch.cat(obj_targets, 0)                 # 将obj_targets在预测框个数上合并，包含一整个批次内所有预测框的前景编码(二维矩阵)
        fg_masks = torch.cat(fg_masks, 0)                       # 将fg_masks在预测框个数上合并，包含一整个批次内所有预测框的前景编码(一维向量)
        if self.use_l1:
            l1_targets = torch.cat(l1_targets, 0)
        num_fg = max(num_fg, 1)                                 # 前景总数

        # 定位损失，使用wing_loss
        loss_reg = (
            self.wing_loss(bbox_preds.view(-1, self.num_apexes * 2)[fg_masks], reg_targets)
        ).sum() / num_fg                                        # view(-1, self.num_apexes * 2)：将bbox_preds重塑为二维向量，包含一整个批次内所有预测框的关键点坐标
                                                                # [fg_masks]：用前景掩码表示哪些预测框是被选中的
                                                                # reg_targets：包含一整个批次内的所有被选中的预测框对应的真值框的关键点坐标
                                                                # .sum() / num_fg：将所有被选中的预测框对应的定位损失值求和，再除以前景框总数，得到平均定位损失

        # 前景损失，使用bcewithlog_loss
        loss_obj = (
            self.bcewithlog_loss(obj_preds.view(-1, 1), obj_targets)
        ).sum() / num_fg                                        # view（1，-1）：将obj_preds重塑为二维张量，包含一个批次中所有的预测框的前景预测
                                                                # obj_targets：包含一个批次中所有预测框的前景掩码
                                                                # .sum() / num_fg ：将所有预测框对应的前景损失值求和，再除以前景框总数，得到平均前景损失
        # 类别损失，使用bcewithlog_loss_cls
        loss_cls = (
            self.bcewithlog_loss_cls(
                cls_preds.view(-1, self.num_classes)[fg_masks], cls_targets
            )
        )                                                       # view(-1, self.num_classes)：重塑cls_preds为二维张量，包含一个批次内所有预测框的类别得分
                                                                #[fg_masks]：标识哪些预测框是被选中的
                                                                # cls_targets：包含一整个批次内的所有被选中预测框的加权类别one-hot编码
        loss_cls = loss_cls.sum() / num_fg                      # 对所有被选中的预测框的类别损失求和再除以总前景框数，求得平均类别损失

         # 颜色损失
        #loss_colors = (
            #self.bcewithlog_loss_colors(
               # color_preds.view(-1, self.num_colors)[fg_masks], colors_targets
           # )                                                   # 
       # ).sum() / num_fg
        # print(cls_target)

        # loss_obj = (
        #     self.focal_loss_obj(obj_preds.view(-1, 1), obj_targets)
        # ).sum() / num_fg

        # loss_cls = (
        #     self.focal_loss_cls(
        #         cls_preds.view(-1, self.num_classes)[fg_masks], cls_targets
        #     )
        # ).sum() / num_fg

        # loss_colors = (
        #     self.focal_loss_colors(
        #         color_preds.view(-1, self.num_colors)[fg_masks], colors_targets
        #     )
        # ).sum() / num_fg

        if self.use_l1:
            loss_l1 = (
                self.l1_loss(origin_preds.view(-1, self.num_apexes * 2)[fg_masks], l1_targets)
            ).sum() / num_fg
        else:
            loss_l1 = 0.0

        reg_weight = 80         # 定位损失权重
        conf_weight = 1.5       # 前景损失权重
        #clr_weight = 1          # 颜色损失权重
        cls_weight = 1          # 分类损失权重
        loss = reg_weight * loss_reg + conf_weight * loss_obj + cls_weight * loss_cls  + loss_l1

        return (
            loss,                       # 总损失
            reg_weight * loss_reg,      # 定位损失
            conf_weight * loss_obj,     # 前景损失
            cls_weight * loss_cls,      # 类别损失
            #clr_weight * loss_colors,   # 颜色损失
            loss_l1,                    # l1损失
            num_fg / max(num_gts, 1),   # 前景框数除以真值框数
        )                               # 返回各损失

    # def get_losses_transfer_learning:():
    def get_l1_target(self, l1_target, gt, stride, x_shifts, y_shifts, eps=1e-8):
        for i in range(self.num_apexes):
            l1_target[:, 2 * i] = gt[:, 2 * i] / stride - x_shifts
            l1_target[:, 2 * i + 1] = gt[:,2 * i + 1] / stride - y_shifts
            # l1_target[:, 0] = gt[:, 0] / stride - x_shifts
            # l1_target[:, 1] = gt[:, 1] / stride - y_shifts
            # l1_target[:, 2] = torch.log(gt[:, 2] / stride + eps)
            # l1_target[:, 3] = torch.log(gt[:, 3] / stride + eps)
        return l1_target

    @torch.no_grad()
    
    # 为每个真值框分配合适的预测框
    def get_assignments(
        self,
        batch_idx,
        num_gt,
        total_num_anchors,
        gt_bboxes_per_image,
        gt_classes,
        #gt_colors,
        bboxes_preds_per_image,
        expanded_strides,
        x_shifts,
        y_shifts,
        cls_preds,
        #color_preds,
        bbox_preds,
        obj_preds,
        labels,
        imgs,
        mode="gpu",
    ):
        if mode == "cpu":
            print("------------CPU Mode for This Batch-------------")   
            gt_bboxes_per_image = gt_bboxes_per_image.cpu().float()
            bboxes_preds_per_image = bboxes_preds_per_image.cpu().float()
            gt_classes = gt_classes.cpu().float()
            #gt_colors = gt_colors.cpu().float()
            expanded_strides = expanded_strides.cpu().float()
            x_shifts = x_shifts.cpu()
            y_shifts = y_shifts.cpu()

        # 为真值框匹配的预测框进行初步筛选
        fg_mask, is_in_boxes_and_center = self.get_in_boxes_info(
            gt_bboxes_per_image,
            expanded_strides,
            x_shifts,                   
            y_shifts,                    
            total_num_anchors,
            num_gt,
        )
        # print(fg_mask.sum())
        #Reduce the anchor area
        bboxes_preds_per_image = bboxes_preds_per_image[fg_mask]
        # print(bboxes_preds_per_image)
        # print(gt_bboxes_per_image)
        # print("="*50)
        cls_preds_ = cls_preds[batch_idx][fg_mask]
        # color_preds_ = color_preds[batch_idx][fg_mask]
        obj_preds_ = obj_preds[batch_idx][fg_mask]
        num_in_boxes_anchor = bboxes_preds_per_image.shape[0]

        if mode == "cpu":
            gt_bboxes_per_image = gt_bboxes_per_image.cpu()
            bboxes_preds_per_image = bboxes_preds_per_image.cpu()
        
        # 
        pair_wise_ious = bboxes_iou(gt_bboxes_per_image, bboxes_preds_per_image, False)


        gt_cls_per_image = (
            F.one_hot(gt_classes.to(torch.int64), self.num_classes)
            .float()
            .unsqueeze(1)
            .repeat(1, num_in_boxes_anchor, 1)
        )

        #gt_colors_per_image = (
            #F.one_hot(gt_colors.to(torch.int64), self.num_colors)
            #.float()
            #.unsqueeze(1)
           # .repeat(1, num_in_boxes_anchor, 1)
       # )

        pair_wise_ious_loss = -torch.log(pair_wise_ious + 1e-8)

        if mode == "cpu":
            cls_preds_, obj_preds_ = cls_preds_.cpu(), obj_preds_.cpu()

        with torch.cuda.amp.autocast(enabled=False):
            cls_preds_ = (
                cls_preds_.float().unsqueeze(0).repeat(num_gt, 1, 1).sigmoid_()
                * obj_preds_.float().unsqueeze(0).repeat(num_gt, 1, 1).sigmoid_()
            )
            #color_preds_ = (
                #color_preds_.float().unsqueeze(0).repeat(num_gt, 1, 1).sigmoid_()
                #* obj_preds_.float().unsqueeze(0).repeat(num_gt, 1, 1).sigmoid_()
            #)
            # pair_wise_colors_loss = F.binary_cross_entropy(
            #     color_preds_.sqrt_(), gt_colors_per_image, reduction="none"
            # ).sum(-1)
            # pair_wise_cls_loss = F.binary_cross_entropy(
            #     cls_preds_.sqrt_(), gt_cls_per_image, reduction="none"
            # ).sum(-1)
            # print(colors_preds_.sqrt_())
            #pair_wise_colors_loss = F.binary_cross_entropy_with_logits(
                #color_preds_.sqrt_(), gt_colors_per_image, reduction="none"
            #).sum(-1)
            pair_wise_cls_loss = F.binary_cross_entropy_with_logits(
                cls_preds_.sqrt_(), gt_cls_per_image, reduction="none"
            ).sum(-1)

            # print(pair_wise_cls_loss.shape)
            # print(pair_wise_colors_loss.shape)
        del cls_preds_
        cost = (
            0.5 * pair_wise_cls_loss
            #+ 0.5 * pair_wise_colors_loss
            + 3.0 * pair_wise_ious_loss
            + 100000.0 * (~is_in_boxes_and_center)
        )
        #-----------------------------------------------------------
        #Dynamic K matching
        (
            num_fg,
            gt_matched_classes,
            pred_ious_this_matching,
            matched_gt_inds,
        ) = self.dynamic_k_matching( cost, pair_wise_ious, gt_classes, num_gt, fg_mask)
        del pair_wise_cls_loss,cost, pair_wise_ious, pair_wise_ious_loss

        if mode == "cpu":
            gt_matched_classes = gt_matched_classes.cuda()
            #gt_matched_colors = gt_matched_colors.cuda()
            fg_mask = fg_mask.cuda()
            pred_ious_this_matching = pred_ious_this_matching.cuda()
            matched_gt_inds = matched_gt_inds.cuda()

        return (
            gt_matched_classes,
            # gt_matched_colors,
            fg_mask,
            pred_ious_this_matching,
            matched_gt_inds,
            num_fg,
        )

    # 通过判断预测框中心点是否在真值框内，来选择筛选掉一部分预测框
    def get_in_boxes_info(
        self,
        gt_bboxes_per_image,
        expanded_strides,       
        x_shifts,
        y_shifts,
        total_num_anchors,
        num_gt,
    ):
        """
        Reduce the area of mathched anchors for dynamic k matching
        """
        expanded_strides_per_image = expanded_strides[0]                # 一维张量expanded_strides_per_image，储存每个特征图的缩放信息
        x_shifts_per_image = x_shifts[0] * expanded_strides_per_image   # 一维张量x_shifts_per_image储存每个锚点/预测框相对于原图的左上角x坐标
        y_shifts_per_image = y_shifts[0] * expanded_strides_per_image   # 一维张量y_shifts_per_image储存每个锚点/预测框相对于原图的左上角y坐标
        x_centers_per_image = (
            (x_shifts_per_image + 0.5 * expanded_strides_per_image)
            .unsqueeze(0)
            .repeat(num_gt, 1)
        )                                                               # 每个锚点/预测框在原图中的实际x坐标
        y_centers_per_image = (
            (y_shifts_per_image + 0.5 * expanded_strides_per_image)
            .unsqueeze(0)
            .repeat(num_gt, 1)
        )                                                               # 每个锚点/预测框在原图中的实际y坐标
        #--------------------Caculating Ground True----------------------#  
        gt_bboxes_per_image_l = (
            (gt_bboxes_per_image[:, 0] - 0.5 * gt_bboxes_per_image[:, 2])
            .unsqueeze(1)
            .repeat(1, total_num_anchors)
        )
        gt_bboxes_per_image_r = (
            (gt_bboxes_per_image[:, 0] + 0.5 * gt_bboxes_per_image[:, 2])
            .unsqueeze(1)
            .repeat(1, total_num_anchors)
        )
        gt_bboxes_per_image_t = (
            (gt_bboxes_per_image[:, 1] - 0.5 * gt_bboxes_per_image[:, 3])
            .unsqueeze(1)
            .repeat(1, total_num_anchors)
        )
        gt_bboxes_per_image_b = (
            (gt_bboxes_per_image[:, 1] + 0.5 * gt_bboxes_per_image[:, 3])
            .unsqueeze(1)
            .repeat(1, total_num_anchors)
        )

        b_l = x_centers_per_image - gt_bboxes_per_image_l
        b_r = gt_bboxes_per_image_r - x_centers_per_image
        b_t = y_centers_per_image - gt_bboxes_per_image_t
        b_b = gt_bboxes_per_image_b - y_centers_per_image
        bbox_deltas = torch.stack([b_l, b_t, b_r, b_b], 2)
        # print(bbox_deltas.shape)

        is_in_boxes = bbox_deltas.min(dim=-1).values > 0.0
        is_in_boxes_all = is_in_boxes.sum(dim=0) > 0
        # in fixed center
        center_radius = 2.5

        gt_bboxes_per_image_l = (gt_bboxes_per_image[:, 0]).unsqueeze(1).repeat(
            1, total_num_anchors
        ) - center_radius * expanded_strides_per_image.unsqueeze(0)
        gt_bboxes_per_image_r = (gt_bboxes_per_image[:, 0]).unsqueeze(1).repeat(
            1, total_num_anchors
        ) + center_radius * expanded_strides_per_image.unsqueeze(0)
        gt_bboxes_per_image_t = (gt_bboxes_per_image[:, 1]).unsqueeze(1).repeat(
            1, total_num_anchors
        ) - center_radius * expanded_strides_per_image.unsqueeze(0)
        gt_bboxes_per_image_b = (gt_bboxes_per_image[:, 1]).unsqueeze(1).repeat(
            1, total_num_anchors
        ) + center_radius * expanded_strides_per_image.unsqueeze(0)

        c_l = x_centers_per_image - gt_bboxes_per_image_l
        c_r = gt_bboxes_per_image_r - x_centers_per_image
        c_t = y_centers_per_image - gt_bboxes_per_image_t
        c_b = gt_bboxes_per_image_b - y_centers_per_image
        center_deltas = torch.stack([c_l, c_t, c_r, c_b], 2)
        is_in_centers = center_deltas.min(dim=-1).values > 0.0
        is_in_centers_all = is_in_centers.sum(dim=0) > 0

        # in boxes and in centers
        is_in_boxes_anchor = is_in_boxes_all | is_in_centers_all        #If one or more than one condition is satisfied

        is_in_boxes_and_center = (
            is_in_boxes[:, is_in_boxes_anchor] & is_in_centers[:, is_in_boxes_anchor]
        )
        return is_in_boxes_anchor, is_in_boxes_and_center

    def dynamic_k_matching(self, cost, pair_wise_ious, gt_classes, num_gt, fg_mask):  # 为每个真值框分配最合适的预测框
        # Dynamic K
        # ---------------------------------------------------------------
        matching_matrix = torch.zeros_like(cost, dtype=torch.uint8)

        ious_in_boxes_matrix = pair_wise_ious
        # print(ious_in_boxes_matrix)
        n_candidate_k = min(10, ious_in_boxes_matrix.size(1))
        topk_ious, _ = torch.topk(ious_in_boxes_matrix, n_candidate_k, dim=1)
        dynamic_ks = torch.clamp(topk_ious.sum(1).int(), min=1)
        for gt_idx in range(num_gt):
            _, pos_idx = torch.topk(
                cost[gt_idx], k=dynamic_ks[gt_idx].item(), largest=False
            )
            matching_matrix[gt_idx][pos_idx] = 1.0

        del topk_ious, dynamic_ks, pos_idx

        anchor_matching_gt = matching_matrix.sum(0)
        if (anchor_matching_gt > 1).sum() > 0:
            _, cost_argmin = torch.min(cost[:, anchor_matching_gt > 1], dim=0)
            matching_matrix[:, anchor_matching_gt > 1] *= 0
            matching_matrix[cost_argmin, anchor_matching_gt > 1] = 1
        fg_mask_inboxes = matching_matrix.sum(0) > 0
        num_fg = fg_mask_inboxes.sum().item()

        fg_mask[fg_mask.clone()] = fg_mask_inboxes

        matched_gt_inds = matching_matrix[:, fg_mask_inboxes].argmax(0)
        gt_matched_classes = gt_classes[matched_gt_inds]
        #gt_matched_colors = gt_colors[matched_gt_inds]

        pred_ious_this_matching = (matching_matrix * pair_wise_ious).sum(0)[
            fg_mask_inboxes
        ]
        return num_fg, gt_matched_classes, pred_ious_this_matching, matched_gt_inds

