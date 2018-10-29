
# this is the main file
# the code is for Algorithm 1 in the paper



import numpy as np
import itertools
import random
import operator
import pdb
import networkx as nx
import math
import time
import matplotlib.pyplot as plt



from pow_level_sel_no_relay import opt_pow_sel_MS_BS_link_no_relay
from MS_Movement import MS_Markovian
from PL_models import PL_ABG
from arrival_cdf import arrival_cdf_func
from processing_no_relay import sys_processing_no_relay
from processing_relay import sys_processing_relay




# creating a grid
grid_lines  = np.linspace(0,2000,num = 201);
grid_lines = grid_lines.tolist();
grid = list(itertools.product(grid_lines,repeat=2));

for i in range(0,len(grid)):
	grid[i] = list(grid[i]);

grid_side_loc = [];
for i in range(1,len(grid_lines)-1):
	grid_side_loc.append([0.0,grid_lines[i]]);
	grid_side_loc.append([grid_lines[i],0.0]);
	grid_side_loc.append([2000.0,grid_lines[i]]);
	grid_side_loc.append([grid_lines[i],2000.0]);

grid_corner_loc = [[0.0,0.0],[0.0,2000.0],[2000.0,0.0],[2000.0,2000.0]];
grid_side_loc = grid_side_loc + grid_corner_loc;






# creating users list, initial grid location , queue lengths
BS_loc = [1000.0,1000.0]; # BS location
num_users = 60; # increasing by 2, increases time by approx 3.5 times




# start of the MArkovian process
N_inf = 40000;
pow_lev = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]; #in Watt
num_PRB = 50; # increasing by 2, increases time by 2 times

P_avg = 28; # in dBm

# defining prob distribution...using memoryless property of poisson point process
#PPP_lambda = 80*(10**3);
PPP_lambda_packet_list = [20]; # eack packet size is 65507 bits


#pdb.set_trace();	


Packet_size = 25000; 
			


# set buffer period 
T = 20;

start_time = time.time();


for PPP_lambda_packet in PPP_lambda_packet_list:


	# for plotting
	arrival_minus_dep_relay = []; # average over MS
	arrival_minus_dep_no_relay = []; # average over MS


	PPP_max_num_packet = 50;
	PPP_cdf = arrival_cdf_func(PPP_lambda_packet,PPP_max_num_packet);

	print("Num of users is: %s" %(num_users));
	print("Num of PRB is: %s" %(num_PRB));
	print("Avg arrival rate: %s" %(PPP_lambda_packet));




	# location initialization
	MS_loc = [];
	for i in range(0,num_users):
		MS_loc.append(random.choice(grid));

	print (MS_loc);	









	# no relay queue initialization
	# queue length initialization
	# initial queue length is taken as 0
	X_no_relay = [];
	U_no_relay = [];
	for i in range(0,num_users):
		X_no_relay.append(50);
		U_no_relay.append(28);


	X_T_no_relay = [];
	U_T_no_relay = [];
	for i in range(0,num_users):
		X_T_no_relay.append(50);
		U_T_no_relay.append(28);





	X_relay = [];
	Y_relay = [];
	U_relay = [];
	for i in range(0,num_users):
		X_relay.append(50);
		Y_relay.append(50);
		U_relay.append(28);


	X_T_relay = [];
	Y_T_relay = [];
	U_T_relay = [];
	for i in range(0,num_users):
		X_T_relay.append(50);
		Y_T_relay.append(50);
		U_T_relay.append(28);






	for n in range(1,N_inf):

		

		# deciding upon the position of the MS
		MS_loc = MS_Markovian(MS_loc,num_users,grid_side_loc,grid_corner_loc);





		# for relay system
		if n%T == 0:
			for i in range(0,num_users):
				X_T_relay[i] = X_relay[i];
				Y_T_relay[i] = Y_relay[i];
				U_T_relay[i] = U_relay[i];

				

		X_relay,Y_relay,U_relay,temp1 = sys_processing_relay(X_relay,Y_relay,U_relay,X_T_relay,Y_T_relay,U_T_relay,PPP_cdf,num_users,num_PRB,pow_lev,MS_loc,BS_loc,P_avg);		
		arrival_minus_dep_relay.append(temp1);






		# for no relay system 
		if n%T == 0:
			for i in range(0,num_users):
				X_T_no_relay[i] = X_no_relay[i];
				U_T_no_relay[i] = U_no_relay[i];


		X_no_relay,U_no_relay,temp2 = sys_processing_no_relay(X_no_relay,U_no_relay,X_T_no_relay,U_T_no_relay,PPP_cdf,num_users,num_PRB,pow_lev,MS_loc,BS_loc,P_avg);
		arrival_minus_dep_no_relay.append(temp2);
				

	print("--- %s seconds ---" % (time.time() - start_time))


	print("Num of users is: %s" %(num_users));
	print("Num of PRB is: %s" %(num_PRB));
	print("Avg arrival rate: %s" %(PPP_lambda_packet));

	'''
	print("Relay_data");

	print (X_relay);
	print (Y_relay);
	print (U_relay);

	print("No_relay_data");

	print (X_no_relay);
	print (U_no_relay);
	'''


	print (MS_loc);
	#avg_U = np.sum(U_list)/len(U_list);
	#print avg_U;

	#arrival_minus_dep_relay_1 = np.array(arrival_minus_dep_relay[0:(N_inf)]);

	with open("Relay.txt", "w") as output:
	    output.write(str(arrival_minus_dep_relay));


	with open("No_Relay.txt", "w") as output:
	    output.write(str(arrival_minus_dep_no_relay));

	# plot
	time_axis = list(range(1,len(arrival_minus_dep_no_relay)+1));
	time_axis = np.array(time_axis);
	plt.plot(time_axis[50:], arrival_minus_dep_relay[50:], 'b-',label = 'Delay with Relay')
	plt.plot(time_axis[50:], arrival_minus_dep_no_relay[50:], 'r-',label = 'Delay with no Relay')
	plt.xlabel('Time')
	plt.ylabel('Delay')
	plt.legend(loc = 'upper right')
	name = 'num_users_' + str(num_users) + '_num_PRB_' + str(num_PRB) + '_Arrival_Rate_'+str(PPP_lambda_packet) + '_Packet_size_' + str(Packet_size);
	#text = 'number of users:' + str(num_users) + ', num of PRB are:' + str(num_PRB) + ', Arrival Rate:'+str(PPP_lambda_packet);
	#plt.text(N_inf/2,100,name,fontsize =5)
	plt.savefig(name)
	plt.gcf().clear()




	del X_relay;
	del Y_relay;
	del U_relay;
	del X_no_relay;
	del U_no_relay;
	del X_T_relay;
	del Y_T_relay;
	del U_T_relay;
	del X_T_no_relay;
	del U_T_no_relay;
	del PPP_cdf;
	del MS_loc;
	del arrival_minus_dep_relay;
	del arrival_minus_dep_no_relay;



	#print X_list;



