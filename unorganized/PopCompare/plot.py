import numpy as np
import pylab as plt

x = [int(line.strip()) for line in open('usaDiv')]
y = [int(line.strip()) for line in open('canSubDiv')]
z = [int(line.strip()) for line in open('canDiv')]


fig = plt.figure()
ax = fig.add_subplot(311)
weights = np.ones_like(x)/float(len(x))
n, bins, patches = ax.hist(x, weights=weights, bins=200, facecolor='g', range=(0,2e5))
ax.set_ylabel('Frequency')
ax.set_title('USA counties')
ax = fig.add_subplot(312)
weights = np.ones_like(y)/float(len(y))
n, bins, patches = ax.hist(y, weights=weights, bins=200, facecolor='g', range=(0,2e5))
ax.set_ylabel('Frequency')
ax.set_title('Canada Sub-Divisions')
ax = fig.add_subplot(313)
weights = np.ones_like(z)/float(len(z))
n, bins, patches = ax.hist(z, weights=weights, bins=200, facecolor='g', range=(0,2e5))
ax.set_xlabel('Population')
ax.set_ylabel('Frequency')
ax.set_title('Canada Divisions')

plt.show()