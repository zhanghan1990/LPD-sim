# encoding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import sys
from pylab import * 

from matplotlib import rcParams
rcParams.update({'font.size': 18,'weight'  : 'bold'})

patterns = ('/','//','-', '+', 'x', '\\', '\\\\', '*', 'o', 'O', '.')
N=9

#first read from file
basepath="/Users/zhanghan/Documents/文件资料/LPD/ex/FCT"  
if(sys.argv[1]=="0"):
    dctcppath=basepath+"/DCTCP/DCTCP_fct_0_"+sys.argv[2]+".SEARCH"
    d2tcppath=basepath+"/D2TCP/D2TCP_fct_0_"+sys.argv[2]+".SEARCH"
    lpdpath = basepath+"/LPD/LPD_fct_0_"+sys.argv[2]+".SEARCH"
    pfabricpath = basepath+"/pFabric/pFabric_fct_0_"+sys.argv[2]+".SEARCH"
    l2dctpath = basepath+"/L2DCT/L2DCT_fct_0_"+sys.argv[2]+".SEARCH"
else:
    dctcppath=basepath+"/DCTCP/DCTCP_fct_0_"+sys.argv[2]+".DATA"
    d2tcppath=basepath+"/D2TCP/D2TCP_fct_0_"+sys.argv[2]+".DATA"
    lpdpath = basepath+"/LPD/LPD_fct_0_"+sys.argv[2]+".DATA"
    pfabricpath = basepath+"/pFabric/pFabric_fct_0_"+sys.argv[2]+".DATA"
    l2dctpath = basepath+"/L2DCT/L2DCT_fct_0_"+sys.argv[2]+".DATA"



if(sys.argv[1]=="0"):
    updctcppath=basepath+"/DCTCP/DCTCP_fct_0_"+sys.argv[2]+".Diff_SEARCH"
    upd2tcppath=basepath+"/D2TCP/D2TCP_fct_0_"+sys.argv[2]+".Diff_SEARCH"
    uplpdpath = basepath+"/LPD/LPD_fct_0_"+sys.argv[2]+".Diff_SEARCH"
    uppfabricpath = basepath+"/pFabric/pFabric_fct_0_"+sys.argv[2]+".Diff_SEARCH"
    upl2dctpath = basepath+"/L2DCT/L2DCT_fct_0_"+sys.argv[2]+".Diff_SEARCH"
else:
    updctcppath=basepath+"/DCTCP/DCTCP_fct_0_"+sys.argv[2]+".Diff_DATA"
    upd2tcppath=basepath+"/D2TCP/D2TCP_fct_0_"+sys.argv[2]+".Diff_DATA"
    uplpdpath = basepath+"/LPD/LPD_fct_0_"+sys.argv[2]+".Diff_DATA"
    uppfabricpath = basepath+"/pFabric/pFabric_fct_0_"+sys.argv[2]+".Diff_DATA"
    upl2dctpath = basepath+"/L2DCT/L2DCT_fct_0_"+sys.argv[2]+".Diff_DATA"




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
        dctcp.append(float(array[1])*10*2)
        #updctcp.append(float(array[2])-float(array[1]))
        #if(array[1]>array[3]):
         #   downdctcp.append(float(array[1])-float(array[3]))
        #else:
         #   downdctcp.append(0)


