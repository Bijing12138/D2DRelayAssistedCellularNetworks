import numpy as np
import itertools
import random
import operator
import pdb

def MS_Markovian(MS_loc,num_users,grid_side_loc,grid_corner_loc):
	for i in range(0,num_users):
		if MS_loc[i] in grid_side_loc:
			if MS_loc[i] in grid_corner_loc:
				if MS_loc[i] == [0.0,0.0]:
					candidate_loc = [];
					candidate_loc.append(MS_loc[i]);


					temp = list(map(operator.add,MS_loc[i],[0.0,10.0]));
					candidate_loc.append(temp);

					temp = list(map(operator.add,MS_loc[i],[10.0,0.0]));
					candidate_loc.append(temp);



				if MS_loc[i] == [0.0,2000.0]:
					candidate_loc = [];
					candidate_loc.append(MS_loc[i]);

					temp = list(map(operator.sub,MS_loc[i],[0.0,10.0]));
					candidate_loc.append(temp);

					temp = list(map(operator.add,MS_loc[i],[10.0,0.0]));
					candidate_loc.append(temp);


				if MS_loc[i] == [2000.0,0.0]:
					candidate_loc = [];
					candidate_loc.append(MS_loc[i]);

					temp = list(map(operator.add,MS_loc[i],[0.0,10.0]));
					candidate_loc.append(temp);

					temp = list(map(operator.sub,MS_loc[i],[10.0,0.0]));
					candidate_loc.append(temp);


				else:
					candidate_loc = [];
					candidate_loc.append(MS_loc[i]);

					temp = list(map(operator.sub,MS_loc[i],[0.0,10.0]));
					candidate_loc.append(temp);

					temp = list(map(operator.sub,MS_loc[i],[10.0,0.0]));
					candidate_loc.append(temp);

				
				for i in range(0,len(candidate_loc)):
					temp_loc_x = candidate_loc[i][0];
					temp_loc_y = candidate_loc[i][1];
					if (temp_loc_x < 0.0)|(temp_loc_y < 0.0):
						pdb.set_trace();


				MS_loc[i] = random.choice(candidate_loc);
	

			else:	
				if MS_loc[i][0] == 0.0:
					candidate_loc = [];
					candidate_loc.append(MS_loc[i]);

					temp = list(map(operator.sub,MS_loc[i],[0.0,10.0]));
					candidate_loc.append(temp);

					temp = list(map(operator.add,MS_loc[i],[0.0,10.0]));
					candidate_loc.append(temp);

					temp = list(map(operator.add,MS_loc[i],[10.0,0.0]));
					candidate_loc.append(temp);


				if MS_loc[i][0]	== 2000.0:
					candidate_loc = [];
					candidate_loc.append(MS_loc[i]);

					temp = list(map(operator.sub,MS_loc[i],[0.0,10.0]));
					candidate_loc.append(temp);

					temp = list(map(operator.add,MS_loc[i],[0.0,10.0]));
					candidate_loc.append(temp);

					temp = list(map(operator.sub,MS_loc[i],[10.0,0.0]));
					candidate_loc.append(temp);
			

				if MS_loc[i][1] == 0.0:
					candidate_loc = [];
					candidate_loc.append(MS_loc[i]);

					temp = list(map(operator.sub,MS_loc[i],[10.0,0.0]));
					candidate_loc.append(temp);

					temp = list(map(operator.add,MS_loc[i],[10.0,0.0]));
					candidate_loc.append(temp);

					temp = list(map(operator.add,MS_loc[i],[0.0,10.0]));
					candidate_loc.append(temp);


				else:
					candidate_loc = [];
					candidate_loc.append(MS_loc[i]);

					temp = list(map(operator.sub,MS_loc[i],[10.0,0.0]));
					candidate_loc.append(temp);

					temp = list(map(operator.add,MS_loc[i],[10.0,0.0]));
					candidate_loc.append(temp);

					temp = list(map(operator.sub,MS_loc[i],[0.0,10.0]));
					candidate_loc.append(temp);

				for i in range(0,len(candidate_loc)):
					temp_loc_x = candidate_loc[i][0];
					temp_loc_y = candidate_loc[i][1];
					if (temp_loc_x < 0.0)|(temp_loc_y < 0.0):
						pdb.set_trace();	

				MS_loc[i] = random.choice(candidate_loc);	


		else:	
			candidate_loc = [];
			candidate_loc.append(MS_loc[i])

			temp = list(map(operator.sub,MS_loc[i],[10.0,0.0]));
			candidate_loc.append(temp);

			temp = list(map(operator.sub,MS_loc[i],[0.0,10.0]));
			candidate_loc.append(temp);

			temp = list(map(operator.add,MS_loc[i],[10.0,0.0]));
			candidate_loc.append(temp);

			temp = list(map(operator.add,MS_loc[i],[0.0,10.0]));
			candidate_loc.append(temp);			

			for i in range(0,len(candidate_loc)):
				temp_loc_x = candidate_loc[i][0];
				temp_loc_y = candidate_loc[i][1];
				if (temp_loc_x < 0.0)|(temp_loc_y < 0.0):
					pdb.set_trace();

			MS_loc[i] = random.choice(candidate_loc);
			
	return MS_loc;		

