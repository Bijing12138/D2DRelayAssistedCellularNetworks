import numpy as np
import itertools
import random
import operator
import pdb
import networkx as nx
import math


def arrival_cdf_func(PPP_lambda_packet,PPP_max_num_packet):
	PPP_prob = [];
	PPP_cdf = [];
	for i in range(0,PPP_max_num_packet):  
	# per packet memory is taken as 65507 bits
		prob_temp = ((PPP_lambda_packet**i)/float(math.factorial(i)))*math.exp(-PPP_lambda_packet);
		PPP_prob.append(prob_temp);

	normalization = np.sum(PPP_prob);   # breakpoint here
	PPP_prob = PPP_prob/normalization;

	for i in range(0,len(PPP_prob)):
		if i == 0:
			PPP_cdf.append(PPP_prob[i]);
		else:
			prob_temp = PPP_cdf[i-1] + PPP_prob[i];
			PPP_cdf.append(prob_temp);

	del prob_temp;
	del normalization;	

	return PPP_cdf;