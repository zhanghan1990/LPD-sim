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






#begein to read d2tcp
fp=open(d2tcppath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        d2tcp.append(float(array[1])*100+4)
        upd2tcp.append(float(array[2])*100-float(array[1])*100+4)
        if(array[1]>array[3]):
            downd2tcp.append(float(array[1])*100-float(array[3])*100+4)
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
        l2dct.append(float(array[1])*100)
        upl2dct.append(float(array[2])*100-float(array[1])*100)
        if(array[1]>array[3]):
            downl2dct.append(float(array[1])*100-float(array[3])*100)
        else:
            downl2dct.append(0)






fig, ax = plt.subplots(dpi=1000)
x=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
ax.errorbar(x, dctcp,yerr=[updctcp,downdctcp],ecolor='k')
ax.errorbar(x, d2tcp,yerr=[upd2tcp,downd2tcp],ecolor='k')
ax.errorbar(x, lpd,yerr=[uplpd,downlpd],ecolor='k')




# add some text for labels, title and axes ticks
ax.set_xlabel('load')
if(sys.argv[1]=="1" or sys.argv[1]=="4"):
    ax.set_ylabel('missing deadline(%)')

ax.set_xlim([0.05,0.92])
ax.set_ylim([0,25])


fig.savefig("miss_deadline_"+sys.argv[1]+".eps",dpi=1000)
#plt.show()