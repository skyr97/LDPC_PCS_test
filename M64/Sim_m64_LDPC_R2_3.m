clc;
clear;

%% 
% 译码算法采用NMS算法，迭代40次，校正因子设置为0.75，错误帧数为200帧
% R = 2/3，信息比特长度为2112，扩展因子Z = 96，码长为3360
% 针对调制阶数为64，此时Bit-AE网络的星座取6dB

NR_64QAM_SNR = 13:0.2:14.4;
NR_64QAM_BER = [1.198e-01, 1.086e-01, 9.196e-02, 6.773e-02, 3.728e-02, 1.341e-02, 3.276e-03, 3.823e-04];

APSK_42_SNR = 12.6:0.2:14.2;
APSK_42_BER = [1.173e-01, 1.044e-01, 8.542e-02, 6.084e-02, 3.482e-02, 1.473e-02, 4.291e-03, 8.168e-04, 1.218e-04];

ATSC_64NUC_R10_15_SNR = 12.6:0.2:14;
ATSC_64NUC_R10_15_BER = [1.146e-01, 1.016e-01, 8.216e-02, 5.457e-02, 2.770e-02, 9.299e-03, 2.064e-03, 2.772e-04];

Bit_AE_M64_EbN0_6dB_SNR = 12.6:0.2:14;
Bit_AE_M64_EbN0_6dB_BER = [1.158e-01, 1.012e-01, 7.957e-02, 5.196e-02, 2.707e-02, 9.170e-03, 2.086e-03, 3.251e-04];

%% 画图
semilogy(NR_64QAM_SNR(3:end), NR_64QAM_BER(3:end), 'o-k', 'Linewidth', 1.2);
hold on;

semilogy(APSK_42_SNR(3:end), APSK_42_BER(3:end), '<-', 'Linewidth', 1.2, 'Color', [1, 0.38, 0]);
hold on;

semilogy(ATSC_64NUC_R10_15_SNR(3:end), ATSC_64NUC_R10_15_BER(3:end), 's-b', 'Linewidth', 1.2);
hold on;

semilogy(Bit_AE_M64_EbN0_6dB_SNR, Bit_AE_M64_EbN0_6dB_BER, 'h-', 'Linewidth', 1.2, 'Color', [1, 0, 1]);
hold on;


%% 设置坐标
set(gca, 'xlim', [13, 14.4], 'xtick', [13:0.05:14.4]);
set(gca, 'ylim', [10^-4, 10^-0]);
grid on;
h1 = legend('64QAM', '64APSK(4,2)', '64NUC-ATSC3.0(R=10/15)', 'Bit-AE(64,EbN0=6dB)');
xlabel('SNR [dB]');
ylabel('BER');