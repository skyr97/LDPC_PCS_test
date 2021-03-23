clc;
clear;

%%
% 针对调制阶数为256
% R = 1/2，信息比特长度为2112，扩展因子Z = 96，译码算法采用NMS算法，迭代40次，校正因子设置为0.75，错误帧数为200帧

NR_256QAM_K2112_R1_2_SNR = 14.6:0.2:15.6;
NR_256QAM_K2112_R1_2_BER = [1.003e-01, 6.110e-02, 2.677e-02, 7.138e-03, 1.823e-03, 2.291e-04];

APSK_5_3_SNR = 13.8:0.2:15;
APSK_5_3_BER = [1.159e-01, 8.030e-02, 4.503e-02, 1.976e-02, 7.094e-03, 2.082e-03, 3.942e-04];

ATSC_256NUC_R8_15_SNR = 13.4:0.2:14.6;
ATSC_256NUC_R8_15_BER = [1.207e-01, 8.608e-02, 5.021e-02, 2.287e-02, 7.772e-03, 1.954e-03, 3.518e-04];

Bit_AE_EbN0_5dB_SNR = 13.4:0.2:14.6;
Bit_AE_EbN0_5dB_BER = [1.078e-01, 7.127e-02, 3.982e-02, 1.774e-02, 4.969e-03, 1.020e-03, 1.865e-04];

%% 画图
semilogy(NR_256QAM_K2112_R1_2_SNR, NR_256QAM_K2112_R1_2_BER, 'o-k', 'Linewidth', 1.2);
hold on;

semilogy(APSK_5_3_SNR, APSK_5_3_BER, '<-', 'Linewidth', 1.2, 'Color', [1, 0.38, 0]);
hold on;

semilogy(ATSC_256NUC_R8_15_SNR, ATSC_256NUC_R8_15_BER, 's-b', 'Linewidth', 1.2);
hold on;

semilogy(Bit_AE_EbN0_5dB_SNR, Bit_AE_EbN0_5dB_BER, 'h-', 'Linewidth', 1.2, 'Color', [1, 0, 1]);
hold on;

%% 设置坐标
set(gca, 'xlim', [13.4, 15.6], 'xtick', [13.4:0.2:15.6]);
set(gca, 'ylim', [10^-4, 10^-0]);
grid on;
h1 = legend('256QAM', '256APSK(5,3)', '256NUC-ATSC3.0(R=8/15)', 'Bit-AE(256,EbN0=5dB)');
xlabel('SNR [dB]');
ylabel('BER');
