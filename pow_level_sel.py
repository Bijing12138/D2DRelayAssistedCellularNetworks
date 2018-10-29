import numpy as np 
import math
import pdb


P_Noise = 10**(-9); #in mWatt
per_packet_size = 65507 # in bits
V = 1;



def opt_pow_sel_MS_BS_link_no_relay(pow_lev,X_i,U_i,PL):
#	pdb.set_trace();
	Metric = [];
	for lev in range(0,len(pow_lev)):
		pow_lev_Watt = pow_lev[lev];
		pow_lev_dBm   = 10*math.log10(pow_lev_Watt*1000);
		P_Rx_dBm = pow_lev_dBm - PL;
		P_Rx_mWatt = 10**(P_Rx_dBm/10);
		mu_bits  = 180*(10**3)*math.log(1 + (P_Rx_mWatt/P_Noise),2); # in bits
		mu = mu_bits//per_packet_size; # num of packets 
		temp = X_i*mu - V*U_i*pow_lev_dBm;
		Metric.append(temp);


	opt_ind = np.argmax(Metric);
	opt_pow_Watt = pow_lev[opt_ind];
	opt_pow = 10*math.log10(opt_pow_Watt*1000);


	opt_P_Rx_dBm = opt_pow - PL;
	opt_P_Rx = 10**(opt_P_Rx_dBm/10);
	opt_link_capacity = (180*(10**3)*math.log(1+(opt_P_Rx/P_Noise),2))//per_packet_size;


	return opt_pow,opt_link_capacity,Metric[opt_ind];