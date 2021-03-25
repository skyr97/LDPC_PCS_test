# -*- coding:utf-8 -*-
from Constellation_Performance_Total import *
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
from scipy.io import loadmat
import fractions
import os
from ldpc_matrix import Ldpc, get_ldpc_code
from datetime import datetime
import comm_operation as comm

if __name__=="__main__":
    modOrder = int(input("输入调制阶数(16,64,暂不支持256):"))
    if modOrder not in {16, 64}:
        raise ValueError("只能选择16或64")
    ebn0_flag = comm.input_bool(input("是否ebn0(y/n):"))
    geometric_flag = False
    if not ebn0_flag:
        matpath = "./images/modOrder%d/" % modOrder
        files = os.listdir(matpath)
        files.sort()
        print("如果使用esn0, 请对照以下文件输入对应的esn0:")
        for f in files:
            if os.path.splitext(f)[1] == ".mat":
                print(f)
    else:
        geometric_flag = comm.input_bool(input("是否使用几何shaping的星座(y/n):"))
        if geometric_flag:
            matpath = "./geometric_shape/M%s/"%modOrder
            files = os.listdir(matpath)
            files.sort()
            print("如果仿真几何shaping的性能, 对照以下文件输入对应的esn0:")
            for f in files:
                if os.path.splitext(f)[1] == ".mat":
                    print(f)
                    
    snr_begin = float(input("输入ebn0起点:")) if ebn0_flag else float(input("输入esn0起点:"))
    snr_step = float(input("输入ebn0步长:")) if ebn0_flag else float(input("输入esn0步长:"))
    snr_end = float(input("输入ebn0停止点:")) if ebn0_flag else float(input("输入esn0停止点:"))
    snr = snr_begin
    st = datetime.now()
    log_path = "./log"
    log_name = "g{}.log".format(st.strftime("%m%d_%H%M%S"))
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    comm.redirect2log(os.path.join(log_path, log_name))
    while snr<=snr_end:
        mt = datetime.now()
        simulation_ldpc(modOrder=modOrder, snr=snr, ebn0_flag=ebn0_flag,geometric_flag=geometric_flag)
        et = datetime.now()
        print("current step run time:", et - mt)
        snr+=snr_step
    end_time = datetime.now()
    print("run time:",end_time-st)