fp=open(updctcppath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        updctcp.append(float(array[1])*10*2)
        downdctcp.append(float(array[2])*10000*4)



fp=open(lpdpath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        lpd.append(float(array[1])*10*2)
        #uplpd.append(float(array[2])-float(array[1]))
        #if(array[1]>array[3]):
         #  downlpd.append(float(array[1])-float(array[3]))
        #else:
         #  downlpd.append(0)


fp=open(uplpdpath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        uplpd.append(float(array[1])*10*2)
        downlpd.append(float(array[2])*10000*4)




fp=open(pfabricpath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        pfabric.append(float(array[1])*10*2)
       # #uppfabric.append(float(array[2])-float(array[1]))
       # if(array[1]>array[3]):
        #    downpfabric.append(float(array[1])-float(array[3]))
       # else:
         #   downpfabric.append(0)



fp=open(uppfabricpath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        uppfabric.append(float(array[1])*10*2)
        downpfabric.append(float(array[2])*10000*4)






fp=open(l2dctpath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        l2dct.append(float(array[1])*10*2)


fp=open(upl2dctpath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        upl2dct.append(float(array[1])*10*2)
        downl2dct.append(float(array[2])*10000*4)


       # upl2dct.append(float(array[2])*1.2-float(array[1])*1.2)
       # if(array[1]>array[3]):
       #     downl2dct.append(float(array[1])*.12-float(array[3])*1.2)
       # else:
       #     downl2dct.append(0)






x=np.linspace(0,1,9);

plt.figure(1)
plot(x,dctcp,linestyle='dashed', marker='o',linewidth=3,markerfacecolor='blue', markersize=12,label="DCTCP",color='blue');
plot(x,l2dct,linestyle='dashed', marker='<',linewidth=3,markerfacecolor='green', markersize=12,label="L2DCT",color='green');
plot(x,pfabric,linestyle='dashed', marker='>',linewidth=3,markerfacecolor='black', markersize=12,label="pFabric",color='black');
plot(x,lpd,linestyle='dashed', marker='d',linewidth=3,markerfacecolor='red', markersize=12,label="LPD",color='red');

xlim(0,1)
if(sys.argv[1]=="0"):
    ylabel('average FCT(s)')
    ylim(0,0.08)
else:
    ylabel('average FCT(Normalized)')
    ylim(0,10)

xlabel('load')

legend(loc=2)


if(sys.argv[1]=="0"):
    savefig("FCT_SEARCH_"+sys.argv[2]+"_"+sys.argv[1]+".eps",dpi=1000)
else:
    savefig("FCT_DATA_"+sys.argv[2]+"_"+sys.argv[1]+".eps",dpi=1000)


plt.figure(2)

plot(x,updctcp,linestyle='dashed', marker='o',linewidth=3,markerfacecolor='blue', markersize=12,label="DCTCP",color='blue');
plot(x,upl2dct,linestyle='dashed', marker='<',linewidth=3,markerfacecolor='green', markersize=12,label="L2DCT",color='green');
plot(x,uppfabric,linestyle='dashed', marker='>',linewidth=3,markerfacecolor='black', markersize=12,label="pFabric",color='black');
plot(x,uplpd,linestyle='dashed', marker='d',linewidth=3,markerfacecolor='red', markersize=12,label="LPD",color='red');

xlim(0,1)
if(sys.argv[1]=="0"):
    ylim(0,0.15)
else:
    ylim(0,40)

xlabel('load')

if(sys.argv[1]=="0"):
    savefig("FCT_SEARCH_large_"+sys.argv[2]+"_"+sys.argv[1]+".eps",dpi=1000)
else:
    savefig("FCT_DATA_large_"+sys.argv[2]+"_"+sys.argv[1]+".eps",dpi=1000)




plt.figure(3)

#plot(x,downdctcp,linestyle='dashed', marker='o',linewidth=3,markerfacecolor='blue', markersize=12,label="DCTCP");
plot(x,downl2dct,linestyle='dashed', marker='<',linewidth=3,markerfacecolor='green', markersize=12,label="L2DCT",color='green');
plot(x,downpfabric,linestyle='dashed', marker='>',linewidth=3,markerfacecolor='black', markersize=12,label="pFabric",color='black');
plot(x,downlpd,linestyle='dashed', marker='d',linewidth=3,markerfacecolor='red', markersize=12,label="LPD",color='red');

xlim(0,1)
ylim(0,10)

xlabel('load')
if(sys.argv[1]=="1"):
    ylabel('average FCT(Normalized)')

if(sys.argv[1]=="0"):
    savefig("FCT_SEARCH_small_"+sys.argv[2]+"_"+sys.argv[1]+".eps",dpi=1200)
else:
    savefig("FCT_DATA_small_"+sys.argv[2]+"_"+sys.argv[1]+".eps",dpi=1200)



#add number to this
#if(sys.argv[1]=="5"):
 #   autolabel(rects1)
  #  autolabel(rects2)
   # autolabel(rects3)
    #autolabel(rects4)
#plt.show()