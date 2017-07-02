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

dctcp=[0,0,0.19,0.38,0.32,0.43,0.42,0.41,0.46]
d2tcp=[0,1,0.2,0.4,0.3,0.4,0.4,0.41,0.45]
lpd=[0,0,0.21,0.33,0.31,0.39,0.43,0.41,0.45]

ind = np.arange(N)  # the x locations for the groups
width = 0.3       # the width of the bars

fig, ax = plt.subplots(dpi=1000)
rects1 = ax.bar(ind, dctcp, width, hatch='/',color='#ADFF2F',ecolor='k')

rects2 = ax.bar(ind+width, d2tcp, width, hatch="//",color='r',ecolor='k')


#rects3 = ax.bar(ind+2*width, l2dct, width, hatch='-',color='w',yerr=[upl2dct,downl2dct],ecolor='k')

rects4 = ax.bar(ind+2*width, lpd, width,hatch='o', color='k',ecolor='k')


# add some text for labels, title and axes ticks
ax.set_xlabel('load')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('0.1', '0.2', '0.3', '0.4', '0.5','0.6','0.7','0.8','0.9') )
ax.legend((rects1[0], rects2[0],rects4[0]), ('LPD-e', 'LPD-d','MLD'),loc=2)
ax.set_ylabel('missing deadline(%)')
ax.set_ylim([0,10])



def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+1.4*rect.get_width(), height+3*rect.get_width(), '%.1f'%float(height),
                ha='center', va='bottom',fontsize='6',fontweight='bold')

#add number to this
fig.savefig("diss_miss_deadline_.eps",dpi=1000)
#plt.show()