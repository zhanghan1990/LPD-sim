# encoding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import sys

from matplotlib import rcParams
rcParams.update({'font.size': 18,'font.weight':'bold'})

patterns = ('/','//','-', '+', 'x', '\\', '\\\\', '*', 'o', 'O', '.')

dctcp=[15,16,18,22]
updctcp=[2,2,5,3]
downdctcp=[8,11,12,14]


d2tcp=[7,12,13,15]
upd2tcp=[4,2,5,4]
downd2tcp=[1,1,1,4]


l2dct=[6,11,15,16]
upl2dct=[2,5,2,6]
downl2dct=[2,1,3,2]


lpd=[4,5,8,10]
uplpd=[1,2,2,3]
downlpd=[1.3,1.2,2,2]

karuna = [3,4,8.1,11]
uplpd=[1,2,2,3]
downlpd=[1.3,1.2,2,2]



N=4

ind = np.arange(N)  # the x locations for the groups
width = 0.2     # the width of the bars

fig, ax = plt.subplots(dpi=1000)
rects1 = ax.bar(ind, dctcp, width, hatch='/',color='#ADFF2F',yerr=[downdctcp,updctcp],ecolor='k')

rects2 = ax.bar(ind+width, d2tcp, width, hatch="//",color='r',yerr=[downd2tcp,upd2tcp],ecolor='k')


rects3 = ax.bar(ind+2*width, l2dct, width, hatch='-',color='w',yerr=[downl2dct,upl2dct],ecolor='k')

rects4 = ax.bar(ind+3*width, lpd,   width,hatch='o', color='k',yerr=[downlpd,uplpd],ecolor='k')

rects5 = ax.bar(ind+4*width, karuna,   width,hatch='o', color='b',yerr=[downlpd,uplpd],ecolor='k')


# add some text for labels, title and axes ticks
ax.set_xlabel('fan-in degree')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('10', '20', '30', '40') )
ax.legend((rects1[0], rects2[0],rects3[0],rects4[0],rects5[0]), ('DCTCP', 'D2TCP','L2DCT','LPD','Karuna'),loc=2)
ax.set_ylabel('missing deadline(%)')
ax.set_ylim([0,35])



def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width(), height+3*rect.get_width(), '%.1f'%float(height),
                ha='center', va='bottom',fontsize='4',fontweight='bold')
fig.savefig("tight.eps",dpi=1000)
#plt.show()




dctcp=[10,11,12,13]
updctcp=[5,5,5,6]
downdctcp=[6,6,7,8]


d2tcp=[6,9,10,11]
upd2tcp=[2,2,1,2]
downd2tcp=[1,1,1,4]


l2dct=[3,5,6,8]
upl2dct=[2,5,2,6]
downl2dct=[2,1,3,2]


lpd=[1,2,3,4]
uplpd=[1,2,2,3]
downlpd=[0.5,1.2,2,2]

karuna = [0.8,1.6,2.9,5]
uplpd=[1,2,2,3]
downlpd=[0.5,1.2,2,2]


N=4

ind = np.arange(N)  # the x locations for the groups
width = 0.2     # the width of the bars

fig, ax = plt.subplots(dpi=1000)
rects1 = ax.bar(ind, dctcp, width, hatch='/',color='#ADFF2F',yerr=[downdctcp,updctcp],ecolor='k')

rects2 = ax.bar(ind+width, d2tcp, width, hatch="//",color='r',yerr=[downd2tcp,upd2tcp],ecolor='k')


rects3 = ax.bar(ind+2*width, l2dct, width, hatch='-',color='w',yerr=[downl2dct,upl2dct],ecolor='k')

rects4 = ax.bar(ind+3*width, lpd,   width,hatch='o', color='k',yerr=[downlpd,uplpd],ecolor='k')

rects5 = ax.bar(ind+4*width, karuna,   width,hatch='o', color='b',yerr=[downlpd,uplpd],ecolor='k')


