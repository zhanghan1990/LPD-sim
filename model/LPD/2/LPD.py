from scipy.integrate import odeint  
from pylab import * 
from numpy import * 
  
from matplotlib import rcParams
rcParams.update({'font.size': 18,'font.weight':'bold'})


N=2 	#flow number

qmax= 10000
DMAX=200

K=60

## dctcp mark process
def ECN(x):
	global K
	if x >= K:
		return 1
	else:
		return 0



interval = 50000
ts = linspace(0.0,3.0,interval+1)
dt = ts[1]-ts[0]  

n=[1,2,5,7,10,12,15,17,20,22,25,27,30]

for N in n:
	queue    = [0]
	window   = [[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1]]
	alpha    = [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]
	deadline = [1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10]   #flow deadline



	c = 10*1024.0*1024.0*1024/1500/8       # link capacity in packets/s
	pd = 0.001                           # propogation delay is 100u

	g=0.2


	maxqueue = 0
	minqueue = 1000

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

		if q > maxqueue and i > 1000:
			maxqueue = q
		if q < minqueue and i > 1000:
			minqueue = q

		queue.append(q)




	average1=0

	for i in range(0,N):
		for j in range(interval):
			average1+=window[i][j]


	average1/=interval;
	average1/=N


	#we just select some points to paint

	nstime=[]
	nswindow=[[],[],[],[],[],[],[],[],[],[]]
	nsalpha= [[],[],[],[],[],[],[],[],[],[]]
	nsqueue=[]




	plt.figure(1) 

	plot(ts,queue,'r',label='fluid-queue',linewidth=3)

	xlim(0.1,0.105)
	ylim(0,200)

	xlabel('time')
	ylabel('queue(pkts)')
	legend()

	print average1,maxqueue,minqueue











#show();