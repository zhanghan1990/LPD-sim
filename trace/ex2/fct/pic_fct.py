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
        dctcp.append(float(array[1]))

#begein to read d2tcp

fp=open(d2tcppath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        d2tcp.append(float(array[1]))

fp=open(lpdpath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        lpd.append(float(array[1]))

fp=open(pfabricpath,"r")
totaline = fp.readlines()
for line in totaline:
        array = line.split()
        pfabric.append(float(array[1]))




x = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

plt.plot(np.array(x), np.array(dctcp), 'o', linewidth=2)
plt.plot(np.array(x), np.array(pfabric), '+', linewidth=2)
plt.plot(np.array(x), np.array(lpd), '*', linewidth=2)





plt.show()