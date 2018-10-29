import numpy as np
import itertools
import random
import operator
import pdb
import networkx as nx
import math
import numpy.matlib



def PL_ABG_relay(MS_loc,num_users,BS_loc):

#	pdb.set_trace();

	loc_list_x = np.array([loc[0] for loc in MS_loc]); # x - coordinate
	loc_list_y = np.array([loc[1] for loc in MS_loc]); # y- coordinate


	# creating matrix for primary MS
	loc1_mat_x = np.matlib.repmat(loc_list_x,num_users,1); 
	loc1_mat_y = np.matlib.repmat(loc_list_y,num_users,1);

	# creating matrix for secondary MS/ BS 
	loc2_mat_x = loc1_mat_x.transpose();
	loc2_mat_y = loc1_mat_y.transpose();


	diff_x = loc1_mat_x - loc2_mat_x;
	diff_y = loc1_mat_y - loc2_mat_y;
	# diagonals are zero...reserved for distance from BS

	BS_loc_x = BS_loc[0]*np.ones(num_users);
	BS_loc_y = BS_loc[1]*np.ones(num_users);


	MS_BS_diff_x = loc_list_x - BS_loc_x;
	MS_BS_diff_y = loc_list_y - BS_loc_y;

	# add it to general distance matrix
	diff_x = diff_x + np.diag(MS_BS_diff_x);
	diff_y = diff_y + np.diag(MS_BS_diff_y);
	# distance from BS added

	sqr_x = diff_x**2;
	sqr_y = diff_y**2;


	squared_dist = sqr_x + sqr_y;

	dist = np.sqrt(squared_dist);

	# as a safety add ones so that no distances are zero
	dist = dist + np.ones((num_users,num_users));



	# channel parameters
	sigma = 3.3;
	alpha = 1.9;
	beta = 31.2;
	gamma = 2.2;
	f = 3.5;



	# shadowing 
	shadowing  = np.random.normal(0,sigma,size=(num_users,num_users));
	

	PL = 10*alpha*(np.log10(dist)) + beta*np.ones((num_users,num_users)) + 10*gamma*(np.log10(f))*np.ones((num_users,num_users)) + shadowing;

	return PL; 



'''
def PL_ABG(loc1,loc2):
	# channel qualities

	alpha_1 = 1.6;
	alpha_2 = 1.9;
	alpha_3 = 1.9;
	beta_1 = 32.9;
	beta_2 = 31.2;
	beta_3 = 35.8;
	gamma_1 = 1.8;
	gamma_2 = 2.2;
	gamma_3 = 1.9;
	sigma_1 = 4.5;
	sigma_2 = 3.3;
	sigma_3 = 2.4;
	f = 3.5;

	if loc1 == loc2:
		d  = 1; # 1 metre
	else:
		temp = (loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2;
		d = np.sqrt(temp);

	if 1 <= d <= 49:
		alpha = alpha_1;
		beta = beta_1;
		gamma = gamma_1;
		sigma = sigma_1;
	if 49 <= d <= 149:
		alpha = alpha_2;
		beta = beta_2;
		gamma = gamma_2;
		sigma = sigma_2;
	else:
		alpha = alpha_3;
		beta = beta_3;
		gamma = gamma_3;
		sigma = sigma_3;

	# shadowing is different for each link	
	shadowing = np.random.normal(0,sigma,1);	
	PL = 10*alpha*(np.log10(d)) + beta + 10*gamma*(np.log10(f)) + shadowing;	 # in dB
 
	return 	PL;
'''
