from scipy.integrate import odeint  
from pylab import * 
from numpy import * 
  
from matplotlib import rcParams
rcParams.update({'font.size': 18,'font.weight':'bold'})


N=2     #flow number

qmax= 10000
DMAX=115

K =65

## dctcp mark process
def ECN(x):
	global K
	if x >= K:
		return 1
	else:
		return 0



interval1=5000
interval2=15000

S =0.0
E =2.0
deadline_min=0.3
deadline_max=0.6

wc_max=5
wc_min=1




interval = interval1+interval2
ts = linspace(S,E,interval+1)
dt = ts[1]-ts[0]  


queue    = [0]
window   = [[1],[0],[0],[0],[0],[0],[0],[0],[0],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1]]
alpha    = [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]
start	 =[0,0.5]
c = 10*1024.0*1024.0*1024/1500/8       # link capacity in packets/s
pd = 0.0001                           # propogation delay is 100u
g=1.0/16



def now(t):
	return (E-S)/interval*t





def penalty(during):
	if(during<deadline_min):
		return wc_max
	elif(during>deadline_max):
		return wc_min
	else:
		return wc_max-(during-deadline_min)*(wc_max-wc_min)/(deadline_max-deadline_min)






#the first stage, only flow 1
for i in range(interval1):
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
		if(w==0):
			win=0
		else:
			win = ((1-a/penalty(now(i)-start[j]))/rtt-w*a/penalty(now(i)-start[j])*ECN(queue[i])/rtt)*dt+w
		if(win<0):
			win=0
		#print win
		else:
			window[j].append(win)
	q = (temp-c)*dt+queue[i]
	if(q>qmax):
		q = qmax;
	if(q<0):
		q=0
	queue.append(q)
window[1][interval1]=1;
#print window[0]





#flow 2 start 
for i in range(interval1,interval):
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
		if(w==0):
			win=0
		else:
			win = ((1-a/penalty(now(i)-start[j]))/rtt-w*a/penalty(now(i)-start[j])*ECN(queue[i])/rtt)*dt+w
		if(win<0):
			win=0
		window[j].append(win)
	q = (temp-c)*dt+queue[i]
	if(q>qmax):
		q = qmax;
	if(q<0):
		q=0
	queue.append(q)


nstime=[]
nswindow=[[],[],[],[],[],[],[],[],[],[]]
nsalpha= [[],[],[],[],[],[],[],[],[],[]]
nsqueue=[]

fp = open("2","r")

totalline= fp.readlines()
for line in totalline:
	array=line.split()
	nstime.append(array[0])
	nswindow[0].append(array[3])
	nswindow[1].append(array[4])
	nsalpha[0].append(float(array[5]))
	nsalpha[1].append(float(array[6]))
	nsqueue.append(array[7])


plt.figure(1) # create fig1 congestion window

plot(ts,window[0],'r',label='fluid-flow1',linewidth=3)
plot(ts,window[1],'y',label='fluid-flow2',linewidth=3)
#plot(ts,window[2],'k',label='fluid-flow3',linewidth=3)
plot(nstime,nswindow[0],'b',label='ns-flow1',linewidth=3)
plot(nstime,nswindow[1],'g',label='ns-flow2',linewidth=3)
#plot(nstime,nswindow[2],'c',label='ns-flow3',linewidth=3)

xlim(0.0,2.0)
ylim(0,200)

xlabel('time')
ylabel('window(pkts)')

legend()
savefig("window.eps");
plt.figure(2) # create fig  2m alpha

plot(ts,alpha[0],'r',label='fluid-flow1',linewidth=3)
plot(ts,alpha[1],'y',label='fluid-flow2',linewidth=3)
#plot(ts,alpha[2],'k',label='fluid-flow3',linewidth=3)
plot(nstime,nsalpha[0],'b',label='ns-flow1',linewidth=3)
plot(nstime,nsalpha[1],'g',label='ns-flow2',linewidth=3)
#plot(nstime,nsalpha[2],'c',label='ns-flow3',linewidth=3)
legend()

xlim(0.0,2.0)
ylim(0,1)

xlabel('time')
ylabel('alpha')


savefig("alpha.eps");

plt.figure(3) # create fig3 queue length

plot(ts,queue,'r',label='fluid-queue',linewidth=3)
plot(nstime,nsqueue,'b',label='ns-queue',linewidth=3)

xlim(0.0,2.0)
ylim(0,200)

xlabel('time')
ylabel('queue(pkts)')
legend()

savefig("queue.eps");


print queue









show();