clc;
clear;

%% 
% 译码算法采用NMS算法，迭代40次，校正因子设置为0.75，错误帧数为200帧
% R = 2/3，信息比特长度为2112，扩展因子Z = 96，码长为3360
NR_16QAM_SNR = 8.2:0.1:9.4;
NR_16QAM_BER = [1.115e-01, 1.040e-01, 9.487e-02, 8.435e-02, 7.020e-02, 5.427e-02, 3.864e-02, 2.380e-02, 1.227e-02, 5.316e-03, 2.301e-03, 6.584e-04, 2.022e-04];

APSK_31_SNR = 8:0.1:9.4;
APSK_31_BER = [1.172e-01, 1.107e-01, 1.026e-01, 9.207e-02, 7.866e-02, 6.368e-02, 4.762e-02, 3.268e-02, 2.073e-02, 1.219e-02, 5.188e-03, 2.000e-03, 6.632e-04, 2.197e-04, 6.622e-05];

ATSC_16NUC_R10_15_SNR = 8:0.1:9.4;
ATSC_16NUC_R10_15_BER = [1.163e-01, 1.097e-01, 1.015e-01, 9.092e-02, 7.868e-02, 6.445e-02, 4.746e-02, 3.209e-02, 1.863e-02, 1.039e-02, 5.190e-03, 2.026e-03, 6.801e-04, 2.284e-04, 5.421e-05];

Bit_AE_EbN0_3dB_SNR = 8:0.1:9.4;
Bit_AE_EbN0_3dB_BER = [1.159e-01, 1.089e-01, 1.005e-01, 8.960e-02, 7.685e-02, 6.249e-02, 4.696e-02, 3.041e-02, 1.800e-02, 1.036e-02, 5.161e-03, 2.193e-03, 6.479e-04, 2.168e-04, 4.576e-05];

Bit_AE_EbN0_5dB_SNR = 8:0.1:9.4;
Bit_AE_EbN0_5dB_BER = [1.210e-01, 1.158e-01, 1.086e-01, 1.005e-01, 8.957e-02, 7.674e-02, 6.112e-02, 4.323e-02, 2.716e-02, 1.507e-02, 7.864e-03, 3.588e-03, 1.216e-03, 3.453e-04, 9.405e-05];

Bit_AE_EbN0_8dB_SNR = 8:0.1:9.4;
Bit_AE_EbN0_8dB_BER = [1.226e-01, 1.169e-01, 1.115e-01, 1.037e-01, 9.414e-02, 8.179e-02, 6.719e-02, 4.957e-02, 3.243e-02, 1.833e-02, 1.018e-02, 4.740e-03, 1.904e-03, 4.619e-04, 1.298e-04];


%% 画图
semilogy(NR_16QAM_SNR(3:end), NR_16QAM_BER(3:end), 'o-k', 'Linewidth', 1.2);
hold on;

semilogy(APSK_31_SNR, APSK_31_BER, '<-', 'Linewidth', 1.2, 'Color', [1, 0.38, 0]);
hold on;

semilogy(ATSC_16NUC_R10_15_SNR(4:end), ATSC_16NUC_R10_15_BER(4:end), 's-b', 'Linewidth', 1.2);
hold on;

semilogy(Bit_AE_EbN0_3dB_SNR(3:end), Bit_AE_EbN0_3dB_BER(3:end), 'h-', 'Linewidth', 1.2, 'Color', [1, 0, 1]);
hold on;

semilogy(Bit_AE_EbN0_5dB_SNR(3:end), Bit_AE_EbN0_5dB_BER(3:end), '*-', 'Linewidth', 1.2, 'Color', [0, 0.79, 0.34]);
hold on;

semilogy(Bit_AE_EbN0_8dB_SNR(3:end), Bit_AE_EbN0_8dB_BER(3:end), '^-r', 'Linewidth', 1.2);
hold on;

%% 设置坐标
set(gca, 'xlim', [8.4, 9.4], 'xtick', [8.4:0.1:9.4]);
set(gca, 'ylim', [10^-4.5, 10^-0]);
grid on;
h1 = legend('16QAM', '16APSK(3,1)', '16NUC-ATSC3.0(R=10/15)', 'Bit-AE(16,EbN0=3dB)', 'Bit-AE(16,EbN0=5dB)', 'Bit-AE(16,EbN0=8dB)');
xlabel('SNR [dB]');
ylabel('BER');

%% 生成子图
% axes('Position',[0.18,0.62,0.28,0.25]);
% SNR_subfig = 8:0.1:9.3;
% 
% NR_16QAM_subfig = [1.115e-01, 1.040e-01, 9.487e-02, 8.435e-02, 7.020e-02, 5.427e-02, 3.864e-02, 2.380e-02, 1.227e-02, 5.316e-03, 2.301e-03, 6.584e-04, 2.022e-04];
% 
% APSK_subfig = [1.172e-01, 1.107e-01, 1.026e-01, 9.207e-02, 7.866e-02, 6.368e-02, 4.762e-02, 3.268e-02, 2.073e-02, 1.219e-02, 5.188e-03, 2.000e-03, 6.632e-04, 2.197e-04];
% 
% ATSC_subfig = [1.163e-01, 1.097e-01, 1.015e-01, 9.092e-02, 7.868e-02, 6.445e-02, 4.746e-02, 3.209e-02, 1.863e-02, 1.039e-02, 5.190e-03, 2.026e-03, 6.801e-04, 2.284e-04];
% 
% Bit_AE_subfig = [1.159e-01, 1.089e-01, 1.005e-01, 8.960e-02, 7.685e-02, 6.249e-02, 4.696e-02, 3.041e-02, 1.800e-02, 1.036e-02, 5.161e-03, 2.193e-03, 6.479e-04, 2.168e-04];
% 
% semilogy(NR_16QAM_SNR, NR_16QAM_BER, 'o-k', 'Linewidth', 1.2);
% hold on;
% 
% semilogy(APSK_31_SNR, APSK_31_BER, '<-', 'Linewidth', 1.2, 'Color', [1, 0.38, 0]);
% hold on;
% 
% semilogy(ATSC_16NUC_R10_15_SNR, ATSC_16NUC_R10_15_BER, 's-b', 'Linewidth', 1.2);
% hold on;
% 
% semilogy(Bit_AE_EbN0_3dB_SNR, Bit_AE_EbN0_3dB_BER, 'h-', 'Linewidth', 1.2, 'Color', [1, 0, 1]);
% hold on;
% 
% set(gca,'xlim',[8.8, 9], 'xtick', [8.8:0.1:9]);
% set(gca,'ylim',[0.005, 0.025], 'ytick', [0.005:0.02:0.025]);