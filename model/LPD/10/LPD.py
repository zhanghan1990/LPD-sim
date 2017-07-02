from scipy.integrate import odeint  
from pylab import * 
from numpy import * 
  

from matplotlib import rcParams
rcParams.update({'font.size': 18,'font.weight':'bold'})

N=10      #flow number

qmax= 128
DMAX=10.24

K =65

## dctcp mark process
def ECN(x):
	global K
	if x > K:
		return 1
	else:
		return 0



interval = 50000
ts = linspace(0.0,3.0,interval+1)
dt = ts[1]-ts[0]  


queue    = [0]
window   = [[1],[1],[1],[1],[1],[1],[1],[1],[1],[1]]
alpha    = [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]
deadline = [1,2,3,4,5,6,7,8,9,10]   #flow deadline



c = 10*1024.0*1024.0*1024/1500/8       # link capacity in packets/s
pd = 0.0001                          # propogation delay is 100u

g=1.0/16



for i in range(interval):
	rtt = pd+queue[i]/c
	temp = 0
	for j in range(N):
		w = window[j][i]
		a = alpha[j][i]
		al  = g/rtt*(ECN(queue[i])-a)*dt+a
		if(al<0):
			al=0
		if(al>1):
			al=1
		alpha[j].append(al)
		temp+=w/rtt
		win = ((1-a*deadline[j]/DMAX)/rtt-w*a*deadline[j]/DMAX*ECN(queue[i])/rtt)*dt+w
		if(win<0):
			win=0
		window[j].append(win)

	q = (temp-c)*dt+queue[i]


	if(q>qmax):
		q = qmax;


	if(q<0):
		q=0

	queue.append(q)






#we just select some points to paint

nstime=[]
nswindow=[[],[],[],[],[],[],[],[],[],[]]
nsalpha= [[],[],[],[],[],[],[],[],[],[]]
nsqueue=[]

fp = open("queue","r")

totalline= fp.readlines()
for line in totalline:
	array=line.split()
	nstime.append(array[0])
	nswindow[0].append(array[11])
	nswindow[1].append(array[12])
	nswindow[2].append(array[13])
	nswindow[3].append(array[14])
	nswindow[4].append(array[15])
	nswindow[5].append(array[16])
	nswindow[6].append(array[17])
	nswindow[7].append(array[18])
	nswindow[8].append(array[19])
	nswindow[9].append(array[20])

	nsalpha[0].append(array[21])
	nsalpha[1].append(array[22])
	nsalpha[2].append(array[23])
	nsalpha[3].append(array[24])
	nsalpha[4].append(array[25])
	nsalpha[5].append(array[26])
	nsalpha[6].append(array[27])
	nsalpha[7].append(array[28])
	nsalpha[8].append(array[29])
	nsalpha[9].append(array[30])

	nsqueue.append(array[31])


plt.figure(1) # create fig1 congestion window

plot(ts,window[0],'#FFFF00',label='fluid-flow1',linewidth=1)
plot(ts,window[1],'#FFE1FF',label='fluid-flow2',linewidth=1)
plot(ts,window[2],'#FF6347',label='fluid-flow3',linewidth=1)
plot(ts,window[3],'#F0FFF0',label='fluid-flow4',linewidth=1)
plot(ts,window[4],'#000F0F',label='fluid-flow5',linewidth=1)
plot(ts,window[5],'#EAEAEA',label='fluid-flow6',linewidth=1)
plot(ts,window[6],'#BA55D3',label='fluid-flow7',linewidth=1)
plot(ts,window[7],'#FFFFFF',label='fluid-flow8',linewidth=1)
plot(ts,window[8],'#0000FF',label='fluid-flow9',linewidth=1)
plot(ts,window[9],'#00CD66',label='fluid-flow10',linewidth=1)

#plot(ts,window[2],'k',label='fluid-flow3',linewidth=3)
plot(nstime,nswindow[0],'#FFFF00',label='fluid-flow1',linewidth=1)
plot(nstime,nswindow[1],'#FFE1FF',label='fluid-flow2',linewidth=1)
plot(nstime,nswindow[2],'#FF6347',label='fluid-flow3',linewidth=1)
plot(nstime,nswindow[3],'#F0FFF0',label='fluid-flow4',linewidth=1)
plot(nstime,nswindow[4],'#000F0F',label='fluid-flow5',linewidth=1)
plot(nstime,nswindow[5],'#EAEAEA',label='fluid-flow6',linewidth=1)
plot(nstime,nswindow[6],'#BA55D3',label='fluid-flow7',linewidth=1)
plot(nstime,nswindow[7],'#FFFFFF',label='fluid-flow8',linewidth=1)
plot(nstime,nswindow[8],'#0000FF',label='fluid-flow9',linewidth=1)
plot(nstime,nswindow[9],'#00CD66',label='fluid-flow10',linewidth=1)
#plot(nstime,nswindow[2],'c',label='ns-flow3',linewidth=3)

xlim(0.3,0.35)
ylim(0,200)

xlabel('time')
ylabel('window(pkts)')

savefig("window.eps");
plt.figure(2) # create fig  2m alpha

plot(ts,alpha[0],'r',label='fluid-flow1',linewidth=3)

#plot(ts,window[2],'k',label='fluid-flow3',linewidth=3)
plot(nstime,nsalpha[0],'#FFFF00',label='fluid-flow1',linewidth=1)
plot(nstime,nsalpha[1],'#FFE1FF',label='fluid-flow2',linewidth=1)
plot(nstime,nsalpha[2],'#FF6347',label='fluid-flow3',linewidth=1)
plot(nstime,nsalpha[3],'#F0FFF0',label='fluid-flow4',linewidth=1)
plot(nstime,nsalpha[4],'#000F0F',label='fluid-flow5',linewidth=1)
plot(nstime,nsalpha[5],'#EAEAEA',label='fluid-flow6',linewidth=1)
plot(nstime,nsalpha[6],'#BA55D3',label='fluid-flow7',linewidth=1)
plot(nstime,nsalpha[7],'#FFFFFF',label='fluid-flow8',linewidth=1)
plot(nstime,nsalpha[8],'#0000FF',label='fluid-flow9',linewidth=1)
plot(nstime,nsalpha[9],'#00CD66',label='fluid-flow10',linewidth=1)
#plot(nstime,nsalpha[2],'c',label='ns-flow3',linewidth=3)

xlim(0.3,0.35)
ylim(0,1)

xlabel('time')
ylabel('alpha')


savefig("alpha.eps");

plt.figure(3) # create fig3 queue length

plot(ts,queue,'r',label='fluid-queue',linewidth=3)
plot(nstime,nsqueue,'b',label='ns-queue',linewidth=3)

xlim(0.3,0.35)
ylim(0,200)

xlabel('time')
ylabel('queue(pkts)')
legend()



savefig("queue.eps");











show();