from scipy.io import loadmat
import numpy as np


class Ldpc:
    def __init__(self, tanner_file_name):
        self.tanner_file_name = tanner_file_name
        self.check_matrix = loadmat(self.tanner_file_name)['data']
        # length of the code
        self.N = self.check_matrix[0][0]
        # number of rows of original check matrix
        self.M = self.check_matrix[0][1]
        # maximum column weight
        self.wc = self.check_matrix[1][0]
        # maximum row weight
        self.wr = self.check_matrix[1][1]
        self.var_degree = np.array(self.check_matrix[2, 0:self.N])
        self.check_degree = np.array(self.check_matrix[3, 0:self.M])
        self.var_index = np.zeros((self.N, self.wc), dtype=int)
        for n in range(self.N):
            self.var_index[n, :] = self.check_matrix[4 + n, 0:self.wc]
        self.check_index = np.zeros((self.M, self.wr), dtype=int)
        for m in range(self.M):
            self.check_index[m,
                             :] = self.check_matrix[self.N + 4 + m, 0:self.wr]

        # 校验矩阵H
        self.H = np.zeros((self.M, self.N), dtype=int)
        for m in range(self.M):
            for n in range(self.check_degree[m]):
                self.H[m, self.check_index[m, n] - 1] = 1

    def check_ldpc_code(self, codeseq):
        """检验编码后的序列是否正确"""
        sum_constraint = 0                             # 不满足监督关系式的个数
        for i in range(self.M):
            temp = 0
            for j in range(self.check_degree[i]):
                temp ^= codeseq[self.check_index[i, j] - 1]

            if temp != 0:
                sum_constraint += 1

        return sum_constraint

    def construct_generate_matrix(self):
        """通过H求解生成矩阵G"""

        # 对tempH进行高斯消去，形成tempH = [P|I]
        tempH = self.H
        col_record = list(range(self.N))                   # 记录交换列的位置
        exchange_num = 0
        for row_cnt in range(self.M - 1, -1, -1):          # 从最后一行开始
            handling_col = self.N - (self.M - row_cnt)
            row_place = row_cnt
            for row_temp in range(row_cnt, -1, -1):
                if tempH[row_temp, handling_col] == 1:
                    break
                else:
                    row_place = row_place - 1
            # if this column has not bit 1
            if row_place == -1:
                exchange_col_findflag = 0
                for exchange_col in range(handling_col - 1, -1, -1):
                    row_place = row_cnt
                    for row_temp in range(row_cnt, -1, -1):
                        if tempH[row_temp, exchange_col] == 1:
                            exchange_col_findflag = 1
                            break
                        else:
                            row_place = row_place - 1
                    if exchange_col_findflag == 1:
                        break

                if exchange_col_findflag == 1:
                    exchange_num = exchange_num + 1

                    temp = col_record[handling_col]
                    col_record[handling_col] = col_record[exchange_col]
                    col_record[exchange_col] = temp

                    temp = tempH[:, handling_col]
                    tempH[:, handling_col] = tempH[:, exchange_col]
                    tempH[:, exchange_col] = temp
                else:
                    print(
                        "error! K is not consistent with the definition! need examine the coding program!")

            if row_place != row_cnt:
                tempH[row_cnt, :] = np.bitwise_xor(
                    tempH[row_cnt, :], tempH[row_place, :])

            for row_temp in range(self.M - 1, -1, -1):
                if tempH[row_temp, handling_col] == 1 and row_temp != row_cnt:
                    tempH[row_temp, :] = np.bitwise_xor(
                        tempH[row_temp, :], tempH[row_cnt, :])
        K = self.N - self.M                                       # 信息比特长度
        P = tempH[0:self.M, 0:K]                             # 得到一个M * K阶矩阵
        Q = P.T                                         # Q是一个K * M阶矩阵
        G = np.zeros((K, self.N), dtype=int)                 # 生成G是一个K * N阶矩阵
        G[0:K, 0:K] = np.eye(K, dtype=int)
        G[:, K:] = Q
        return G


def get_ldpc_code(baseband_bit, generated_matrix):
    # generated_matrix = construct_generate_matrix()
    output_bit = np.mod(np.dot(baseband_bit, generated_matrix), 2)
    output_bit = np.array(output_bit, dtype=int)

    # test_flag = check_ldpc_code(output_bit)            # 用来测试生成的LDPC码
    # if test_flag == 1:                                 # 需要注意的是一次只能测一个码，不能一次测多个码
    #     print("error!")

    return output_bit
