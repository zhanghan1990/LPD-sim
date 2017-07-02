import numpy as np
import matplotlib.pyplot as plt
import sys

from matplotlib import rcParams
rcParams.update({'font.size': 18,'weight'  : 'bold'})

patterns = ('/','//','-', '+', 'x', '\\', '\\\\', '*', 'o', 'O', '.')

##first read from file
basepath="/Users/zhanghan/Documents/file/ex2"

N = 9
dctcppath=basepath+"/DCTCP/DCTCP_fct_"+sys.argv[1]+".result"
d2tcppath=basepath+"/D2TCP/D2TCP_fct_"+sys.argv[1]+".result"
lpdpath = basepath+"/LPD/LPD_fct_"+sys.argv[1]+".result"
pfabricpath = basepath+"/pFabric/pFabric_fct_"+sys.argv[1]+".result"

dctcp=[]
d2tcp=[]
lpd=[]
pfabric=[]


##now begin to read DCTCP
fp=open(dctcppath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        dctcp.append(float(array[1])*100)

#begein to read d2tcp

fp=open(d2tcppath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        d2tcp.append(float(array[1])*100)

fp=open(lpdpath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        lpd.append(float(array[1])*100)

fp=open(pfabricpath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        pfabric.append(float(array[1])*100)



ind = np.arange(N)  # the x locations for the groups
width = 0.2       # the width of the bars

fig, ax = plt.subplots(dpi=100)
rects1 = ax.bar(ind, dctcp, width, hatch='/',color='blue')

rects2 = ax.bar(ind+width, d2tcp, width, hatch="//",color='yellow')


rects3 = ax.bar(ind+2*width, pfabric, width, hatch='+',color='green')

rects4 = ax.bar(ind+3*width, lpd, width,hatch='o', color='red')


# add some text for labels, title and axes ticks
ax.set_ylabel('Percentage of flows missing deadline(%)')
ax.set_xlabel('load')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('0.1', '0.2', '0.3', '0.4', '0.5','0.6','0.7','0.8','0.9') )
ax.legend((rects1[0], rects2[0],rects3[0],rects4[0]), ('dctcp', 'd2tcp','pFabric','LPD'),loc=2)
ax.set_ylim([0,20])

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%f'%float(height),
                ha='center', va='bottom')

#add number to this
#autolabel(rects1)
#autolabel(rects2)
#autolabel(rects3)
fig.savefig("miss_deadline_"+sys.argv[1]+".pdf",dpi=1000)
#plt.show()