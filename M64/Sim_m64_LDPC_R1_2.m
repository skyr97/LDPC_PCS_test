clc;
clear;

%%
% R = 1/2����Ϣ���س���Ϊ2112����չ����Z = 96�������㷨����NMS�㷨������40�Σ�У����������Ϊ0.75������֡��Ϊ200֡
% ��Ե��ƽ���Ϊ64

NR_64QAM_SNR = 10.6:0.2:11.4;
NR_64QAM_BER = [1.059e-01, 6.126e-02, 2.349e-02, 5.277e-03, 7.727e-04];

APSK_42_SNR = 10:0.2:11;
APSK_42_BER = [1.220e-01, 8.077e-02, 3.898e-02, 1.339e-02, 3.423e-03, 4.817e-04];

ATSC_64NUC_R8_15_SNR = 10:0.2:11;
ATSC_64NUC_R8_15_BER = [1.044e-01, 6.016e-02, 2.408e-02, 6.959e-03, 1.189e-03, 1.555e-04];

Bit_AE_M64_EbN0_2dB_SNR = 10:0.2:11;
Bit_AE_M64_EbN0_2dB_BER = [9.951e-02, 5.721e-02, 2.473e-02, 6.324e-03, 1.234e-03, 1.527e-04];

%% ��ͼ
semilogy(NR_64QAM_SNR, NR_64QAM_BER, 'o-k', 'Linewidth', 1.2);
hold on;

semilogy(APSK_42_SNR, APSK_42_BER, '<-', 'Linewidth', 1.2, 'Color', [1, 0.38, 0]);
hold on;

semilogy(ATSC_64NUC_R8_15_SNR, ATSC_64NUC_R8_15_BER, 's-b', 'Linewidth', 1.2);
hold on;

semilogy(Bit_AE_M64_EbN0_2dB_SNR, Bit_AE_M64_EbN0_2dB_BER, 'h-', 'Linewidth', 1.2, 'Color', [1, 0, 1]);
hold on;

%% ��������
set(gca, 'xlim', [10, 11.4], 'xtick', [10:0.2:11.4])
set(gca, 'ylim', [10^-4, 10^-0]);
grid on;
h1 = legend('64QAM', '64APSK(4,2)', '64NUC-ATSC3.0(R=8/15)', 'Bit-AE(64,EbN0=2dB)');
xlabel('SNR [dB]');
ylabel('BER');

