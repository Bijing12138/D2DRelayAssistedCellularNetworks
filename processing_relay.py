import numpy as np
import itertools
import random
import operator
import pdb
import networkx as nx
import math
import time
#import matplotlib.pyplot as plt


from pow_level_sel_relay import opt_pow_opt_link_relay
from MS_Movement import MS_Markovian
from PL_models_relay import PL_ABG_relay
from arrival_cdf import arrival_cdf_func




def sys_processing_relay(X_relay,Y_relay,U_relay,X_T_relay,Y_T_relay,U_T_relay,PPP_cdf,num_users,num_PRB,pow_lev,MS_loc,BS_loc,P_avg):


	if all(i < 0 for i in X_relay) == True:
		pdb.set_trace();
	if all(i < 0 for i in Y_relay) == True:
		pdb.set_trace();	
	if all(i < 0 for i in U_relay) == True:
		pdb.set_trace();	


	# declaring the bipartite graph
	G_relay = nx.Graph();


	# nodes addition
	for MS_cnt in range(0,num_users):
		temp = 'MS' + str(MS_cnt);
		G_relay.add_node(temp);
	for PRB_cnt in range(0,num_PRB):
		temp = 'PRB' + str(PRB_cnt);
		G_relay.add_node(temp);



	X_to_be_added_relay = []; # this is exogeneous arrival
	Y_to_be_added_relay = []; # done later
	U_to_be_added_relay = []; # power addition



# breakpoint here
	for i in range(0,num_users):
		# adding exogeneous arrival
		p_temp = random.uniform(0,1);
		ind_temp = [ x for x,y in enumerate(PPP_cdf) if y>p_temp ][0]
		X_to_be_added_relay.append(ind_temp);
		Y_to_be_added_relay.append(0);
		U_to_be_added_relay.append(0);



	MS_PRB_dict_relay = {}; 
	# values of each key willl be of form: [opt_link_ID,pow_level,link_capacity] if not connected to BS or otherwise, [opt_link_ID,pow_level,link_capacity,queue_flag]
	# key of form 'MS_ID-PRB_ID'

	# for i-th index, optimal_outgoing_link_for_MS[i] gives the MS to which it is sending the data
	# if optimal_outgoing_link_for_MS[i] == i, then it means it is sending data to BS



	PL = PL_ABG_relay(MS_loc,num_users,BS_loc);
	# format for PL is : row id gives link id and column id gives user id  





	for i in range(0,num_PRB):
		# for each PRB assigned to a MS, one neeeds to know best link and optimal power level	
		


		for j in range(0,num_users):

			


#			pdb.set_trace();
			temp_array = PL[:,j];
			temp_mat = np.matlib.repmat(temp_array,len(pow_lev),1);
			PL_link_pow_lev = temp_mat.transpose();


			array_returned = opt_pow_opt_link_relay(pow_lev,X_T_relay[j],Y_T_relay,U_T_relay[j],PL_link_pow_lev,num_users,j);

#			pdb.set_trace();
			new_key = 'MS'+str(j)+'-'+'PRB'+str(i);
			new_value = [];
			new_value.append(array_returned[3]); # adding optimal link ID - to whih MS or BS it is connecting
			new_value.append(array_returned[0]); # adding optimal power
			new_value.append(array_returned[1]); # adding capacity in the optimal link due to optimal power
			if array_returned[3] == j: # link from MS to BS
				new_value.append(array_returned[4]);
			MS_PRB_dict_relay[new_key] = new_value;	




#			pdb.set_trace();
			# opt metric is weight in the bipartite graph
			# edge addition 
			# weight is a function of MS and PRB
			node1 = 'MS' + str(j);
			node2 = 'PRB' + str(i);
			weight_temp = array_returned[2];
			G_relay.add_edge(node1,node2,weight = weight_temp);

									



	# maximum bipartite weighted matching
	best_matching_relay = list(nx.max_weight_matching(G_relay,True));




	arrival_minus_dep_list = [];
	
	

	for i in range(0,len(best_matching_relay)):
		temp1 = best_matching_relay[i][0];
		if temp1[0] == 'P':
			node1 = best_matching_relay[i][0];
			node2 = best_matching_relay[i][1];
		else:
			node1 = best_matching_relay[i][1];
			node2 = best_matching_relay[i][0];
		key_to_search = node2 + '-' + node1;
		value_to_search = MS_PRB_dict_relay[key_to_search];
		Tx_MS = int(node2[2:]);
		Rx_MS_BS = value_to_search[0];		



		temp3 = X_relay[Tx_MS];

		if Rx_MS_BS != Tx_MS: # update of own queue at Tx MS and update of relay queue at Rx MS
			Y_to_be_added_relay[Rx_MS_BS] = Y_to_be_added_relay[Rx_MS_BS] + value_to_search[2];
			X_relay[Tx_MS] = max(X_relay[Tx_MS]-value_to_search[2],0);
		else:	# update of own or relay queue at Tx MS...BS is a black hole
			if value_to_search[3] == 0:
				X_relay[Tx_MS] = max(X_relay[Tx_MS] - value_to_search[2],0); 
			else:
				Y_relay[Tx_MS] = max(Y_relay[Tx_MS] - value_to_search[2],0);
		U_relay[Tx_MS] = max(U_relay[Tx_MS] - P_avg,0);
		U_to_be_added_relay[Tx_MS] = value_to_search[1];


		
	# addition of to be added queues
	X_relay = list(map(operator.add,X_relay,X_to_be_added_relay));
	Y_relay = list(map(operator.add,Y_relay,Y_to_be_added_relay));
	U_relay = list(map(operator.add,U_relay,U_to_be_added_relay));



#	X_list.append(np.sum(X)/num_users);
#	Y_list.append(np.sum(Y)/num_users);
#	U_list.append(np.sum(U_to_be_added)/num_users);

	for i in range(0,num_users):
		arrival_minus_dep_list.append(X_relay[i]+Y_relay[i]); # packets arriving from other MS



	# averaging of arrival minus dep in the whole system	
	avg_arrival_minus_dep_list = np.sum(arrival_minus_dep_list)/num_users;


	# delete vaiables
	del arrival_minus_dep_list;
	del G_relay;
	del best_matching_relay;
	del MS_PRB_dict_relay;
	del X_to_be_added_relay;
	del Y_to_be_added_relay;
	del U_to_be_added_relay;	



	return X_relay,Y_relay,U_relay,avg_arrival_minus_dep_list;


# avg_U = np.sum(U_list)/len(U_list);
# print avg_U;



'''
# plot
time_axis = list(range(1,N_inf));
plt.plot(time_axis, X_list, 'ro')
plt.axis([0, 1000, 0, 5000])
plt.show()

print X_list;
'''


