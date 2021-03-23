clc;
clear;

%%
% R = 22/29(0.758), 信息比特长度为2112, 扩展因子Z = 96, 译码算法采用NMS算法, 迭代40次, 校正因子设置为0.75, 错误帧数为200帧

NR_256QAM_K2112_R22_29_SNR = 18.8:0.2:21.2;
NR_256QAM_K2112_R22_29_BER = [1.130e-01, 1.084e-01, 1.033e-01, 9.692e-02, 9.053e-02, 8.166e-02, 6.955e-02, 5.341e-02, 3.356e-02, 1.565e-02, 5.095e-03, 1.176e-03, 1.532e-04];

APSK_5_3_SNR = 18.8:0.2:21;
APSK_5_3_BER = [9.848e-02, 9.198e-02, 8.336e-02, 7.185e-02, 5.814e-02, 4.105e-02, 2.443e-02, 1.172e-02, 4.160e-03, 1.539e-03, 3.912e-04, 1.008e-04];

ATSC_256NUC_R11_15_SNR = 18.8:0.2:20.6;
ATSC_256NUC_R11_15_BER = [9.381e-02, 8.584e-02, 7.562e-02, 6.088e-02, 4.249e-02, 2.460e-02, 1.178e-02, 4.180e-03, 1.072e-03, 2.155e-04];

Bit_AE_EbN0_11dB_SNR = 18.8:0.2:20.8;
Bit_AE_EbN0_11dB_BER = [9.861e-02, 9.110e-02, 8.149e-02, 6.947e-02, 5.361e-02, 3.634e-02, 1.922e-02, 7.620e-03, 2.392e-03, 5.527e-04, 1.136e-04];

%% 画图
semilogy(NR_256QAM_K2112_R22_29_SNR, NR_256QAM_K2112_R22_29_BER, 'o-k', 'Linewidth', 1.2);
hold on;

semilogy(APSK_5_3_SNR, APSK_5_3_BER, '<-', 'Linewidth', 1.2, 'Color', [1, 0.38, 0]);
hold on;

semilogy(ATSC_256NUC_R11_15_SNR, ATSC_256NUC_R11_15_BER, 's-b', 'Linewidth', 1.2);
hold on;

semilogy(Bit_AE_EbN0_11dB_SNR, Bit_AE_EbN0_11dB_BER, 'h-', 'Linewidth', 1.2, 'Color', [1, 0, 1]);
hold on;

%% 设置坐标
set(gca, 'xlim', [19.2, 21.2], 'xtick', [19.2:0.2:21.2]);
set(gca, 'ylim', [10^-4, 10^-0]);
grid on;
h1 = legend('256QAM', '256APSK(5,3)', '256NUC-ATSC3.0(R=11/15)', 'Bit-AE(256,EbN0=11dB)');
xlabel('SNR [dB]');
ylabel('BER');
