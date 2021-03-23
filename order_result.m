clear,close all

load("ber_3.mat")
% hold on
plain_esn0 = plain_ebn0+10*log10(2);
semilogy(plain_esn0,plain_ber,'-*')
% semilogy(plain_ebn0,plain_ber,'-*',geom_ebn0,geom_ber,'-o',pcs_ebn0,pcs_ber,'-h')
grid on
hold on
% legend("普通QAM","几何整形","概率几何整形")
% xlabel("EbN0")
% ylabel("BER")


% figure;semilogy(plain_ebn0,plain_fer,'-*',geom_ebn0,geom_fer,'-o',pcs_ebn0,pcs_fer,'-h')
% grid on
% legend("普通QAM","几何整形","概率几何整形")
% xlabel("EbN0")
% ylabel("FER")