# add some text for labels, title and axes ticks
ax.set_xlabel('fan-in degree')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('10', '20', '30', '40') )
ax.legend((rects1[0], rects2[0],rects3[0],rects4[0],rects5[0]), ('DCTCP', 'D2TCP','L2DCT','LPD','Karuna'),loc=2)
ax.set_ylabel('missing deadline(%)')
ax.set_ylim([0,35])



def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width(), height+3*rect.get_width(), '%.1f'%float(height),
                ha='center', va='bottom',fontsize='4',fontweight='bold')
fig.savefig("moderate.eps",dpi=1000)
#plt.show()





dctcp=[5,6,7,9]
updctcp=[2,2,2,3]
downdctcp=[1,2,3,4]


d2tcp=[2,4,5,6]
upd2tcp=[1,2,3,2]
downd2tcp=[1,1,1,4]


l2dct=[2,3,4,5]
upl2dct=[2,5,2,6]
downl2dct=[1,2,1,2]


lpd=[0.5,1,2,3]
uplpd=[1,2,2,1]
downlpd=[0.1,1,1,2]

karuna = [0.4,0.9,1.7,2]
uplpd=[1,2,2,1]
downlpd=[0.1,1,1,1]



N=4

ind = np.arange(N)  # the x locations for the groups
width = 0.2     # the width of the bars

fig, ax = plt.subplots(dpi=1000)
rects1 = ax.bar(ind, dctcp, width, hatch='/',color='#ADFF2F',yerr=[downdctcp,updctcp],ecolor='k')

rects2 = ax.bar(ind+width, d2tcp, width, hatch="//",color='r',yerr=[downd2tcp,upd2tcp],ecolor='k')


rects3 = ax.bar(ind+2*width, l2dct, width, hatch='-',color='w',yerr=[downl2dct,upl2dct],ecolor='k')

rects4 = ax.bar(ind+3*width, lpd,   width,hatch='o', color='k',yerr=[downlpd,uplpd],ecolor='k')

rects5 = ax.bar(ind+4*width, karuna,   width,hatch='o', color='b',yerr=[downlpd,uplpd],ecolor='k')

# add some text for labels, title and axes ticks
ax.set_xlabel('fan-in degree')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('10', '20', '30', '40') )
ax.legend((rects1[0], rects2[0],rects3[0],rects4[0],rects5[0]), ('DCTCP', 'D2TCP','L2DCT','LPD','Karuna'),loc=2)
ax.set_ylabel('missing deadline(%)')
ax.set_ylim([0,35])



def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width(), height+3*rect.get_width(), '%.1f'%float(height),
                ha='center', va='bottom',fontsize='4',fontweight='bold')
fig.savefig("lax.eps",dpi=1000)
#plt.show()







dctcp=[5,7,7,9]
updctcp=[2,2,2,3]
downdctcp=[1,2,3,4]


d2tcp=[3,4,5,6]
upd2tcp=[1,2,3,2]
downd2tcp=[1,1,1,4]


l2dct=[4,3,5,8]
upl2dct=[2,5,2,6]
downl2dct=[1,2,1,2]


lpd=[1,2,3,4]
uplpd=[1,2,2,1]
downlpd=[0.1,1,1,2]


karuna = [0.8,1.8,2.8,4.1]
uplpd=[1,2,2,1]
downlpd=[0.1,1,1,2]



N=4

ind = np.arange(N)  # the x locations for the groups
width = 0.2     # the width of the bars

fig, ax = plt.subplots(dpi=1000)
rects1 = ax.bar(ind, dctcp, width, hatch='/',color='#ADFF2F',yerr=[downdctcp,updctcp],ecolor='k')

rects2 = ax.bar(ind+width, d2tcp, width, hatch="//",color='r',yerr=[downd2tcp,upd2tcp],ecolor='k')


