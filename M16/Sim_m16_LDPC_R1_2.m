clc;
clear;
% close all

%%
% R = 1/2，信息比特长度为2112，扩展因子Z = 96，译码算法采用NMS算法，迭代40次，校正因子设置为0.75，错误帧数为200帧
NR_16QAM_SNR = 6:0.1:7.0;
NR_16QAM_BER = [1.432e-01, 1.256e-01, 1.021e-01, 7.595e-02, 4.966e-02, 2.890e-02, 1.320e-02, 5.353e-03, 1.739e-03, 5.138e-04, 1.508e-04];

APSK_31_SNR = 6:0.1:6.9;
APSK_31_BER = [1.158e-01, 9.271e-02, 6.571e-02, 4.120e-02, 2.243e-02, 1.121e-02, 4.821e-03, 1.842e-03, 7.170e-04, 1.838e-04];

ATSC_16NUC_R8_15_SNR = 6.0:0.1:6.9;
ATSC_16NUC_R8_15_BER = [1.062e-01, 8.257e-02, 5.661e-02, 3.515e-02, 1.840e-02, 8.535e-03, 3.498e-03, 1.232e-03, 3.857e-04, 1.066e-04];

Bit_AE_EbN0_1dB_SNR = 6.0:0.1:6.9;
Bit_AE_EbN0_1dB_BER = [1.032e-01, 7.671e-02, 5.206e-02, 3.113e-02, 1.483e-02, 7.022e-03, 2.888e-03, 9.927e-04, 3.320e-04, 8.061e-05];

%% 画图
semilogy(NR_16QAM_SNR, NR_16QAM_BER, 'o-k', 'Linewidth', 1.2);
hold on;

semilogy(APSK_31_SNR, APSK_31_BER, '<-', 'Linewidth', 1.2, 'Color', [1, 0.38, 0]);
hold on;

% semilogy(APSK_22_SNR, APSK_22_BER, '^-', 'Linewidth', 1.2, 'Color', [0, 0.79, 0.34]);
% hold on;

semilogy(ATSC_16NUC_R8_15_SNR, ATSC_16NUC_R8_15_BER, 's-b', 'Linewidth', 1.2);
hold on;

semilogy(Bit_AE_EbN0_1dB_SNR, Bit_AE_EbN0_1dB_BER, 'h-', 'Linewidth', 1.2, 'Color', [1, 0, 1]);
hold on;

%% 设置坐标
set(gca, 'xlim', [6, 6.9], 'xtick', [6:0.1:6.9]);
set(gca, 'ylim', [10^-4, 10^-0]);
grid on;
% h1 = legend('16QAM', '16APSK(3,1)', '16APSK(2,2)', '16NUC-ATSC3.0(R=8/15)', 'Bit-AE(16,EbN0=3dB)');
h1 = legend('16QAM', '16APSK(3,1)', '16NUC-ATSC3.0(R=8/15)', 'Bit-AE(16,EbN0=1dB)');
xlabel('SNR [dB]');
ylabel('BER');

%% 生成子图
% axes('Position',[0.18,0.62,0.28,0.25]);
% SNR_subfig = 6:0.1:6.9;
% 
% NR_16QAM_subfig = [1.432e-01, 1.256e-01, 1.021e-01, 7.595e-02, 4.966e-02, 2.890e-02, 1.320e-02, 5.353e-03, 1.739e-03, 5.138e-04, 1.508e-04];
% 
% APSK_subfig = [1.158e-01, 9.271e-02, 6.571e-02, 4.120e-02, 2.243e-02, 1.121e-02, 4.821e-03, 1.842e-03, 7.170e-04, 1.838e-04];
% 
% ATSC_subfig = [1.062e-01, 8.257e-02, 5.661e-02, 3.515e-02, 1.840e-02, 8.535e-03, 3.498e-03, 1.232e-03, 3.857e-04, 1.066e-04];
% 
% Bit_AE_subfig = [1.032e-01, 7.671e-02, 5.206e-02, 3.113e-02, 1.483e-02, 7.022e-03, 2.888e-03, 9.927e-04, 3.320e-04, 8.061e-05];
% 
% semilogy(NR_16QAM_SNR, NR_16QAM_BER, 'o-k', 'Linewidth', 1.2);
% hold on;
% 
% semilogy(APSK_31_SNR, APSK_31_BER, '<-', 'Linewidth', 1.2, 'Color', [1, 0.38, 0]);
% hold on;
% 
% semilogy(ATSC_16NUC_R8_15_SNR, ATSC_16NUC_R8_15_BER, 's-b', 'Linewidth', 1.2);
% hold on;
% 
% semilogy(Bit_AE_EbN0_1dB_SNR, Bit_AE_EbN0_1dB_BER, 'h-', 'Linewidth', 1.2, 'Color', [1, 0, 1]);
% hold on;
% 
% set(gca,'xlim',[6.48, 6.52], 'xtick', [6.48:0.02:6.52]);
% set(gca,'ylim',[0.006, 0.015], 'ytick', [0.006:0.009:0.015]);