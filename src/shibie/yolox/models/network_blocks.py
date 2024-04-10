#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (c) 2014-2021 Megvii Inc. All rights reserved.

import torch
import torch.nn as nn

from .coord_conv import CoordConv


class SiLU(nn.Module):
    """export-friendly version of nn.SiLU()"""

    @staticmethod
    def forward(x):
        return x * torch.sigmoid(x)

def get_activation(name="hswish", inplace=True):
    if name == "silu":
        module = nn.SiLU(inplace=inplace)
    elif name == "relu":
        module = nn.ReLU(inplace=inplace)
    elif name == "lrelu":
        module = nn.LeakyReLU(0.1, inplace=inplace)
    elif name == "hswish":
        module = nn.Hardswish(inplace=inplace)
    else:
        raise AttributeError("Unsupported act type: {}".format(name))
    return module

def channel_shuffle(x, groups=2):
    """Channel Shuffle"""

    batchsize, num_channels, height, width = x.data.size()
 
    channels_per_group = num_channels // groups
 
    # reshape
    x = x.view(batchsize, groups,
               channels_per_group, height, width)
 
    # transpose
    # - contiguous() required if transpose() is used before view().
    #   See https://github.com/pytorch/pytorch/issues/764
    x = torch.transpose(x, 1, 2).contiguous()
 
    # flatten
    x = x.view(batchsize, -1, height, width)
    
    return x

class BaseConv(nn.Module):
    """A Conv2d -> Batchnorm -> hswish/leaky relu block"""

    def __init__(
        self, in_channels, out_channels, ksize, stride, groups=1, bias=False, act="hswish", no_act=False
    ):
        super().__init__()
        # same padding
        pad = (ksize - 1) // 2
        self.conv = nn.Conv2d(
            in_channels,
            out_channels,
            kernel_size=ksize,
            stride=stride,
            padding=pad,
            groups=groups,
            bias=bias,
        )
        self.bn = nn.BatchNorm2d(out_channels)
        self.act = get_activation(act, inplace=True)
        self.no_act = no_act

    def forward(self, x):
        if self.no_act:
            return self.bn(self.conv(x))
        else:
            return self.act(self.bn(self.conv(x)))

    def fuseforward(self, x):
        return self.act(self.conv(x))


class DWConv(nn.Module):
    """Depthwise Conv + Conv"""

    def __init__(self, in_channels, out_channels, ksize, stride=1, act="hswish",no_depth_act=True):
        super().__init__()
        self.dconv = BaseConv(
            in_channels,
            in_channels,
            ksize=ksize,
            stride=stride,
            groups=in_channels,
            act=act,
            no_act = no_depth_act
        )
        self.pconv = BaseConv(
            in_channels, out_channels, ksize=1, stride=1, groups=1, act=act
        )

    def forward(self, x):
        x = self.dconv(x)
        return self.pconv(x)

# Bottleneck结构
class Bottleneck(nn.Module):
    def __init__(
        self,
        in_channels,
        out_channels,
        shortcut=True,      # 是否加入残差连接
        expansion=0.5,      # 隐藏层输出的宽度和输出层输出的宽度的比值
        depthwise=False,    # 是否使用深度可分离卷积
        act="hswish",
    ):
        super().__init__()
        hidden_channels = int(out_channels * expansion)                                 # 隐藏层
        Conv = DWConv if depthwise else BaseConv                                        # 是否使用深度可分离卷积
        self.conv1 = BaseConv(in_channels, hidden_channels, 1, stride=1, act=act)       # 普通卷积层
        self.conv2 = Conv(hidden_channels, out_channels, 3, stride=1, act=act)          # 普通卷积层/深度可分离卷积
        self.use_add = shortcut and in_channels == out_channels                         # 是否使用残差连接

    def forward(self, x):
        y = self.conv2(self.conv1(x))
        if self.use_add:                                                                # 如果使用残差连接
            y = y + x                                                                   # x与y相加操作
        return y


