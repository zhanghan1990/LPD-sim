import numpy as np
import matplotlib.pyplot as plt
import sys

from matplotlib import rcParams
rcParams.update({'font.size': 18,'font.weight':'bold'})

patterns = ('/','//','-', '+', 'x', '\\', '\\\\', '*', 'o', 'O', '.')

lpd1=[0,0.1,0.5,1.3]

lpd2=[0.1,0,0.3,1]

lpd3=[0.1,0.2,0.4,1.2]



N=4

ind = np.arange(N)  # the x locations for the groups
width = 0.2     # the width of the bars

fig, ax = plt.subplots(dpi=1000)
rects1 = ax.bar(ind, lpd1, width, hatch='/',color='#ADFF2F',ecolor='k')

rects2 = ax.bar(ind+width, lpd2, width, hatch="//",color='r',ecolor='k')


rects3 = ax.bar(ind+2*width, lpd3, width, hatch='-',color='black',ecolor='k')



# add some text for labels, title and axes ticks
ax.set_xlabel('Number of machines per rack')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('10', '20', '30', '40') )
ax.legend((rects1[0], rects2[0],rects3[0]), ('LPD-e', 'LPD-d','MLD'),loc=2)
ax.set_ylabel('missing deadline(%)')
ax.set_ylim([0,3])



def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width(), height+3*rect.get_width(), '%.1f'%float(height),
                ha='center', va='bottom',fontsize='4',fontweight='bold')
fig.savefig("lpd.eps",dpi=1000)