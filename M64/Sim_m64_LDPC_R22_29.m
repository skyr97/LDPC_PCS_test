clc;
clear;

%% 
% 译码算法采用NMS算法，迭代40次，校正因子设置为0.75，错误帧数为200帧
% R = 22/29，信息比特长度为2112，扩展因子Z = 96，码长为2976
% 针对调制阶数为64，此时Bit-AE网络的星座取8, 9dB

NR_64QAM_SNR = 14:0.2:16;
NR_64QAM_BER = [1.109e-01, 1.058e-01, 9.944e-02, 9.189e-02, 8.283e-02, 6.954e-02, 5.127e-02, 2.814e-02, 1.017e-02, 2.795e-03, 3.209e-04];

APSK_42_SNR = 14:0.2:16;
APSK_42_BER = [1.022e-01, 9.575e-02, 8.726e-02, 7.658e-02, 6.120e-02, 4.252e-02, 2.373e-02, 1.047e-02, 3.082e-03, 6.706e-04, 1.126e-04];

ATSC_64NUC_R11_15_SNR = 14:0.2:15.6;
ATSC_64NUC_R11_15_BER = [9.833e-02, 9.104e-02, 8.112e-02, 6.701e-02, 4.879e-02, 2.812e-02, 1.101e-02, 2.903e-03, 5.555e-04];

Bit_AE_M64_EbN0_8dB_SNR = 14:0.2:15.6;
Bit_AE_M64_EbN0_8dB_BER = [9.949e-02, 9.205e-02, 8.268e-02, 6.879e-02, 4.993e-02, 2.811e-02, 1.136e-02, 3.021e-03, 4.815e-04];

Bit_AE_M64_EbN0_9dB_SNR = 14:0.2:15.8;
Bit_AE_M64_EbN0_9dB_BER = [1.026e-01, 9.552e-02, 8.675e-02, 7.537e-02, 5.837e-02, 3.706e-02, 1.854e-02, 5.834e-03, 1.343e-03, 1.874e-04];
%% 画图
semilogy(NR_64QAM_SNR, NR_64QAM_BER, 'o-k', 'Linewidth', 1.2);
hold on;

semilogy(APSK_42_SNR(1:10), APSK_42_BER(1:10), '<-', 'Linewidth', 1.2, 'Color', [1, 0.38, 0]);
hold on;

semilogy(ATSC_64NUC_R11_15_SNR, ATSC_64NUC_R11_15_BER, 's-b', 'Linewidth', 1.2);
hold on;

semilogy(Bit_AE_M64_EbN0_8dB_SNR, Bit_AE_M64_EbN0_8dB_BER, 'h-', 'Linewidth', 1.2, 'Color', [1, 0, 1]);
hold on;

semilogy(Bit_AE_M64_EbN0_9dB_SNR, Bit_AE_M64_EbN0_9dB_BER, '*-', 'Linewidth', 1.2, 'Color', [0, 0.79, 0.34]);
hold on;
%% 设置坐标
set(gca, 'xlim', [14.4, 16], 'xtick', [14.4:0.2:16]);
set(gca, 'ylim', [10^-4, 10^-0]);
grid on;
h1 = legend('64QAM', '64APSK(4,2)', '64NUC-ATSC3.0(R=11/15)', 'Bit-AE(64,EbN0=8dB)', 'Bit-AE(64,EbN0=9dB)');
xlabel('SNR [dB]');
ylabel('BER');