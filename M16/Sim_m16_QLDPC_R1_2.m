clc;
clear;

%%
% R = 1/2，GF16的多元域LDPC编码，译码算法采用Trellis Min Max算法，最大译码迭代次数为25，测试时SNR设置为EbN0，所以需要换算一下
deta = 10 * log10(4) + 10 * log10(0.5);
NR_16QAM_QLDPC_EbN0 = 3:0.5:5.5;
NR_16QAM_QLDPC_BER = [1.323850e-01, 8.343050e-02, 3.469122e-02, 7.516720e-03, 5.262045e-04, 1.552567e-05];

Symbol_AE_EbN0_1dB_EbN0 = 3:0.5:5;
Symbol_AE_EbN0_1dB_BER = [1.236590e-01, 5.361187e-02, 1.171606e-02, 1.573864e-03, 5.759467e-05];

Symbol_AE_EbN0_4dB_EbN0 = 3:0.5:5;
Symbol_AE_EbN0_4dB_BER = [1.373795e-01, 6.825939e-02, 1.616511e-02, 2.040970e-03, 8.711136e-05];

Symbol_AE_EbN0_8dB_EbN0 = 3:0.5:5;
Symbol_AE_EbN0_8dB_BER = [1.861202e-01, 9.386736e-02, 2.648653e-02, 3.275308e-03, 1.885676e-04];

%% 
semilogy(NR_16QAM_QLDPC_EbN0 + deta, NR_16QAM_QLDPC_BER, 'o-k', 'Linewidth', 1.3);
hold on;

semilogy(Symbol_AE_EbN0_1dB_EbN0 + deta, Symbol_AE_EbN0_1dB_BER, '<-', 'Linewidth', 1.3, 'Color', [1, 0.38, 0]);
hold on;

semilogy(Symbol_AE_EbN0_4dB_EbN0 + deta, Symbol_AE_EbN0_4dB_BER, 's-b', 'Linewidth', 1.3);
hold on;

semilogy(Symbol_AE_EbN0_8dB_EbN0 + deta, Symbol_AE_EbN0_8dB_BER, 'h-', 'Linewidth', 1.3, 'Color', [1, 0, 1]);
hold on;

%% 
set(gca, 'xlim', [6, 5 + deta], 'xtick', [6:0.1:5 + deta]);
set(gca, 'ylim', [10^-5, 10^-0]);
grid on;
h1 = legend('16QAM', 'Symbol-AE (16, EbN0 = 1dB)', 'Symbol-AE (16, EbN0 = 4dB)', 'Symbol-AE (16, EbN0 = 8dB)');
xlabel('SNR [dB]');
ylabel('BER');