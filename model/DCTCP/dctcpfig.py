from scipy.integrate import odeint  
from pylab import * 
from numpy import * 
import matplotlib.pyplot as plt
  


N=2       #flow number

qmax= 128

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


c = 10*1024.0*1024.0*1024/1500/8       # link capacity in packets/s
pd = 0.0001                          # propogation delay is 100u

g=1.0/16



for i in range(interval):
	rtt = pd+queue[i]/c
	w= window[0][i]
	a = alpha[0][i]
	al  = g/rtt*(ECN(queue[i])-a)*dt+a
	q = (int)(N*w/rtt-c)*dt+queue[i]

	if(q>qmax):
		q = qmax;

	if(q<0):
		q=0
	if(al<0):
		al=0
	if(al>1):
		al=1

	queue.append(q)

	for j in range(N):
		win = (int)(1/rtt-w*a*ECN(queue[i])/2/rtt)*dt+w
		if(win<0):
			win=0
		window[j].append(win)
		alpha[j].append(al)





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
	nswindow[0].append(array[3])
	nswindow[1].append(array[4])
	nsalpha[0].append(array[5])
	nsalpha[1].append(array[6])
	nsqueue.append(array[7])


plt.figure(1) # create fig1 congestion window

plot(ts,window[1],'r',label='fluid-flow',linewidth=3)
plot(nstime,nswindow[1],'b',label='ns-flow1',linewidth=3)
plot(nstime,nswindow[0],'g',label='ns-flow2',linewidth=3)

xlim(1.00,1.02)
ylim(0,200)

xlabel('time')
ylabel('window(pkts)')

legend()
savefig("window.pdf");
plt.figure(2) # create fig  2m alpha

plot(ts,alpha[1],'r',label='fluid-alpha',linewidth=3)
plot(nstime,nsalpha[1],'b',label='ns-flow1',linewidth=3)
plot(nstime,nsalpha[0],'g',label='ns-flow2',linewidth=3)
legend()

xlim(1.00,1.02)
ylim(0,1)

xlabel('time')
ylabel('alpha')


savefig("alpha.pdf");

plt.figure(3) # create fig3 queue length

plot(ts,queue,'r',label='fluid-queue',linewidth=3)
plot(nstime,nsqueue,'b',label='ns-queue',linewidth=3)

xlim(1.00,1.02)
ylim(0,200)

xlabel('time')
ylabel('queue(pkts)')
legend()



savefig("queue.pdf");











show();