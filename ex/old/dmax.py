# encoding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import sys
from pylab import * 

from matplotlib import rcParams
rcParams.update({'font.size': 18,'weight'  : 'bold'})

patterns = ('/','//','-', '+', 'x', '\\', '\\\\', '*', 'o', 'O', '.')





x=[20,30,40,50,60,70,80,90,100,110,120,130,140,150,160]
flow20=[2.5,2.6,2.5,2.6,2.85,3.05,3.33,3.41,3.5,4.2,5,5.2,5.5,6,6.5]
flow30=[2.7,2.8,2.8,2.9,3.1,3.5,4.0,4.2,4.3,4.5,4.6,5.0,6.6,6.7,7.0]
flow40=[2.9,3.0,3.1,3.2,3.5,3.9,4.2,4.4,4.8,5.1,5.5,6.0,6.9,7.2,7.8]


plot(x,flow20,linestyle='dashed', marker='D',linewidth=3,markerfacecolor='red', markersize=18,label="fan-in-degree 20",color='black')
plot(x,flow30,linestyle='dashed', marker='>',linewidth=3,markerfacecolor='blue', markersize=18,label="fan-in-degree 30",color='black')
plot(x,flow40,linestyle='dashed', marker='^',linewidth=3,markerfacecolor='black', markersize=18,label="fan-in-degree 40",color='black')


xlim(10,160)
ylim(0,10)

xlabel('t_max(ms)')
ylabel('Percentage of flows missing deadline')

legend(loc=2)
savefig("DMAX.eps",dpi=1200)


show();