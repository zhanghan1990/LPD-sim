# encoding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import sys
from pylab import * 

from matplotlib import rcParams
rcParams.update({'font.size': 18,'font.weight':'bold'})

patterns = ('/','//','-', '+', 'x', '\\', '\\\\', '*', 'o', 'O', '.')


x=[]
fluidw1=[]
fluidw2=[]
nsw1=[]
nsw2=[]

fluidratio=[]
nsratio=[]

##now begin to read DCTCP
fp=open("averag2.txt","r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        x.append(float(array[0]))
        fluidw1.append(float(array[1]))
        fluidw2.append(float(array[2]))
        nsw1.append(float(array[3]))
        nsw2.append(float(array[4]))
        fluidratio.append(float(array[1])/float(array[2]))
        nsratio.append(float(array[3])/float(array[4]));


plt.figure(1)

#plot(x,downdctcp,linestyle='dashed', marker='o',linewidth=3,markerfacecolor='blue', markersize=12,label="DCTCP");
plot(x,fluidratio,linestyle='dashed', marker='o',linewidth=3,markerfacecolor='red', markersize=12,label="fluid model",color='green')
plot(x,nsratio,linestyle='dashed', marker='>',linewidth=3,markerfacecolor='blue', markersize=12,label="ns-2",color='black')

xlim(0,110)
ylim(0,5)

xlabel('tmax')
ylabel('w1/w2')

legend()


savefig("ratio.eps",dpi=1200)


plt.figure(2)

xlim(0,110)
ylim(0,200)


plot(x,fluidw1,linestyle='dashed', marker='o',linewidth=3,markerfacecolor='red', markersize=12,label="fluid flow1",color='green')
plot(x,nsw1,linestyle='dashed', marker='>',linewidth=3,markerfacecolor='green', markersize=12,label="ns flow1",color='green')

plot(x,fluidw2,linestyle='dashed', marker='.',linewidth=3,markerfacecolor='blue', markersize=12,label="fluid flow2",color='black')
plot(x,nsw2,linestyle='dashed', marker='>',linewidth=3,markerfacecolor='black', markersize=12,label="ns flow2",color='black')



xlabel('tmax')
ylabel('congestion window')

legend()
savefig("window2.eps",dpi=1200)


show();