rects3 = ax.bar(ind+2*width, l2dct, width, hatch='-',color='w',yerr=[downl2dct,upl2dct],ecolor='k')

rects4 = ax.bar(ind+3*width, lpd,   width,hatch='o', color='k',yerr=[downlpd,uplpd],ecolor='k')

rects5 = ax.bar(ind+4*width, karuna,   width,hatch='o', color='b',yerr=[downlpd,uplpd],ecolor='k')

# add some text for labels, title and axes ticks
ax.set_xlabel('fan-in degree')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('10', '20', '30', '40') )

ax.legend((rects1[0], rects2[0],rects3[0],rects4[0],rects5[0]), ('DCTCP', 'D2TCP','L2DCT','LPD','Karuna'),loc=2)
ax.set_ylabel('missing deadline(%)')
ax.set_ylim([0,25])



def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width(), height+3*rect.get_width(), '%.1f'%float(height),
                ha='center', va='bottom',fontsize='4',fontweight='bold')
fig.savefig("tight1.eps",dpi=1000)
#plt.show()





dctcp=[4,6,7,8]
updctcp=[2,2,2,3]
downdctcp=[1,2,3,4]


d2tcp=[2,3,4,5]
upd2tcp=[1,2,3,2]
downd2tcp=[1,1,1,4]


l2dct=[2,2.5,3.5,5.2]
upl2dct=[2,5,2,6]
downl2dct=[1,2,1,2]


lpd=[0.5,1.5,3,4]
uplpd=[1,2,2,1]
downlpd=[0.1,1,1,2]

karuna = [0.4,1.4,2.8,4.1]
uplpd=[1,2,2,1]
downlpd=[0.1,1,1,2]

N=4

ind = np.arange(N)  # the x locations for the groups
width = 0.2     # the width of the bars

fig, ax = plt.subplots(dpi=1000)
rects1 = ax.bar(ind, dctcp, width, hatch='/',color='#ADFF2F',yerr=[downdctcp,updctcp],ecolor='k')

rects2 = ax.bar(ind+width, d2tcp, width, hatch="//",color='r',yerr=[downd2tcp,upd2tcp],ecolor='k')


rects3 = ax.bar(ind+2*width, l2dct, width, hatch='-',color='w',yerr=[downl2dct,upl2dct],ecolor='k')

rects4 = ax.bar(ind+3*width, lpd,   width,hatch='o', color='k',yerr=[downlpd,uplpd],ecolor='k')
rects5 = ax.bar(ind+4*width, karuna,   width,hatch='o', color='b',yerr=[downlpd,uplpd],ecolor='k')

# add some text for labels, title and axes ticks
ax.set_xlabel('fan-in degree')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('10', '20', '30', '40') )
ax.legend((rects1[0], rects2[0],rects3[0],rects4[0],rects5[0]), ('DCTCP', 'D2TCP','L2DCT','LPD','Karuna'),loc=2)
ax.set_ylabel('missing deadline(%)')
ax.set_ylim([0,25])



def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width(), height+3*rect.get_width(), '%.1f'%float(height),
                ha='center', va='bottom',fontsize='4',fontweight='bold')
fig.savefig("moderate1.eps",dpi=1000)







dctcp=[3,5,6,7]
updctcp=[2,2,2,3]
downdctcp=[1,2,3,4]


d2tcp=[1,2,3,4]
upd2tcp=[1,2,3,2]
downd2tcp=[1,1,1,4]


l2dct=[1,1.5,2.5,4.2]
upl2dct=[2,5,2,6]
downl2dct=[1,2,1,2]


lpd=[0,1,2,3]
uplpd=[0,1,2,1]
downlpd=[0,0.2,1,2]

karuna = [0,0.9,1.8,2.8]
uplpd=[0,1,2,1]
downlpd=[0,0.2,1,2]

N=4

ind = np.arange(N)  # the x locations for the groups
width = 0.2     # the width of the bars

