
import matplotlib.pylab as plt
from scipy.io import loadmat
from scipy.io import savemat
pcs_ebn0_ber={
    3.1451629926328435:1.1363636363636363e-07,
    3.7171037542994116:9.46969696969697e-08,
    2.0657182973302923:0.0009645106225923278,
    2.9085237302169173:1.5909090909090908e-06,
}

plain_ebn0_ber={
    4.9:1.1799242424242424e-05,
    5.5:2.840909090909091e-07,
    3.0:0.08551515151515152,
    1.0:0.19249810606060605,
    2.07:0.15252083333333333,
    4.0:0.004899538866930171,
    3.974:0.0055049589274430615,
    4.6:0.00012779222762898337,
    5.2566:1.2121212121212122e-06,
    5.7688:0.0
}

geometric_ebn0_ber={
    1.0:0.17602083333333332,
    2.0:0.15978030303030302,
    3.0:0.06821780303030303,
    4.0:0.0020867815035043626,
    5.0:5.0852272727272725e-06
    # 8.0:0.0
}

pcs_ebn0_fer = {
    3.1451629926328435:1.5e-05,
    3.7171037542994116:1e-05,
    2.0657182973302923:0.02537427048972342,
    2.9085237302169173:0.0004
}

plain_ebn0_fer = {
    4.9:0.00038,
    5.5:1.5e-05,
    3.0:0.852,
    1.0:1.0,
    2.07:0.998,
    4.0:0.08695652173913043,
    3.974:0.09066183136899365,
    4.6:0.002863934473179254,
    5.2566:6e-05,
    5.7688:0.0
}


geometric_ebn0_fer={
    1.0:1.0,
    2.0:1.0,
    3.0:0.76,
    4.0:0.06743088334457181,
    5.0:0.00019
}

print(pcs_ebn0_ber)
pcs_keys = sorted(pcs_ebn0_ber)
plain_keys = sorted(plain_ebn0_ber)
geom_keys = sorted(geometric_ebn0_ber)

pcs_ber_val = [pcs_ebn0_ber[k] for k in pcs_keys]
plain_ber_val = [plain_ebn0_ber[k] for k in plain_keys]
geom_ber_val = [geometric_ebn0_ber[k] for k in geom_keys]

pcs_fer_val = [pcs_ebn0_fer[k] for k in pcs_keys]
plain_fer_val = [plain_ebn0_fer[k] for k in plain_keys]
geom_fer_val = [geometric_ebn0_fer[k] for k in geom_keys]


savemat("ber_3.mat",
        {"pcs_ebn0":pcs_keys,
         "pcs_ber":pcs_ber_val,
         "plain_ebn0":plain_keys,
         "plain_ber":plain_ber_val,
         "geom_ebn0":geom_keys,
         "geom_ber":geom_ber_val,
         "pcs_fer":pcs_fer_val,
         "plain_fer":plain_fer_val,
         "geom_fer":geom_fer_val
         })

# plt.semilogy(pcs_keys,pcs_ber_val,"-*")  
# plt.semilogy(plain_keys,plain_ber_val,"-o")
# plt.semilogy(geom_keys,geom_ber_val,"-s")

# plt.show()