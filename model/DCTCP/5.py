import numpy as np 
import matplotlib.pyplot as plt 
plt.figure(1) # create fig1
plt.figure(2) # create fig2
ax1 = plt.subplot(211)
ax2 = plt.subplot(212)

x = np.linspace(0,3,100)

for i in xrange(5):
	plt.figure(1)
	plt.plot(x,np.exp(i*x/3),label="$x^3$")
	plt.legend()
	plt.sca(ax1)
	plt.plot(x,np.sin(i*x),label="curve2")
	plt.legend()
	plt.sca(ax2)
	plt.plot(x,np.cos(i*x),label="curve3")
	plt.legend()

plt.show()