fig, ax = plt.subplots(dpi=1000)
rects1 = ax.bar(ind, dctcp, width, hatch='/',color='#ADFF2F',yerr=[downdctcp,updctcp],ecolor='k')

rects2 = ax.bar(ind+width, d2tcp, width, hatch="//",color='r',yerr=[downd2tcp,upd2tcp],ecolor='k')


rects3 = ax.bar(ind+2*width, l2dct, width, hatch='-',color='w',yerr=[downl2dct,upl2dct],ecolor='k')

rects4 = ax.bar(ind+3*width, lpd,   width,hatch='o', color='k',yerr=[downlpd,uplpd],ecolor='k')
rects5 = ax.bar(ind+4*width, karuna,   width,hatch='o', color='b',yerr=[downlpd,uplpd],ecolor='k')

# add some text for labels, title and axes ticks
ax.set_xlabel('fan-in degree')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('10', '20', '30', '40') )

ax.legend((rects1[0], rects2[0],rects3[0],rects4[0],rects5[0]), ('DCTCP', 'D2TCP','L2DCT','LPD','Karuna'),loc=2)
ax.set_ylabel('missing deadline(%)')
ax.set_ylim([0,25])



def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width(), height+3*rect.get_width(), '%.1f'%float(height),
                ha='center', va='bottom',fontsize='4',fontweight='bold')
fig.savefig("lax1.eps",dpi=1000)























dctcp=[4,6.5,7,10]
updctcp=[2,2,2,3]
downdctcp=[1,2,3,4]


d2tcp=[3,5,6,7]
upd2tcp=[1,2,3,2]
downd2tcp=[1,1,1,4]


l2dct=[3.1,3,5.8,6.8]
upl2dct=[2,5,2,6]
downl2dct=[1,2,1,2]


lpd=[1,2,2.5,3]
uplpd=[1,2,2,1]
downlpd=[0.1,1,1,2]

karuna = [0,1.9,2.3,3.2]
uplpd=[1,2,2,1]
downlpd=[0.1,1,1,2]

N=4

ind = np.arange(N)  # the x locations for the groups
width = 0.2     # the width of the bars

fig, ax = plt.subplots(dpi=1000)
rects1 = ax.bar(ind, dctcp, width, hatch='/',color='#ADFF2F',yerr=[downdctcp,updctcp],ecolor='k')

rects2 = ax.bar(ind+width, d2tcp, width, hatch="//",color='r',yerr=[downd2tcp,upd2tcp],ecolor='k')


rects3 = ax.bar(ind+2*width, l2dct, width, hatch='-',color='w',yerr=[downl2dct,upl2dct],ecolor='k')

rects4 = ax.bar(ind+3*width, lpd,   width,hatch='o', color='k',yerr=[downlpd,uplpd],ecolor='k')

rects5 = ax.bar(ind+4*width, karuna,   width,hatch='o', color='b',yerr=[downlpd,uplpd],ecolor='k')

# add some text for labels, title and axes ticks
ax.set_xlabel('fan-in degree')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('10', '20', '30', '40') )

ax.legend((rects1[0], rects2[0],rects3[0],rects4[0],rects5[0]), ('DCTCP', 'D2TCP','L2DCT','LPD','Karuna'),loc=2)
ax.set_ylabel('missing deadline(%)')
ax.set_ylim([0,25])



def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width(), height+3*rect.get_width(), '%.1f'%float(height),
                ha='center', va='bottom',fontsize='4',fontweight='bold')
fig.savefig("tight2.eps",dpi=1000)
#plt.show()





dctcp=[4.3,6,7.8,7.4]
updctcp=[2,2,2,5]
downdctcp=[1,2,3,2]


d2tcp=[2,3,4,5]
upd2tcp=[1,2,3,3]
downd2tcp=[1,1,1,4]


l2dct=[2,2.5,3.5,5.2]
upl2dct=[2,5,2,2]
downl2dct=[1,2,1,2]


