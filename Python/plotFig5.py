import globals
import matplotlib.pyplot as plt
import numpy as np
import math
import csv

path = globals.projectDirectory
fluxFile = path + 'usData/fluxToUsMexicoCanada.csv'
mexDistFile = path + 'usData/distanceToMexico.csv'
canDistFile = path + 'usData/distanceToCanada.csv'

canDist = {entry['uid']:float(entry['distance']) for entry in csv.DictReader(open(canDistFile))}
mexDist = {entry['uid']:float(entry['distance']) for entry in csv.DictReader(open(mexDistFile))}

mexicoDistance = []
canadaDistance = []
mexicoError = []
canadaError = []
for entry in csv.DictReader(open(fluxFile)):
	uid = entry['uid']
	mexicoError.append(math.log10(int(entry['mexicoFluxData']) + 1) - math.log10(int(entry['mexicoFluxModel']) + 1))
	canadaError.append(math.log10(int(entry['canadaFluxData']) + 1) - math.log10(int(entry['canadaFluxModel']) + 1))
	mexicoDistance.append(mexDist[uid])
	canadaDistance.append(canDist[uid])

plt.subplot('211')
plt.xlabel('distance (km)')
plt.ylabel('error')
plt.title('Mexico')
plt.xscale('log')
plt.scatter(mexicoDistance, mexicoError, color='black', linewidth=0, alpha=0.5, s=40)

plt.subplot('212')
plt.xlabel('distance (km)')
plt.ylabel('error')
plt.title('Canada')
plt.xscale('log')
plt.scatter(canadaDistance, canadaError, color='black', linewidth=0, alpha=0.5, s=40)

plt.tight_layout()
plt.show()