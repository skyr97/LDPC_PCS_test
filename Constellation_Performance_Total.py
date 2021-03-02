# -*- coding:utf-8 -*-
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
import scipy.io as sio
from scipy.io import loadmat
import fractions
import os
from Gaussian_elimination import get_ldpc_code, construct_generate_matrix
from Conventional_NMS import decode_algorithm_NMS
from collections.abc import Iterable
np.set_printoptions(threshold=np.inf)
np.random.seed(137)

# 该版本支持加5G LDPC, 概率解调, 不支持普通LDPC码, 因为普通LDPC码不需要打孔
# glob_ModOrder = 16
# data = pd.read_csv('QAM_Gray_Mapping/NR_16QAM.txt', header=None, sep='\s+')
# constellation_real = np.reshape(np.array(data[[3]]), glob_ModOrder)
# constellation_image = np.reshape(np.array(data[[5]]), glob_ModOrder)
# l_dict = sio.loadmat("tmp_prob_cons6.8.mat")
# constellation_real = l_dict["cons"][:,0].reshape([-1])
# constellation_image = l_dict["cons"][:,1].reshape([-1])
# l_dict = sio.loadmat("./结果1_比较好的星座图_ZLH/16QAM/learning_qam16.mat")
# constellation_real = l_dict["deep_qam16"][:,0].reshape([-1])
# constellation_image = l_dict["deep_qam16"][:,1].reshape([-1])
# LDPC码设置
# LDPC_flag = 1                      # 0 --- 不加LDPC码, 1 --- 加LDPC码
# # 5G LDPC码长, 该程序只接受传输码长是log2(ModOrder)的倍数, 否则就需要补0, 我不想写
# glob_ldpc_length = 1104
# glob_trans_ldpc_length = 1056      # 实际信道中传输比特的长度, 5G LDPC码需要打孔前两列
# glob_information_length = 528      # 信息比特长度
# glob_Z = 24                        # QC矩阵中扩展因子Z, 该参数大小决定了打孔比特的长度

# # 保存文件
# NoLDPC_filename = 'ceshi.txt'
# LDPC_filename = 'ceshi_ldpc_gallager.txt'


