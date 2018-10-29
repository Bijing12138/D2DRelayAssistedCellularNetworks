import numpy as np 
import math
import pdb


P_Noise = 10**(-9); #in mWatt
per_packet_size = 25000 # in bits



def opt_pow_opt_link_relay(pow_lev,X_i,Y,U_i,PL_link_pow_lev,num_users,Tx_MS_ID):

#	pdb.set_trace();
	pow_lev_Watt_mat = np.matlib.repmat(pow_lev,num_users,1); # format is: row id is link ID, column id is power level id
	pow_lev_dBm_mat = 10*np.log10(pow_lev_Watt_mat*1000);
	P_Rx_dBm_mat = pow_lev_dBm_mat - PL_link_pow_lev;
	# same link ID has same PL acrooss columns but different pow_level

	P_Rx_mWatt_mat = 10**(P_Rx_dBm_mat/10);
	SINR_mat = P_Rx_mWatt_mat/P_Noise;
	mu_bits_mat = 180*(10**3)*np.log2( 1 + SINR_mat); # in bits
	mu_mat = mu_bits_mat//per_packet_size;



	U_mat = np.ones((num_users,len(pow_lev)))*U_i; 
	pow_part_of_metric = np.multiply(U_mat,pow_lev_dBm_mat);



	X_i_mat = X_i*np.ones((num_users,len(pow_lev)));
	temp_mat2 = np.matlib.repmat(Y,len(pow_lev),1);
	Y_mat = temp_mat2.transpose();
	
	Queue_diff = X_i_mat - Y_mat; # added MS-MS link


	Queue_diff[Tx_MS_ID,:]*=0; # making space for MS- to BS link
	temp_array3 = max(X_i,Y[Tx_MS_ID])*np.ones((1,len(pow_lev)));
	temp_mat3 = np.zeros((num_users,len(pow_lev)));
	temp_mat3[Tx_MS_ID,:] = temp_array3;

	Queue_diff = Queue_diff + temp_mat3; # all queue diffs in MS-MS and max of queues in MS-BS taken

	queue_part_of_metric = np.multiply(Queue_diff,mu_mat);


	metric = queue_part_of_metric - pow_part_of_metric;


	row = np.argmax(metric,axis=0);
	col = np.argmax(metric,axis=1);

	opt_Rx_ID = row[0];
	opt_pow_ID = col[Tx_MS_ID];
	opt_pow_Watt = pow_lev[opt_pow_ID];
	opt_pow = 10*math.log10(opt_pow_Watt*1000); # in dBm


	opt_link_capacity = mu_mat[opt_Rx_ID][opt_pow_ID];
	opt_metric = metric[opt_Rx_ID][opt_pow_ID];

	array_to_be_returned = [];

	if Tx_MS_ID != opt_Rx_ID:
		array_to_be_returned.append(opt_pow);
		array_to_be_returned.append(opt_link_capacity);
		array_to_be_returned.append(opt_metric);
		array_to_be_returned.append(opt_Rx_ID);
		return opt_pow,opt_link_capacity,opt_metric,opt_Rx_ID;
	else:
		if X_i >= Y[Tx_MS_ID]:
			queue_flag = 0;
		else:
			queue_flag = 1;

		array_to_be_returned.append(opt_pow);
		array_to_be_returned.append(opt_link_capacity);
		array_to_be_returned.append(opt_metric);
		array_to_be_returned.append(opt_Rx_ID);
		array_to_be_returned.append(queue_flag);
		return opt_pow,opt_link_capacity,opt_metric,opt_Rx_ID,queue_flag;	










'''


def opt_pow_sel_MS_MS_link_relay(pow_lev,X_i,Y_j,U_i,PL):
#	pdb.set_trace();
	Metric = [];
	for lev in range(0,len(pow_lev)):
		pow_lev_Watt = pow_lev[lev];
		pow_lev_dBm   = 10*math.log10(pow_lev_Watt*1000);
		P_Rx_dBm = pow_lev_dBm - PL;
		P_Rx_mWatt = 10**(P_Rx_dBm/10);
		mu_bits  = 180*(10**3)*math.log(1 + (P_Rx_mWatt/P_Noise),2); # in bits
		mu = mu_bits//per_packet_size; # num of packets 
		temp = (X_i - Y_j)*mu - U_i*pow_lev_dBm;
		Metric.append(temp);

	opt_ind = np.argmax(Metric);
	opt_pow_Watt = pow_lev[opt_ind];
	opt_pow = 10*math.log10(opt_pow_Watt*1000); # in dBm

	opt_P_Rx_dBm = opt_pow - PL;
	opt_P_Rx = 10**(opt_P_Rx_dBm/10);
	opt_link_capacity = (180*(10**3)*math.log(1+(opt_P_Rx/P_Noise),2))//per_packet_size;

	return opt_pow,opt_link_capacity,Metric[opt_ind];


def opt_pow_sel_MS_BS_link_relay(pow_lev,X_i,Y_i,U_i,PL):
#	pdb.set_trace();
	Metric = [];
	for lev in range(0,len(pow_lev)):
		pow_lev_Watt = pow_lev[lev];
		pow_lev_dBm   = 10*math.log10(pow_lev_Watt*1000);
		P_Rx_dBm = pow_lev_dBm - PL;
		P_Rx_mWatt = 10**(P_Rx_dBm/10);
		mu_bits  = 180*(10**3)*math.log(1 + (P_Rx_mWatt/P_Noise),2); # in bits
		mu = mu_bits//per_packet_size; # num of packets 
		temp = max(X_i,Y_i)*mu - U_i*pow_lev_dBm;
		Metric.append(temp);

	if X_i >= Y_i:
		queue_flag = 0;
	else:
		queue_flag = 1;

	opt_ind = np.argmax(Metric);
	opt_pow_Watt = pow_lev[opt_ind];
	opt_pow = 10*math.log10(opt_pow_Watt*1000);


	opt_P_Rx_dBm = opt_pow - PL;
	opt_P_Rx = 10**(opt_P_Rx_dBm/10);
	opt_link_capacity = (180*(10**3)*math.log(1+(opt_P_Rx/P_Noise),2))//per_packet_size;


	return opt_pow,opt_link_capacity,Metric[opt_ind],queue_flag;


'''