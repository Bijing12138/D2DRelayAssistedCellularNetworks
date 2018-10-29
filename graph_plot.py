import numpy as np
import itertools
import random
import operator
import pdb
import networkx as nx
import math
import time
import matplotlib.pyplot as plt


pdb.set_trace();

with open("relay.txt") as file:
    for relay in file:
        relay = relay.strip() #preprocess line
        #take action on line instead of storing in a list. more memory efficient at the cost of execution speed.

  

with open("no_relay.txt") as file:
    for no_relay in file:
        no_relay = no_relay.strip() #preprocess line
        #take action on line instead of storing in a list. more memory efficient at the cost of execution speed.



time_axis = list(range(1,len(relay)+1));
time_axis = np.array(time_axis);
plt.plot(time_axis[500:], relay[500:], 'b-')
plt.plot(time_axis[500:], no_relay[500:], 'r-')
plt.show()
