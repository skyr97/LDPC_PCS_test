import scipy.io as sio
import numpy as np

filename = 'LDPC_matrix/format_mat/Tanner_R2-3_Z32_BG1.mat'
data = sio.loadmat(filename)
check_matrix = data['data']                        # 存储校验矩阵的信息，根据txt文件

N = check_matrix[0][0]                             # length of the code
M = check_matrix[0][1]                             # number of rows of original check matrix
wc = check_matrix[1][0]                            # maximum column weight
wr = check_matrix[1][1]                            # maximum row weight
var_degree = np.array(check_matrix[2, 0:N])
check_degree = np.array(check_matrix[3, 0:M])
var_index = np.zeros((N, wc), dtype=int)
for n in range(N):
    var_index[n, :] = check_matrix[4 + n, 0:wc]
check_index = np.zeros((M, wr), dtype=int)
for m in range(M):
    check_index[m, :] = check_matrix[N + 4 + m, 0:wr]


H = np.zeros((M, N), dtype=int)                    # 校验矩阵H
for m in range(M):
    for n in range(check_degree[m]):
        H[m, check_index[m, n] - 1] = 1


def check_ldpc_code(codeseq):
    """检验编码后的序列是否正确"""
    sum_constraint = 0                             # 不满足监督关系式的个数
    for i in range(M):
        temp = 0
        for j in range(check_degree[i]):
            temp ^= codeseq[check_index[i, j] - 1]

        if temp != 0:
            sum_constraint += 1

    return sum_constraint


def construct_generate_matrix():
    """通过H求解生成矩阵G"""
    global exchange_col
    tempH = H                                     # 对tempH进行高斯消去，形成tempH = [P|I]
    col_record = list(range(N))                   # 记录交换列的位置
    exchange_num = 0
    for row_cnt in range(M - 1, -1, -1):          # 从最后一行开始
        handling_col = N - (M - row_cnt)
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
                print("error! K is not consistent with the definition! need examine the coding program!")

        if row_place != row_cnt:
            tempH[row_cnt, :] = np.bitwise_xor(tempH[row_cnt, :], tempH[row_place, :])

        for row_temp in range(M - 1, -1, -1):
            if tempH[row_temp, handling_col] == 1 and row_temp != row_cnt:
                tempH[row_temp, :] = np.bitwise_xor(tempH[row_temp, :], tempH[row_cnt, :])

    K = N - M                                       # 信息比特长度
    P = tempH[0:M, 0:K]                             # 得到一个M * K阶矩阵
    Q = P.T                                         # Q是一个K * M阶矩阵
    G = np.zeros((K, N), dtype=int)                 # 生成G是一个K * N阶矩阵
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


# trans_bit = np.random.randint(0, 2, (5, 60))
# print(trans_bit)
# trans_ldpc = get_ldpc_code(trans_bit)
# print(trans_ldpc)
