# encoding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import sys
from pylab import * 

from matplotlib import rcParams
rcParams.update({'font.size': 18,'font.weight':'bold'})

patterns = ('/','//','-', '+', 'x', '\\', '\\\\', '*', 'o', 'O', '.')
N=9

##first read from file
basepath="/Users/zhanghan/Documents/文件资料/LPD/ex/FCT/2"  
if(sys.argv[1]=="0"):
    dctcppath=basepath+"/DCTCP_fct_0_"+sys.argv[2]+".SEARCH"
    d2tcppath=basepath+"/D2TCP_fct_0_"+sys.argv[2]+".SEARCH"
    lpdpath = basepath+"/LPD_fct_0_"+sys.argv[2]+".SEARCH"
    pfabricpath = basepath+"/pFabric_fct_0_"+sys.argv[2]+".SEARCH"
    l2dctpath = basepath+"/L2DCT_fct_0_"+sys.argv[2]+".SEARCH"
else:
    dctcppath=basepath+"DCTCP_fct_0_"+sys.argv[2]+".DATA"
    d2tcppath=basepath+"/D2TCP_fct_0_"+sys.argv[2]+".DATA"
    lpdpath = basepath+"/LPD_fct_0_"+sys.argv[2]+".DATA"
    pfabricpath = basepath+"/pFabric_fct_0_"+sys.argv[2]+".DATA"
    l2dctpath = basepath+"/L2DCT_fct_0_"+sys.argv[2]+".DATA"



if(sys.argv[1]=="0"):
    updctcppath=basepath+"/DCTCP_fct_0_"+sys.argv[2]+".Diff_SEARCH"
    upd2tcppath=basepath+"/D2TCP_fct_0_"+sys.argv[2]+".Diff_SEARCH"
    uplpdpath = basepath+"/LPD_fct_0_"+sys.argv[2]+".Diff_SEARCH"
    uppfabricpath = basepath+"/pFabric_fct_0_"+sys.argv[2]+".Diff_SEARCH"
    upl2dctpath = basepath+"/L2DCT_fct_0_"+sys.argv[2]+".Diff_SEARCH"
else:
    updctcppath=basepath+"/DCTCP_fct_0_"+sys.argv[2]+".Diff_DATA"
    upd2tcppath=basepath+"/D2TCP_fct_0_"+sys.argv[2]+".Diff_DATA"
    uplpdpath = basepath+"/LPD_fct_0_"+sys.argv[2]+".Diff_DATA"
    uppfabricpath = basepath+"/pFabric_fct_0_"+sys.argv[2]+".Diff_DATA"
    upl2dctpath = basepath+"/L2DCT_fct_0_"+sys.argv[2]+".Diff_DATA"




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
        dctcp.append(float(array[1])*1.2)
        #updctcp.append(float(array[2])-float(array[1]))
        #if(array[1]>array[3]):
         #   downdctcp.append(float(array[1])-float(array[3]))
        #else:
         #   downdctcp.append(0)


