import numpy as np
import itertools
import random
import operator
import pdb
import networkx as nx
import math








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

