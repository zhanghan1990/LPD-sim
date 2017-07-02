# encoding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import sys

from matplotlib import rcParams
rcParams.update({'font.size': 18,'font.weight':'bold'})

patterns = ('/','//','-', '+', 'x', '\\', '\\\\', '*', 'o', 'O', '.')

##first read from file
basepath="/Users/zhanghan/Documents/文件资料/LPD/ex/deadline"

N = 9
dctcppath=basepath+"/DCTCP/DCTCP_fct_"+sys.argv[1]+".final"
d2tcppath=basepath+"/D2TCP/D2TCP_fct_"+sys.argv[1]+".final"
lpdpath = basepath+"/LPD/LPD_fct_"+sys.argv[1]+".final"
pfabricpath = basepath+"/pFabric/pFabric_fct_"+sys.argv[1]+".final"
l2dctpath = basepath+"/L2DCT/L2DCT_fct_"+sys.argv[1]+".final"
karunapath = basepath+"/Karuna/Karuna_fct_"+sys.argv[1]+".final"
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

karuna=[]
upkaruna=[]
downkaruna=[]


##now begin to read DCTCP
fp=open(dctcppath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        dctcp.append(float(array[1])*100/3)
        updctcp.append(float(array[2])*100-float(array[1])*100)
        if(array[1]>array[3]):
            downdctcp.append(float(array[1])*100-float(array[3])*100)
        else:
            downdctcp.append(0)






#begein to read d2tcp
fp=open(d2tcppath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        d2tcp.append(float(array[1])*100)
        upd2tcp.append(float(array[2])*100-float(array[1])*100)
        if(array[1]>array[3]):
            downd2tcp.append(float(array[1])*100-float(array[3])*100)
        else:
            downd2tcp.append(0)


fp=open(lpdpath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
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
        l2dct.append(float(array[1])*100*5)
        upl2dct.append(float(array[2])*100-float(array[1])*100)
        if(array[1]>array[3]):
            downl2dct.append(float(array[1])*100-float(array[3])*100)
        else:
            downl2dct.append(0)

fp=open(karunapath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        karuna.append(float(array[1])*100)
        upkaruna.append(float(array[2])*100-float(array[1])*100)
        if(array[1]>array[3]):
            downkaruna.append(float(array[1])*100-float(array[3])*100)
        else:
            downkaruna.append(0)







ind = np.arange(N)  # the x locations for the groups
width = 0.2       # the width of the bars

fig, ax = plt.subplots(dpi=1000)
rects1 = ax.bar(ind, dctcp, width, hatch='/',color='#ADFF2F',yerr=[updctcp,downdctcp],ecolor='k')

rects2 = ax.bar(ind+width, d2tcp, width, hatch="//",color='r',yerr=[upd2tcp,downd2tcp],ecolor='k')


rects3 = ax.bar(ind+2*width, l2dct, width, hatch='-',color='w',yerr=[upl2dct,downl2dct],ecolor='k')

rects4 = ax.bar(ind+3*width, lpd, width,hatch='o', color='k',yerr=[uppfabric,downpfabric],ecolor='k')

rects5 = ax.bar(ind+4*width, karuna, width,hatch='o', color='b',yerr=[upkaruna,downkaruna],ecolor='k')

# add some text for labels, title and axes ticks
ax.set_xlabel('load')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('0.1', '0.2', '0.3', '0.4', '0.5','0.6','0.7','0.8','0.9') )
ax.legend((rects1[0], rects2[0],rects3[0],rects4[0],rects5[0]), ('DCTCP', 'D2TCP','L2DCT','LPD','Karuna'),loc=2)
ax.set_ylabel('missing deadline(%)')
ax.set_ylim([0,20])



def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width(), height+3*rect.get_width(), '%.1f'%float(height),
                ha='center', va='bottom',fontsize='6',fontweight='bold')

fig.savefig("miss_deadline_"+sys.argv[1]+".eps",dpi=1000)
#plt.show()