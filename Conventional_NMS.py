import scipy.io as sio
import numpy as np

filename = 'LDPC_matrix/format_mat/Tanner_R1-2_Z24_BG1.mat'
data = sio.loadmat(filename)
BG1 = data['data']

N = BG1[0][0]                                    # length of the code
M = BG1[0][1]                                    # number of rows of original check matrix
wc = BG1[1][0]                                   # maximum column weight
wr = BG1[1][1]                                   # maximum row weight
var_degree = np.array(BG1[2, 0:N])
check_degree = np.array(BG1[3, 0:M])
var_index = np.zeros((N, wc), dtype=int)
for n in range(N):
    var_index[n, :] = BG1[4 + n, 0:wc]
check_index = np.zeros((M, wr), dtype=int)
for m in range(M):
    check_index[m, :] = BG1[N + 4 + m, 0:wr]


def check_ldpc_code(codeseq):                    # codeseq是一个N长度的LDPC码
    """"检验解码是否正确"""
    sum_constraint = 0                           # 不满足监督关系式的个数
    for i in range(M):
        temp = 0
        for j in range(check_degree[i]):
            temp ^= codeseq[check_index[i, j] - 1]

        if temp != 0:
            sum_constraint += 1

    return sum_constraint


def decode_algorithm_NMS(bitsoft):               # bitsoft是软信息
    """MinSum算法"""
    alpha = 0.75                                    # NMS算法的系数
    outseq = np.zeros(N, dtype=int)
    max_iteration = 30                           # 迭代次数

    # hard decision
    for i in range(N):
        if bitsoft[i] > 0:
            outseq[i] = 0
        else:
            outseq[i] = 1
    if check_ldpc_code(outseq) == 0:
        return outseq

    # NMS Algorithm
    p = np.array(bitsoft, dtype=float)          # 初始化最大似然后验概率
    r = np.zeros((M, wr), dtype=float)          # 初始化校验节点传向变量节点的消息

    for k in range(max_iteration):
        p1 = p
        p = np.zeros(N, dtype=float)
        for i in range(M):
            sign = 1
            pos = -1
            min1 = 1e10       # 最小值
            min2 = 1e10       # 次最小值
            sgn_value = []

            for j in range(check_degree[i]):
                tempd = p1[check_index[i, j] - 1] - r[i, j]
                if tempd < 0:
                    sgn_value.append(-1)
                    sign = 0 - sign
                    tempd = 0 - tempd
                else:
                    sgn_value.append(1)
                if tempd < min1:
                    min2 = min1
                    min1 = tempd
                    pos = j
                else:
                    if tempd < min2:
                        min2 = tempd

            for j in range(check_degree[i]):
                if j == pos:
                    r[i, j] = min2 * alpha
                else:
                    r[i, j] = min1 * alpha
                r[i, j] = sign * sgn_value[j] * r[i, j]
                p[check_index[i, j] - 1] += r[i, j]

        # hard decision
        for i in range(N):
            p[i] = p[i] + bitsoft[i]
            if p[i] > 0:
                outseq[i] = 0
            else:
                outseq[i] = 1

        if check_ldpc_code(outseq) == 0:
            break

    return outseq