class ConstellationPerformanceTotal:
    def __init__(self, modOrder, constellation_real, constellation_image, prob, ldpc_length, trans_ldpc_length, information_length, QC_Z, snr_list):
        self.ModOrder = modOrder
        self.bitsPerSym = int(math.log2(self.ModOrder))
        self.Cons_Re = constellation_real
        self.Cons_Im = constellation_image
        self.prob = prob
        self.prob_quadra = self.prob[0:len(self.prob)//4]
        if not isinstance(prob, np.ndarray):
            self.prob = np.array(prob)
        self.prob = self.prob.reshape([-1])
        self.ldpc_length = ldpc_length
        if isinstance(snr_list, Iterable):
            self.snr_list = list(snr_list)
        else:
            self.snr_list = [snr_list]

        # LDPC码设置 (设置5G LDPC码的参数)
        # 是否加LDPC码 (0-No!, 1-Yes!)
        self.LDPC_flag = LDPC_flag
        self.LDPC_Len = glob_ldpc_length                                     # 码长
        self.trans_ldpc_length = trans_ldpc_length                         # 实际传输比特
        self.information_Len = information_length                       # 信息比特长度
        # self.LDPC_code_rate = self.information_Len / self.trans_ldpc_length     # 码率
        self.ldpc_code_rate = fractions.Fraction(
            self.information_Len, self.trans_ldpc_length)
        self.ldpc_code_rate: fractions.Fraction
        # 保存文件名
        self.NoLDPC_filename = NoLDPC_filename
        self.LDPC_filename = LDPC_filename

    def _probability_shaping(self):

        self.prob = self.prob/np.sum(self.prob)
        self.prob_quadra = self.prob_quadra/np.sum(self.prob_quadra)
        # self.ps_value = np.ones(self.ModOrder, dtype=float)
        # self.ps_value = prob
        # # 融合2个点
        # fuse_2points = [0, 12, 8, 10, 4, 5, 24, 26, 16, 28, 20, 21, 52, 53, 48, 60, 56, 58, 40, 42, 32, 44, 36, 37]
        # # # 融合3个点
        # fuse_3points = [1, 2, 3, 17, 18, 19, 49, 50, 51, 33, 34, 35]
        # for i in range(self.ModOrder):
        #     if i in fuse_2points:
        #         self.ps_value[i] = 0.5
        #     elif i in fuse_3points:
        #         self.ps_value[i] = 1 / 3

        # fuse_points = [62, 30, 28, 60, 56, 24, 40, 8, 44, 12, 46, 14, 42, 10, 26, 58]
        # for i in range(self.ModOrder):
        #     if i in fuse_points:
        #         self.ps_value[i] = 0.5

    def _record_index(self):
        """记录星座点中每个比特为0和1时对应的符号"""
        self.list_zero = []                         # 记录比特为0的星座点的索引, 维度为[bitsPerSym, ModOrder / 2]
        # 记录比特为1的星座点的索引, 维度为[bitsPerSym, ModOrder / 2]
        self.list_one = []
        for i in range(self.bitsPerSym):
            self.list_zero.append([])
            self.list_one.append([])

        # 生成 0 ~ ModOrder - 1 的比特, 例[0000]
        source_bit = np.zeros((self.ModOrder, self.bitsPerSym), dtype=int)
        for i in range(self.ModOrder):
            temp_source_bit = np.zeros((1, self.bitsPerSym), dtype=int)
            for j in range(self.bitsPerSym):
                temp_source_bit[0][self.bitsPerSym -
                                   1 - j] = int(i / math.pow(2, j)) % 2
            source_bit[i, :] = temp_source_bit[:]

        for i in range(self.ModOrder):
            for j in range(self.bitsPerSym):
                if source_bit[i][j] == 0:
                    self.list_zero[j].append(i)
                else:
                    self.list_one[j].append(i)

        self.list_zero = np.array(self.list_zero, dtype=int)
        self.list_one = np.array(self.list_one, dtype=int)

    def calcu_ebn0(self, esn0: float):
        eq_prob = np.ones(self.ModOrder)
        eq_prob = eq_prob/np.sum(eq_prob)
        H1 = -np.sum(eq_prob*np.log(eq_prob))
        H2 = -np.sum(self.prob*np.log(self.prob))
        R2 = H2/H1
        ebn0 = esn0-10*math.log10(self.bitsPerSym*self.ldpc_code_rate*R2)
        return ebn0

    def constellation_norm(self):
        """星座归一化"""
        power = 0.0
        for i in range(self.ModOrder):
            power += (self.Cons_Re[i] ** 2 + self.Cons_Im[i] ** 2)*self.prob[i]
        print("Suppose Average Power is: " + "1")
        print("Actual Power is: " + str(power))
        self.Cons_Re = self.Cons_Re / np.sqrt(power)
        self.Cons_Im = self.Cons_Im / np.sqrt(power)

    def mod(self, msg):
        """取模值, 将用户传输的比特转换为(0 ~ ModOrder - 1)之间的值"""
        # msg的维度为(1, bitsPerSym), 二维数组形式; 假设8QAM, 输入[[0, 1, 1]], 输出3
        count = 0
        for i in range(self.bitsPerSym):
            count += msg[0][i] * (2 ** (self.bitsPerSym - 1 - i))

        return count

    def mapping(self, count):
        """实现星座映射"""
        map_sig = np.zeros((1, 2), dtype=float)
        map_sig[0][0] = self.Cons_Re[count]
        map_sig[0][1] = self.Cons_Im[count]

        return map_sig

    def channel_awgn(self, tx_spread, noise_sigma):
        """加入高斯白噪声"""
        rx_spread = tx_spread + noise_sigma * np.random.randn(1, 2)

        return rx_spread

    def demodulation(self, rx_spread, noise_sigma):
        """实现解调功能, 这个函数可以得到比特软量, 这个函数是传统log-MAP算法, 可以用于概率Shaping中"""
        var = math.pow(noise_sigma, 2) * \
            2         # 噪声方差, notice 噪声加的方差是对应实部或虚部的2倍, 切记不能用**
        # 计算解调器得到的LLR信息
        demod_out_llr = np.zeros((1, self.bitsPerSym), dtype=float)
        for i in range(self.bitsPerSym):
            bit0_add = 0
            bit1_add = 0
            for j in range(int(self.ModOrder / 2)):
                temp_index_bit0 = self.list_zero[i, j]
                bit0_add += self.prob[temp_index_bit0] * 1.0 / np.pi / var * np.exp(-1 * (math.pow(
                    rx_spread[0][0] - self.Cons_Re[temp_index_bit0], 2) + math.pow(rx_spread[0][1] - self.Cons_Im[temp_index_bit0], 2)) / var)
                temp_index_bit1 = self.list_one[i, j]
                bit1_add += self.prob[temp_index_bit1] * 1.0 / np.pi / var * np.exp(-1 * (math.pow(
                    rx_spread[0][0] - self.Cons_Re[temp_index_bit1], 2) + math.pow(rx_spread[0][1] - self.Cons_Im[temp_index_bit1], 2)) / var)

            # 为了防止出现除0操作
            if bit0_add < 1e-100:
                temp_llr = np.log((bit0_add + 1e-300) / bit1_add)
            elif bit1_add < 1e-100:
                temp_llr = np.log(bit0_add / (bit1_add + 1e-300))
            else:
                temp_llr = np.log(bit0_add / bit1_add)

            demod_out_llr[0, i] = temp_llr

        if self.LDPC_flag == 0:
            # 硬判决
            demod_out_hard_decision = np.where(demod_out_llr > 0, 0, 1)
            return demod_out_hard_decision
        else:
            # 软解调
            return demod_out_llr

    def run_no_ldpc(self, msg, noise_sigma):
        """这个函数用于没有加LDPC码的系统, 输出是硬判决的值"""
        tx_mod = self.mod(msg)
        tx_spread = self.mapping(tx_mod)
        rx_spread = self.channel_awgn(tx_spread, noise_sigma)
        rec_bit = self.demodulation(rx_spread, noise_sigma)

        return rec_bit

    def run_ldpc(self, msg, noise_sigma):
        """这个函数用于加LDPC码的系统, 输出是软解调的LLR信息"""
        tx_mod = self.mod(msg)
        tx_spread = self.mapping(tx_mod)
        rx_spread = self.channel_awgn(tx_spread, noise_sigma)
        rec_bit_llr = self.demodulation(rx_spread, noise_sigma)

        return rec_bit_llr

    def test_no_ldpc(self):
        """该函数是测试不加LDPC码的系统性能"""
        self._record_index()
        self._probability_shaping()
        self.constellation_norm()
        for EbN0 in range(0, 11):
            total_symbol = 0
            error_symbol = 0
            error_bit = 0
            flag = True
            print("EbN0 = " + str(EbN0))
            while flag:
                total_symbol += 1
                snr = EbN0 + 10 * np.log10(self.bitsPerSym)
                noise_sigma = np.sqrt(0.5 / math.pow(10, snr / 10))
                trans_bit = np.random.randint(0, 2, (1, self.bitsPerSym))
                rec_bit = self.run_no_ldpc(trans_bit, noise_sigma)
                if np.sum(np.abs(rec_bit - trans_bit)) == 0:
                    error_symbol += 0
                    error_bit += 0
                else:
                    error_symbol += 1
                    error_bit += np.sum(np.abs(rec_bit - trans_bit))

                if error_symbol >= 2000 and total_symbol >= 50000:
                    flag = False
                if total_symbol % 5000 == 0:
                    temp_ser = error_symbol / total_symbol
                    temp_ber = error_bit / (total_symbol * self.bitsPerSym)
                    print("temp_ser = " + str(temp_ser) +
                          ", temp_ber = " + str(temp_ber))

            ser = error_symbol / total_symbol
            ber = error_bit / (total_symbol * self.bitsPerSym)
            print("SER = " + str(ser) + ", BER = " + str(ber))
            print("\n")
            f1 = open(self.NoLDPC_filename, 'a')
            f1.write("\n")
            f1.write("EbN0 = " + str(EbN0) + ", SER = " +
                     str(ser) + ", BER = " + str(ber))
            f1.write("\n")
            f1.close()

    def msg_bit_gen(self):
        info_bits_per_sym = self.bitsPerSym-2
        info_order = self.ModOrder//4
        src = np.random.choice(
            np.arange(info_order), p=self.prob_quadra, size=self.information_Len//info_bits_per_sym)
        msg_bit = np.zeros(shape=[len(src), info_bits_per_sym])
        for i in range(info_bits_per_sym-1, -1, -1):
            msg_bit[:, i] = src % 2
            src //= 2
        msg_bit = msg_bit.reshape([1, -1])
        return msg_bit

    def test_ldpc(self):
        """该函数是测试加LDPC码的系统性能"""
        self._record_index()
        self._probability_shaping()
        self.constellation_norm()
        save_count = self.trans_ldpc_length // self.bitsPerSym    # 保存需要传输多少次
        generated_matrix = construct_generate_matrix()             # 获得生成矩阵
        for snr in self.snr_list:
            total_frame = 0
            error_frame = 0
            error_bit = 0
            flag = True
            print("EsN0 = " + str(snr))
            while flag:
                total_frame += 1
                noise_sigma = np.sqrt(0.5 / math.pow(10, snr / 10))
                msg_bit = self.msg_bit_gen()  # 按概率产生符号，再转换成信息比特
                # msg_bit = np.random.randint(
                #     0, 2, (1, self.information_Len))    # 产生信息比特流
                trans_bit = get_ldpc_code(
                    msg_bit, generated_matrix)            # 产生LDPC码
                actual_trans_bit = trans_bit[:, :-2 * glob_Z]
                actual_trans_bit = self.ldpc_pcs_rearray_encode(
                    actual_trans_bit)
                # rearray_trans_bit_decode = self.ldpc_pcs_rearray_decode(rearray_trans_bit)
                rec_dims = np.zeros((save_count, self.bitsPerSym), dtype=float)
                for i in range(save_count):
                    temp_actual_trans_bit = actual_trans_bit[:,
                                                             self.bitsPerSym * i: self.bitsPerSym * (i + 1)]
                    temp_rec_bit_llr = self.run_ldpc(
                        temp_actual_trans_bit, noise_sigma)
                    rec_dims[i, :] = temp_rec_bit_llr[:]

                # 得到解调器的输出
                total_rec_bit_llr = np.squeeze(np.reshape(
                    rec_dims, (-1, self.trans_ldpc_length)))  # 降维, 变成一维
                total_rec_bit_llr = self.ldpc_pcs_rearray_decode(
                    total_rec_bit_llr)
                # 补上打孔的
                ldpc_in_llr = np.zeros(self.LDPC_Len, dtype=float)
                ldpc_in_llr[:-2 * glob_Z] = total_rec_bit_llr

                # LDPC译码
                ldpc_out_llr = decode_algorithm_NMS(ldpc_in_llr)

                # 取信息比特
                decode_information_bit = np.reshape(
                    ldpc_out_llr[0:self.information_Len], (1, self.information_Len))

                temp_error_num = np.sum(
                    np.abs(decode_information_bit - msg_bit))

                if temp_error_num == 0:
                    error_frame += 0
                    error_bit += 0
                else:
                    error_frame += 1
                    error_bit += temp_error_num

                if error_frame >= 100 and total_frame >= 1000:
                    flag = False

                if total_frame % 20 == 0:
                    temp_fer = error_frame / total_frame
                    temp_ber = error_bit / (total_frame * self.information_Len)
                    print("temp_fer = " + str(temp_fer) +
                          ", temp_ber = " + str(temp_ber))

            fer = error_frame / total_frame
            ber = error_bit / (total_frame * self.information_Len)
            ebn0 = self.calcu_ebn0(snr)
            print("fer = " + str(fer) + ", ber = " + str(ber))
            print("\n")
            f1 = open(self.LDPC_filename, 'a')
            f1.write("\n")
            # f1.write("EsN0 = " + str(snr) + ", FER = " +
            #          str(fer) + ", BER = " + str(ber))
            f1.write("EsN0 = {esn0}, EbN0 = {ebn0}, FER = {fer}, BER = {ber}".format(esn0=snr,ebn0=ebn0,fer=fer,ber=ber))
            f1.write("\n")
            f1.close()

    def evaluate(self):
        if self.LDPC_flag == 1:
            self.test_ldpc()
        else:
            self.test_no_ldpc()

    def ldpc_pcs_rearray_encode(self, code_bits: np.ndarray):
        """
        在PCS中, 仅设计单个象限内的星座位置与概率, 由高位的2bit冗余位决定符号位于哪个象限, 低位的信息bit决定符号在象限中的位置
        经过系统LDPC编码后, 编码序列code_bits前N位是信息位.
        该函数将冗余位中每2bits与信息位中每个符号配对, 重排编码序列code_bits
        """
        rate_dic = {16: fractions.Fraction(2, 4), 64: fractions.Fraction(
            4, 6), 256: fractions.Fraction(6, 8)}
        if self.ldpc_code_rate != rate_dic[self.ModOrder]:
            raise ValueError(
                "the LDPC code rate must be {numerator}/{denom} if the modulation order is {modOrder},\
                     but {numerator2}/{denom2} is given".format(numerator=rate_dic[self.ModOrder].numerator,
                                                                denom=rate_dic[self.ModOrder].denominator,
                                                                modOrder=self.ModOrder, numerator2=self.ldpc_code_rate.numerator,
                                                                denom2=self.ldpc_code_rate.denominator))
        shape = code_bits.shape
        code_bits = code_bits.reshape([-1])
        code_len = len(code_bits)
        msg_len = int(code_len*self.ldpc_code_rate)
        res = np.zeros(shape=[code_len], dtype=code_bits.dtype)
        sign_step = 2
        msg_step = self.ldpc_code_rate.numerator*2
        i, j, k = 0, msg_len, 0
        while j < code_len:
            res[k:k+sign_step] = code_bits[j:j+sign_step]
            res[k+sign_step:k+sign_step+msg_step] = code_bits[i:i+msg_step]
            k = k+msg_step+sign_step
            j += sign_step
            i += msg_step
        res = res.reshape(shape)
        return res

    def ldpc_pcs_rearray_decode(self, rec_bits: np.ndarray):
        """
        该函数是函数ldpc_pcs_rearray_encode的逆操作
        """
        size = rec_bits.shape
        rec_bits = rec_bits.reshape([-1])
        code_len = len(rec_bits)
        msg_len = int(code_len*self.ldpc_code_rate)
        msg_step = self.ldpc_code_rate.numerator*2
        sign_step = 2
        res = np.zeros(shape=[code_len], dtype=rec_bits.dtype)
        res: np.ndarray
        i, j, sign_ptr, msg_ptr = 0, msg_len, 0, sign_step
        while j < code_len:
            res[i:i+msg_step] = rec_bits[msg_ptr:msg_ptr+msg_step]
            msg_ptr = msg_ptr+msg_step+sign_step
            i += msg_step
            res[j:j+sign_step] = rec_bits[sign_ptr:sign_ptr+sign_step]
            sign_ptr = sign_ptr+msg_step+sign_step
            j += sign_step
        res = res.reshape(size)
        return res


if __name__ == '__main__':
    modOrder = 16
    snr = float(input("snr:"))

    data = pd.read_csv('QAM_Gray_Mapping/NR_16QAM.txt', header=None, sep='\s+')
    constellation_real = np.reshape(np.array(data[[3]]), modOrder)
    constellation_image = np.reshape(np.array(data[[5]]), modOrder)
    prob = np.ones(shape=modOrder, dtype=np.float32)/modOrder

    # matpath = "./images/modOrder16/"
    
    # order = 16
    # filename = "snr{snr:.2f}_order{M}.mat".format(snr=snr, M=order)
    # cons_l_dict = loadmat(os.path.join(matpath, filename))

    # cons = cons_l_dict["cons"]
    # prob = cons_l_dict["prob"].reshape([-1])
    # constellation_real = cons[:, 0].reshape([-1])
    # constellation_image = cons[:, 1].reshape([-1])

    LDPC_flag = 1                      # 0 --- 不加LDPC码, 1 --- 加LDPC码
    # 5G LDPC码长, 该程序只接受传输码长是log2(ModOrder)的倍数, 否则就需要补0, 我不想写
    glob_ldpc_length = 1104
    glob_trans_ldpc_length = 1056      # 实际信道中传输比特的长度, 5G LDPC码需要打孔前两列
    glob_information_length = 528      # 信息比特长度
    glob_Z = 24                        # QC矩阵中扩展因子Z, 该参数大小决定了打孔比特的长度

    # 保存文件
    NoLDPC_filename = 'ceshi.txt'
    LDPC_filename = 'ceshi_ldpc_gallager.txt'

    # prob = sio.loadmat("tmp_prob_cons6.8.mat")['prob'].reshape([-1])
    Conventional_test = ConstellationPerformanceTotal(
        modOrder=16, constellation_real=constellation_real, constellation_image=constellation_image, prob=prob,
        ldpc_length=glob_ldpc_length, trans_ldpc_length=glob_trans_ldpc_length, information_length=glob_information_length,
        QC_Z=glob_Z, snr_list=snr)

    # plt.scatter(constellation_real, constellation_image)
    # sn = list(range(modOrder))
    # for i in range(modOrder):
    #     marker = ""
    #     sym = i
    #     for _ in range(int(math.log2(modOrder))):
    #         marker = str(sym % 2)+marker
    #         sym //= 2
    #     marker = "$"+marker+"$"

    #     plt.scatter(
    #         constellation_real[i], constellation_image[i], s=400, marker=marker, c='r')
    # plt.show()
    Conventional_test.evaluate()
