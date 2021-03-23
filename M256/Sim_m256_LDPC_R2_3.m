clc;
clear;

%%
% R = 2/3，信息比特长度为2112，扩展因子Z = 96，译码算法采用NMS算法，迭代40次，校正因子设置为0.75，错误帧数为200帧

NR_256QAM_K2112_R2_3_SNR = 18:0.2:19.2;
NR_256QAM_K2112_R2_3_BER = [1.040e-01, 8.487e-02, 5.992e-02, 3.229e-02, 1.295e-02, 2.925e-03, 5.484e-04];

APSK_5_3_SNR = 17.2:0.2:18.8;
APSK_5_3_BER = [1.047e-01, 8.641e-02, 6.458e-02, 4.144e-02, 2.156e-02, 8.041e-03, 2.870e-03, 7.957e-04, 1.698e-04];

ATSC_256NUC_R10_15_SNR = 17:0.2:18.6;
ATSC_256NUC_R10_15_BER = [1.114e-01, 9.698e-02, 7.687e-02, 5.223e-02, 2.883e-02, 1.089e-02, 3.889e-03, 8.915e-04, 1.452e-04];

Bit_AE_EbN0_9dB_SNR = 17:0.2:18.6;
Bit_AE_EbN0_9dB_BER = [1.119e-01, 9.901e-02, 8.153e-02, 5.932e-02, 3.637e-02, 1.706e-02, 5.701e-03, 1.420e-03, 2.386e-04];

%% 画图
semilogy(NR_256QAM_K2112_R2_3_SNR, NR_256QAM_K2112_R2_3_BER, 'o-k', 'Linewidth', 1.2);
hold on;

semilogy(APSK_5_3_SNR, APSK_5_3_BER, '<-', 'Linewidth', 1.2, 'Color', [1, 0.38, 0]);
hold on;

semilogy(ATSC_256NUC_R10_15_SNR, ATSC_256NUC_R10_15_BER, 's-b', 'Linewidth', 1.2);
hold on;

semilogy(Bit_AE_EbN0_9dB_SNR, Bit_AE_EbN0_9dB_BER, 'h-', 'Linewidth', 1.2, 'Color', [1, 0, 1]);
hold on;

%% 设置坐标
set(gca, 'xlim', [17.4, 19.2], 'xtick', [17.4:0.2:19.2]);
set(gca, 'ylim', [10^-4, 10^-0]);
grid on;
h1 = legend('256QAM', '256APSK(5,3)', '256NUC-ATSC3.0(R=10/15)', 'Bit-AE(256,EbN0=9dB)');
xlabel('SNR [dB]');
ylabel('BER');