class ResLayer(nn.Module):
    "Residual layer with `in_channels` inputs."

    def __init__(self, in_channels: int):
        super().__init__()
        mid_channels = in_channels // 2
        self.layer1 = BaseConv(
            in_channels, mid_channels, ksize=1, stride=1, act="lrelu"
        )
        self.layer2 = BaseConv(
            mid_channels, in_channels, ksize=3, stride=1, act="lrelu"
        )

    def forward(self, x):
        out = self.layer2(self.layer1(x))
        return x + out


class SPPBottleneck(nn.Module):
    """Spatial pyramid pooling layer used in YOLOv3-SPP"""

    def __init__(
        self, in_channels, out_channels, kernel_sizes=(5, 9, 13), activation="hswish"
    ):
        super().__init__()
        hidden_channels = in_channels // 2
        self.conv1 = BaseConv(in_channels, hidden_channels, 1, stride=1, act=activation)
        self.m = nn.ModuleList(
            [
                nn.MaxPool2d(kernel_size=ks, stride=1, padding=ks // 2)
                for ks in kernel_sizes
            ]
        )
        conv2_channels = hidden_channels * (len(kernel_sizes) + 1)
        self.conv2 = BaseConv(conv2_channels, out_channels, 1, stride=1, act=activation)

    def forward(self, x):
        x = self.conv1(x)
        x = torch.cat([x] + [m(x) for m in self.m], dim=1)
        x = self.conv2(x)
        return x

# CSP层
class CSPLayer(nn.Module):                  
    """C3 in yolov5, CSP Bottleneck with 3 convolutions"""

    def __init__(
        self,
        in_channels,                        # 输入通道
        out_channels,                       # 输出通道
        n=1,                                # bottleneck层数量
        shortcut=True,                      # 是否在bottleneck里面加入残差连接
        expansion=0.5,                      # 隐藏层(输入和输出的中间层）宽度和输出层宽度比值
        depthwise=True,                    # 是否使用深度可分离卷积，每个通道分别进卷积，减小计算量
        act="hswish",                       # 激活函数hswish，相比于swish更简单
    ):
        """
        Args:
            in_channels (int): input channels.
            out_channels (int): output channels.
            n (int): number of Bottlenecks. Default value: 1.
        """
        super().__init__()
        hidden_channels = int(out_channels * expansion)                                  # 隐藏层(非输入输出层)通道数
        self.conv1 = BaseConv(in_channels, hidden_channels, 1, stride=1, act=act)        # 基本卷积层
        self.conv2 = BaseConv(in_channels, hidden_channels, 1, stride=1, act=act)
        self.conv3 = BaseConv(2 * hidden_channels, out_channels, 1, stride=1, act=act)
        module_list = [
            Bottleneck(
                hidden_channels, hidden_channels, shortcut, 1.0, depthwise, act=act
            )                                                                            # 多个Bottleneck层
            for _ in range(n)
        ]
        self.m = nn.Sequential(*module_list)

    def forward(self, x):
        x_1 = self.conv1(x)                 # 通过conv1普通卷积层
        x_2 = self.conv2(x)                 # 通过conv2普通卷积层
        x_1 = self.m(x_1)                   # 通过多个Bottleneck层
        x = torch.cat((x_1, x_2), dim=1)    # concat操作，深度上相融
        return self.conv3(x)                # 经过conv3

class Focus(nn.Module):
    """Focus width and height information into channel space."""

    def __init__(self, in_channels, out_channels, ksize=1, stride=1, depthwise=False, act="hswish"):
        super().__init__()
        Conv = DWConv if depthwise else BaseConv
        self.conv = Conv(in_channels * 4, out_channels, ksize, stride, act=act)

    def forward(self, x):
        # shape of x (b,c,w,h) -> y(b,4c,w/2,h/2)
        patch_top_left = x[..., ::2, ::2]
        patch_top_right = x[..., ::2, 1::2]
        patch_bot_left = x[..., 1::2, ::2]
        patch_bot_right = x[..., 1::2, 1::2]
        x = torch.cat(
            (
                patch_top_left,
                patch_bot_left,
                patch_top_right,
                patch_bot_right,
            ),
            dim=1,
        )
        return self.conv(x)

class ShuffleV2DownSampling(nn.Module):
    def __init__(self, in_channels, out_channels, c_ratio=0.5, groups=2, act="hswish"):
        super().__init__()
        self.groups = groups
        self.l_channels = int(in_channels * c_ratio)
        self.r_channels = in_channels - self.l_channels
        self.o_r_channels = out_channels - self.l_channels
        
        self.dwconv_l = DWConv(in_channels, self.l_channels,ksize=3,stride=2,act=act,no_depth_act=True)
        self.conv_r1 = BaseConv(in_channels, self.r_channels,ksize=1,stride=1,act=act)
        self.dwconv_r = DWConv(self.r_channels,self.o_r_channels,ksize=3,stride=2,act=act,no_depth_act=True)

    def forward(self, x):
        out_l = self.dwconv_l(x)

        out_r = self.conv_r1(x)
        out_r = self.dwconv_r(out_r)
        x = torch.cat((out_l, out_r), dim=1)
        return channel_shuffle(x,self.groups)

#TODO:Add SE Block Support
class ShuffleV2Basic(nn.Module):
    def __init__(self, in_channels, out_channels, ksize=3,stride=1, c_ratio=0.5, groups=2, act="hswish",type=""):
        super().__init__()
        self.in_channels = in_channels
        self.l_channels = int(in_channels * c_ratio)
        self.r_channels = in_channels - self.l_channels
        self.o_r_channels = out_channels - self.l_channels

        self.groups = groups
        self.conv_r1 = BaseConv(self.r_channels, self.o_r_channels, ksize=1, stride=stride, act=act)
        self.dwconv_r = DWConv(self.o_r_channels, self.o_r_channels,ksize=ksize, stride=stride, act=act, no_depth_act=True)

    def forward(self, x):
        x_l = x[:, :self.l_channels, :, :]
        x_r = x[:, self.l_channels:, :, :]
        out_r = self.conv_r1(x_r)
        out_r = self.dwconv_r(out_r)

        x = torch.cat((x_l, out_r), dim=1)

        return channel_shuffle(x,self.groups)

class ShuffleV2Reduce(nn.Module):
    def __init__(self, in_channels, out_channels, ksize=3, stride=1, c_ratio=0.5, groups=2, act="hswish"):
        super().__init__()
        self.in_channels = in_channels
        self.l_channels = int(out_channels * c_ratio)
        self.r_channels = in_channels - self.l_channels
        self.o_r_channels = out_channels - self.l_channels

        self.groups = groups
        self.conv_r1 = BaseConv(self.r_channels, self.o_r_channels, ksize=1, stride=stride, act=act)
        self.dwconv_r = DWConv(self.o_r_channels, self.o_r_channels,ksize=ksize, stride=stride, act=act, no_depth_act=True)

    def forward(self, x):
        
        x = channel_shuffle(x,self.groups)
        
        x_l = x[:, :self.l_channels, :, :]
        x_r = x[:, self.l_channels:, :, :]
        out_r = self.conv_r1(x_r)
        out_r = self.dwconv_r(out_r)
        
        x = torch.cat((x_l, out_r), dim=1)
        
        return channel_shuffle(x,self.groups)

class ShuffleV2ReduceBlock(nn.Module):
    def __init__(self, in_channels, out_channels, ksize=3, stride=1, c_ratio=0.5, repeat=2, groups=2, act="hswish",type=""):
        super().__init__()
        # self.conv1 = DWConv(in_channels, out_channels, ksize=ksize)
        self.conv1 = ShuffleV2Reduce(in_channels, out_channels, ksize=ksize, c_ratio=c_ratio, groups=groups, act=act)
        self.shuffle_blocks_list = []

        for _ in range(repeat):
            self.shuffle_blocks_list.append(ShuffleV2Basic(out_channels, out_channels, ksize, act=act))
        self.shuffle_blocks = nn.Sequential(*self.shuffle_blocks_list)

    def forward(self, x):
        x = self.conv1(x)
        x = self.shuffle_blocks(x)

        return x