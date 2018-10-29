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


'''
import sys

def info(type, value, tb):
    if hasattr(sys, 'ps1') or not sys.stderr.isatty():
    # we are in interactive mode or we don't have a tty-like
    # device, so we call the default hook
        sys.__excepthook__(type, value, tb)
    else:
        import traceback, pdb
        # we are NOT in interactive mode, print the exception...
        traceback.print_exception(type, value, tb)
        print
        # ...then start the debugger in post-mortem mode.
        # pdb.pm() # deprecated
        pdb.post_mortem(tb) # more "modern"

sys.excepthook = info

'''
#pdb.set_trace();


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


# location initialization
MS_loc = [];
for i in range(0,num_users):
	MS_loc.append(random.choice(grid));

print (MS_loc);	

start_time = time.time();
PL = PL_ABG(MS_loc,num_users,BS_loc);
print(time.time()	- start_time);

print (PL);






