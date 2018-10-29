import numpy as np
import itertools
import random
import operator
import pdb
import networkx as nx
import math
import time
#import matplotlib.pyplot as plt



from pow_level_sel_no_relay import opt_pow_sel_MS_BS_link_no_relay
from MS_Movement import MS_Markovian
from PL_models import PL_ABG
from arrival_cdf import arrival_cdf_func



def sys_processing_no_relay(X_no_relay,U_no_relay,X_T_no_relay,U_T_no_relay,PPP_cdf,num_users,num_PRB,pow_lev,MS_loc,BS_loc,P_avg):


	# declaring the bipartite graph
	G_no_relay = nx.Graph();


	# nodes addition
	for MS_cnt in range(0,num_users):
		temp = 'MS' + str(MS_cnt);
		G_no_relay.add_node(temp);
	for PRB_cnt in range(0,num_PRB):
		temp = 'PRB' + str(PRB_cnt);
		G_no_relay.add_node(temp);
	
	X_to_be_added_no_relay = []; # this is exogeneous arrival
	U_to_be_added_no_relay = []; # power addition


	for i in range(0,num_users):
		# adding exogeneous arrival
		p_temp = random.uniform(0,1);
		ind_temp = [ x for x,y in enumerate(PPP_cdf) if y>p_temp ][0]
		X_to_be_added_no_relay.append(ind_temp);
		U_to_be_added_no_relay.append(0);


	MS_PRB_dict_no_relay = {}; 
	# values of each key willl be of form: [opt_link_ID,pow_level,link_capacity] if not connected to BS or otherwise, [opt_link_ID,pow_level,link_capacity,queue_flag]
	# key of form 'MS_ID-PRB_ID'

	# for i-th index, optimal_outgoing_link_for_MS[i] gives the MS to which it is sending the data
	# if optimal_outgoing_link_for_MS[i] == i, then it means it is sending data to BS




	for i in range(0,num_PRB):
		# for each PRB assigned to a MS, one neeeds to know best link and optimal power level	
		


		for j in range(0,num_users):
			loc1 = MS_loc[j];
			


#			print('Tx is {}'.format(j));		


			# this is for MS and BS link
#			pdb.set_trace();
#			print('Rx is the BS');
			loc2 = BS_loc;
			PL = PL_ABG(loc1,loc2);
			opt_pow,opt_link_capacity,opt_metric = opt_pow_sel_MS_BS_link_no_relay(pow_lev,X_T_no_relay[j],U_T_no_relay[j],PL); # opt_pow is the appropriate power for that PRB in that link



			new_key = 'MS'+str(j)+'-'+'PRB'+str(i);
			new_value = [];
			new_value.append(opt_pow); # adding optimal power
			new_value.append(opt_link_capacity); # adding capacity in the optimal link due to optimal power
			MS_PRB_dict_no_relay[new_key] = new_value;	



#			pdb.set_trace();
			# opt metric is weight in the bipartite graph
			# edge addition 
			# weight is a function of MS and PRB
			node1 = 'MS' + str(j);
			node2 = 'PRB' + str(i);
			weight_temp = opt_metric;
			G_no_relay.add_edge(node1,node2,weight = weight_temp);

									



	# maximum bipartite weighted matching
	best_matching_no_relay = list(nx.max_weight_matching(G_no_relay,True));





	for i in range(0,len(best_matching_no_relay)):
		temp1 = best_matching_no_relay[i][0];
		if temp1[0] == 'P':
			node1 = best_matching_no_relay[i][0];
			node2 = best_matching_no_relay[i][1];
		else:
			node1 = best_matching_no_relay[i][1];
			node2 = best_matching_no_relay[i][0];
		key_to_search = node2 + '-' + node1;
		value_to_search = MS_PRB_dict_no_relay[key_to_search];
		Tx_MS = int(node2[2:]);
		


		X_no_relay[Tx_MS] = max(X_no_relay[Tx_MS] - value_to_search[1],0); 

		U_no_relay[Tx_MS] = max(U_no_relay[Tx_MS] - P_avg,0);
		U_to_be_added_no_relay[Tx_MS] = value_to_search[0];


		
	# addition of to be added queues
	X_no_relay = list(map(operator.add,X_no_relay,X_to_be_added_no_relay));
	U_no_relay = list(map(operator.add,U_no_relay,U_to_be_added_no_relay));


	arrival_minus_dep_list = [];
	for i in range(0,num_users):
		arrival_minus_dep_list.append(X_no_relay[i]);
	#X_no_relay is the number of pkts generated tilll t - number of pkts delivered till t	



#	X_list.append(np.sum(X)/num_users);
#	Y_list.append(np.sum(Y)/num_users);
#	U_list.append(np.sum(U_to_be_added)/num_users);

				

	# delete vaiables
	del G_no_relay;
	del best_matching_no_relay;
	del MS_PRB_dict_no_relay;
	del X_to_be_added_no_relay;
	del U_to_be_added_no_relay;	


	avg_arrival_minus_dep_list = np.sum(arrival_minus_dep_list)/num_users;


	return X_no_relay,U_no_relay,avg_arrival_minus_dep_list;
