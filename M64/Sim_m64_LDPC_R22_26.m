clc;
clear;

%% 
% 译码算法采用NMS算法，迭代40次，校正因子设置为0.75，错误帧数为200帧
% R = 22/26，信息比特长度为2112，扩展因子Z = 96，码长为2688
% 针对调制阶数为64，此时Bit-AE网络的星座取9dB

NR_64QAM_SNR = 15.8:0.2:17.6;
NR_64QAM_BER = [8.734e-02, 8.248e-02, 7.677e-02, 6.841e-02, 5.715e-02, 4.202e-02, 2.413e-02, 9.385e-03, 2.173e-03, 4.605e-04];

APSK_42_SNR = 15.8:0.2:17.6;
APSK_42_BER = [8.612e-02, 8.152e-02, 7.597e-02, 6.853e-02, 5.891e-02, 4.722e-02, 3.247e-02, 1.807e-02, 8.025e-03, 3.281e-03];

ATSC_64NUC_R13_15_SNR = 15.8:0.2:17.4;
ATSC_64NUC_R13_15_BER = [7.868e-02, 7.122e-02, 6.050e-02, 4.572e-02, 2.918e-02, 1.418e-02, 4.897e-03, 1.008e-03, 1.432e-04];

Bit_AE_M64_EbN0_9dB_SNR = 15.8:0.2:17.6;
Bit_AE_M64_EbN0_9dB_BER = [8.156e-02, 7.530e-02, 6.699e-02, 5.450e-02, 3.853e-02, 2.293e-02, 9.912e-03, 3.194e-03, 8.172e-04, 1.226e-04];

%% 画图
semilogy(NR_64QAM_SNR, NR_64QAM_BER, 'o-k', 'Linewidth', 1.2);
hold on;

semilogy(APSK_42_SNR, APSK_42_BER, '<-', 'Linewidth', 1.2, 'Color', [1, 0.38, 0]);
hold on;

semilogy(ATSC_64NUC_R13_15_SNR, ATSC_64NUC_R13_15_BER, 's-b', 'Linewidth', 1.2);
hold on;

semilogy(Bit_AE_M64_EbN0_9dB_SNR, Bit_AE_M64_EbN0_9dB_BER, 'v-', 'Linewidth', 1.2, 'Color', [0, 0.79, 0.34]);
hold on;

% semilogy(Bit_AE_M64_EbN0_8dB_SNR, Bit_AE_M64_EbN0_8dB_BER, 'h-', 'Linewidth', 1.2, 'Color', [1, 0, 1]);
% hold on;
%% 设置坐标
set(gca, 'xlim', [15.8, 17.6], 'xtick', [15.8:0.2:17.6]);
set(gca, 'ylim', [10^-4, 10^-0]);
grid on;
h1 = legend('64QAM', '64APSK(4,2)', '64NUC-ATSC3.0(R=13/15)', 'Bit-AE(64,EbN0=9dB)');
xlabel('SNR [dB]');
ylabel('BER');