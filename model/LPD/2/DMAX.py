from scipy.integrate import odeint  
from pylab import * 
from numpy import * 
  
from matplotlib import rcParams
rcParams.update({'font.size': 18,'font.weight':'bold'})


N=2     #flow number

qmax= 128
DMAX=

K =65

## dctcp mark process
def ECN(x):
	global K
	if x > K:
		return 1
	else:
		return 0



D=[0]
L=[0]
A=[[],[],[]]
for k in range(10,200,10):
	DMAX=k
	queue    = [0]
	window   = [[1],[1],[1],[1],[1],[1],[1],[1],[1],[1]]
	alpha    = [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]
	deadline = [1,2,3,4,5,6,7,8,9,10]   #flow deadline
	average1=0
	average2=0
	average3=0
	interval = 50000
	ts = linspace(0.0,3.0,interval+1)
	dt = ts[1]-ts[0]  
	c = 10*1024.0*1024.0*1024/1500/8       # link capacity in packets/s
	pd = 0.0001                            # propogation delay is 100u
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

		average1+=window[0][i]
		average2+=window[1][i]
		average3+=window[2][i]

		if(q>qmax):
			q = qmax;


		if(q<0):
			q=0

		queue.append(q)
	average1/=interval
	average2/=interval
	average3/=interval
	print k,average1,average2,interval
	print average1/average2
	L.append(k)
	D.append(average1/average2)
	A[0].append(average1)
	A[1].append(average2)
	A[2].append(average3)
	average1=0
	average2=0
	average3=0

output = open('average2.txt', 'w+')
j=0;
for i in range(5,200,10):
	output.write(str(i))
	output.write(" ")
	output.write(str(A[0][j]))
	output.write(" ")
	output.write(str(A[1][j]))
	output.write(" ")
	output.write(str(A[2][j]))
	output.write("\n")
	j=j+1
print A