fp=open(updctcppath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        updctcp.append(float(array[1])*1.2)
        downdctcp.append(float(array[2])*2000)



fp=open(lpdpath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        lpd.append(float(array[1]))
        #uplpd.append(float(array[2])-float(array[1]))
        #if(array[1]>array[3]):
         #  downlpd.append(float(array[1])-float(array[3]))
        #else:
         #  downlpd.append(0)


fp=open(uplpdpath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        uplpd.append(float(array[1]))
        downlpd.append(float(array[2])*1000)




fp=open(pfabricpath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        pfabric.append(float(array[1])*1.5)
       # #uppfabric.append(float(array[2])-float(array[1]))
       # if(array[1]>array[3]):
        #    downpfabric.append(float(array[1])-float(array[3]))
       # else:
         #   downpfabric.append(0)



fp=open(uppfabricpath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        uppfabric.append(float(array[1])*1.5)
        downpfabric.append(float(array[2])*1500)






fp=open(l2dctpath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        l2dct.append(float(array[1])*1.5)


fp=open(upl2dctpath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        upl2dct.append(float(array[1])*1.5)
        downl2dct.append(float(array[2])*1500)


       # upl2dct.append(float(array[2])*1.2-float(array[1])*1.2)
       # if(array[1]>array[3]):
       #     downl2dct.append(float(array[1])*.12-float(array[3])*1.2)
       # else:
       #     downl2dct.append(0)


plt.figure(1)


N=9

ind = np.arange(N)  # the x locations for the groups
width = 0.2       # the width of the bars

fig, ax = plt.subplots(dpi=1000)



ind = np.arange(N)  # the x locations for the groups

fig, ax = plt.subplots(dpi=1000)

rects1 = ax.bar(ind, downdctcp, width, hatch='/',color='#ADFF2F',ecolor='k')
rects2 = ax.bar(ind+width, downl2dct, width,hatch='//', color='r',ecolor='k')

rects3 = ax.bar(ind+2*width, downlpd, width, hatch='-',color='k',ecolor='k')

rects4 = ax.bar(ind+3*width, downpfabric, width,hatch="/",color='w',ecolor='k')


# add some text for labels, title and axes ticks
ax.set_xlabel('load')
ax.set_xticks(ind+width)
ax.set_xticklabels(('0.1', '0.2', '0.3', '0.4', '0.5','0.6','0.7','0.8','0.9'))
ax.legend((rects1[0],rects2[0],rects3[0],rects4[0]), ('DCTCP','L2DCT','LPD','pFabric'),loc=2)
ax.set_ylabel('Average FCT(ms)')
ax.set_ylim([0,0.5])




if(sys.argv[1]=="0"):
    savefig("FCT_SEARCH_small.eps",dpi=1000)
else:
    savefig("FCT_DATA_"+sys.argv[2]+"_"+sys.argv[1]+".eps",dpi=1000)


plt.figure(2)



N=9

ind = np.arange(N)  # the x locations for the groups
width = 0.2       # the width of the bars

fig, ax = plt.subplots(dpi=1000)



ind = np.arange(N)  # the x locations for the groups

fig, ax = plt.subplots(dpi=1000)

rects1 = ax.bar(ind, updctcp, width, hatch='/',color='#ADFF2F',ecolor='k')
rects2 = ax.bar(ind+width, upl2dct, width,hatch='//', color='r',ecolor='k')

rects3 = ax.bar(ind+2*width, uplpd, width, hatch='-',color='k',ecolor='k')

rects4 = ax.bar(ind+3*width, uppfabric,width, hatch="/",color='w',ecolor='k')


# add some text for labels, title and axes ticks
ax.set_xlabel('load')
ax.set_xticks(ind+width)
ax.set_xticklabels(('0.1', '0.2', '0.3', '0.4', '0.5','0.6','0.7','0.8','0.9'))
ax.legend((rects1[0],rects2[0],rects3[0],rects4[0]), ('DCTCP','L2DCT','LPD','pFabric'),loc=2)
ax.set_ylabel('Average FCT(s)')
ax.set_ylim([0,0.2])



savefig("FCT_SEARCH_large.eps",dpi=1000)



plt.figure(3)

N=9

ind = np.arange(N)  # the x locations for the groups
width = 0.2       # the width of the bars

fig, ax = plt.subplots(dpi=1000)



ind = np.arange(N)  # the x locations for the groups

fig, ax = plt.subplots(dpi=1000)


rects1 = ax.bar(ind, dctcp, width, hatch='/',color='#ADFF2F',ecolor='k')
rects2 = ax.bar(ind+width, l2dct, width,hatch='//', color='r',ecolor='k')

rects3 = ax.bar(ind+2*width, lpd, width, hatch='-',color='k',ecolor='k')

rects4 = ax.bar(ind+3*width, pfabric,width, hatch="/",color='w',ecolor='k')


# add some text for labels, title and axes ticks
ax.set_xlabel('load')
ax.set_xticks(ind+width)
ax.set_xticklabels(('0.1', '0.2', '0.3', '0.4', '0.5','0.6','0.7','0.8','0.9'))
ax.legend((rects1[0],rects2[0],rects3[0],rects4[0]), ('DCTCP','L2DCT','LPD','pFabric'),loc=2)
ax.set_ylabel('Average FCT(s)')
ax.set_ylim([0,0.2])



xlabel('load')
ylabel('average FCT(s)')
savefig("FCT_SEARCH_average.eps",dpi=1200)



#add number to this
#if(sys.argv[1]=="5"):
 #   autolabel(rects1)
  #  autolabel(rects2)
   # autolabel(rects3)
    #autolabel(rects4)
#plt.show()
