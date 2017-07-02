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
dctcppath=basepath+"/average/DCTCP_fct.SEARCH"
d2tcppath=basepath+"/average/D2TCP_fct.SEARCH"
lpdpath = basepath+"/average/LPD_fct.SEARCH"
pfabricpath = basepath+"/average/pFabric_fct.SEARCH"
l2dctpath = basepath+"/average/L2DCT_fct.SEARCH"

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
        dctcp.append(float(array[1])*100)
        updctcp.append(float(array[2])*100-float(array[1])*100)
        if(array[1]>array[3]):
            downdctcp.append(float(array[1])*100-float(array[3])*100)
        else:
            downdctcp.append(0)


fp=open(lpdpath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        print array[1]
        lpd.append(float(array[1])*100)
        uplpd.append(float(array[2])*100-float(array[1])*100)
        if(array[1]>array[3]):
            downlpd.append(float(array[1])*100-float(array[3])*100)
        else:
            downlpd.append(0)

fp=open(pfabricpath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        pfabric.append(float(array[1])*100)
        uppfabric.append(float(array[2])*100-float(array[1])*100)
        if(array[1]>array[3]):
            downpfabric.append(float(array[1])*100-float(array[3])*100)
        else:
            downpfabric.append(0)




fp=open(l2dctpath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        l2dct.append(float(array[1])*100)
        upl2dct.append(float(array[2])*100-float(array[1])*100)
        if(array[1]>array[3]):
            downl2dct.append(float(array[1])*100-float(array[3])*100)
        else:
            downl2dct.append(0)






ind = np.arange(N)  # the x locations for the groups
width = 0.2       # the width of the bars

fig, ax = plt.subplots(dpi=1000)

rects1 = ax.bar(ind, dctcp, width, hatch='/',color='#ADFF2F',yerr=[updctcp,downdctcp],ecolor='k')

rects2 = ax.bar(ind+width, l2dct, width, hatch="//",color='red',yerr=[upl2dct,downl2dct],ecolor='k')


rects3 = ax.bar(ind+2*width, lpd, width, hatch='-',color='k',yerr=[uplpd,downlpd],ecolor='k')

rects4 = ax.bar(ind+3*width, pfabric, width,hatch='/', color='w',yerr=[uppfabric,downpfabric],ecolor='k')


# add some text for labels, title and axes ticks
ax.set_xlabel('oversubscription factor')
ax.set_xticks(ind+width)
ax.set_xticklabels(('5', '10', '15', '20', '25','30'))
ax.legend((rects1[0], rects2[0],rects3[0],rects4[0]), ('DCTCP', 'L2DCT','FDRC','pFabric'),loc=2)
ax.set_ylabel('Average FCT(Normalized)')
ax.set_ylim([0,100])



def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+1.1*rect.get_width(), height+5*rect.get_width(), '%.1f'%float(height),
                ha='center', va='bottom',fontsize='6',fontweight='bold')

#add number to this
#autolabel(rects1)
#autolabel(rects2)
#autolabel(rects3)
#autolabel(rects4)
fig.savefig("fct.eps",dpi=1000)
#plt.show()