lpd=[0,1.5,3,4]
uplpd=[0,2,2,2]
downlpd=[0,1,1,2]


karuna = [0,1.3,2.4,2.9]
uplpd=[0,2,2,2]
downlpd=[0,1,1,2]

N=4

ind = np.arange(N)  # the x locations for the groups
width = 0.2     # the width of the bars

fig, ax = plt.subplots(dpi=1000)
rects1 = ax.bar(ind, dctcp, width, hatch='/',color='#ADFF2F',yerr=[downdctcp,updctcp],ecolor='k')

rects2 = ax.bar(ind+width, d2tcp, width, hatch="//",color='r',yerr=[downd2tcp,upd2tcp],ecolor='k')


rects3 = ax.bar(ind+2*width, l2dct, width, hatch='-',color='w',yerr=[downl2dct,upl2dct],ecolor='k')

rects4 = ax.bar(ind+3*width, lpd,   width,hatch='o', color='k',yerr=[downlpd,uplpd],ecolor='k')

rects5 = ax.bar(ind+4*width, karuna,   width,hatch='o', color='b',yerr=[downlpd,uplpd],ecolor='k')

# add some text for labels, title and axes ticks
ax.set_xlabel('fan-in degree')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('10', '20', '30', '40') )

ax.legend((rects1[0], rects2[0],rects3[0],rects4[0],rects5[0]), ('DCTCP', 'D2TCP','L2DCT','LPD','Karuna'),loc=2)
ax.set_ylabel('missing deadline(%)')
ax.set_ylim([0,25])



def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width(), height+3*rect.get_width(), '%.1f'%float(height),
                ha='center', va='bottom',fontsize='4',fontweight='bold')
fig.savefig("moderate2.eps",dpi=1000)







dctcp=[3,5,6,7]
updctcp=[2,2,2,3]
downdctcp=[1,2,3,4]


d2tcp=[1,2,3,4]
upd2tcp=[1,2,3,2]
downd2tcp=[1,1,1,4]


l2dct=[1,1.5,2.5,3.5]
upl2dct=[2,5,2,6]
downl2dct=[1,2,1,2]


lpd=[0,1,2,3]
uplpd=[0,1,2,1]
downlpd=[0,0.2,1,2]

lpd=[0,0.9,1.7,2.7]
uplpd=[0,1,2,1]
downlpd=[0,0.2,1,2]

N=4

ind = np.arange(N)  # the x locations for the groups
width = 0.2     # the width of the bars

fig, ax = plt.subplots(dpi=1000)
rects1 = ax.bar(ind, dctcp, width, hatch='/',color='#ADFF2F',yerr=[downdctcp,updctcp],ecolor='k')

rects2 = ax.bar(ind+width, d2tcp, width, hatch="//",color='r',yerr=[downd2tcp,upd2tcp],ecolor='k')


rects3 = ax.bar(ind+2*width, l2dct, width, hatch='-',color='w',yerr=[downl2dct,upl2dct],ecolor='k')

rects4 = ax.bar(ind+3*width, lpd,   width,hatch='o', color='k',yerr=[downlpd,uplpd],ecolor='k')

rects5 = ax.bar(ind+4*width, karuna,   width,hatch='o', color='b',yerr=[downlpd,uplpd],ecolor='k')

# add some text for labels, title and axes ticks
ax.set_xlabel('fan-in degree')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('10', '20', '30', '40') )

ax.legend((rects1[0], rects2[0],rects3[0],rects4[0],rects5[0]), ('DCTCP', 'D2TCP','L2DCT','LPD','Karuna'),loc=2)
ax.set_ylabel('missing deadline(%)')
ax.set_ylim([0,25])



def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width(), height+3*rect.get_width(), '%.1f'%float(height),
                ha='center', va='bottom',fontsize='4',fontweight='bold')
fig.savefig("lax2.eps",dpi=1000)










