# encoding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import sys

from matplotlib import rcParams
rcParams.update({'font.size': 18,'font.weight':'bold'})

patterns = ('/','//','-', '+', 'x', '\\', '\\\\', '*', 'o', 'O', '.')

##first read from file
basepath="/Users/zhanghan/Documents/文件资料/LPD/ex/fct"

N = 6
dctcppath=basepath+"/DCTCP/DCTCP_small_fct.SEARCH"
d2tcppath=basepath+"/D2TCP/D2TCP_small_fct.SEARCH"
lpdpath = basepath+"/LPD/LPD_small_fct.SEARCH"
pfabricpath = basepath+"/pFabric/pFabric_small_fct.SEARCH"
l2dctpath = basepath+"/L2DCT/L2DCT_small_fct.SEARCH"

dctcp=[]
updctcp=[]
downdctcp=[]


d2tcp=[]
upd2tcp=[]
downd2tcp=[]


lpd=[]
uplpd=[]
downlpd=[]


pfabric=[]
uppfabric=[]
downpfabric=[]

l2dct=[]
upl2dct=[]
downl2dct=[]



##now begin to read DCTCP
fp=open(dctcppath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        dctcp.append(float(array[1])*10000)
        updctcp.append(float(array[2])*100000-float(array[1])*100000)
        if(array[1]>array[3]):
            downdctcp.append(float(array[1])*100000-float(array[3])*100000)
        else:
            downdctcp.append(0)


fp=open(lpdpath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        print array[1]
        lpd.append(float(array[1])*10000)
        uplpd.append(float(array[2])*100000-float(array[1])*100000)
        if(array[1]>array[3]):
            downlpd.append(float(array[1])*100000-float(array[3])*100000)
        else:
            downlpd.append(0)

fp=open(pfabricpath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        pfabric.append(float(array[1])*10000)
        uppfabric.append(float(array[2])*100000-float(array[1])*100000)
        if(array[1]>array[3]):
            downpfabric.append(float(array[1])*100000-float(array[3])*100000)
        else:
            downpfabric.append(0)




fp=open(l2dctpath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        l2dct.append(float(array[1])*10000)
        upl2dct.append(float(array[2])*100000-float(array[1])*100000)
        if(array[1]>array[3]):
            downl2dct.append(float(array[1])*100000-float(array[3])*100000)
        else:
            downl2dct.append(0)






ind = np.arange(N)  # the x locations for the groups
width = 0.2       # the width of the bars

fig, ax = plt.subplots(dpi=1000)

#rects1 = ax.bar(ind, dctcp, width, hatch='/',color='green',yerr=[updctcp,downdctcp],ecolor='k')

rects2 = ax.bar(ind, l2dct, width, hatch="//",color='red',yerr=[downl2dct,upl2dct],ecolor='k')


rects3 = ax.bar(ind+width, lpd, width, hatch='-',color='k',yerr=[downlpd,uplpd],ecolor='k')

rects4 = ax.bar(ind+2*width, pfabric, width,hatch='o', color='w',yerr=[downpfabric,uppfabric],ecolor='k')


# add some text for labels, title and axes ticks
ax.set_xlabel('oversubscribed factor')
ax.set_xticks(ind+width)
ax.set_xticklabels(('5', '10', '15', '20', '25','30'))
ax.legend((rects2[0],rects3[0],rects4[0]), ('l2dct','LPD','pFabric'),loc=2)
ax.set_ylabel('Average FCT(Normalized)')
ax.set_ylim([0,40])



def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+1.1*rect.get_width(), height+5*rect.get_width(), '%.1f'%float(height),
                ha='center', va='bottom',fontsize='6',fontweight='bold')

#add number to this
autolabel(rects2)
autolabel(rects3)
autolabel(rects4)
fig.savefig("small_fct.eps",dpi=1000)
#plt.show()