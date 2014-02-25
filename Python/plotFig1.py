import globals
import matplotlib.pyplot as plt
import csv

path = globals.projectDirectory + 'usData/'
inputFileName = path + 'dataVsModelUsContiguousToContiguousNoZeros.csv'

def getXY(fileName):
	inFile = open(fileName)
	reader = csv.DictReader(inFile, delimiter=',', quotechar='"')
	x = []
	y = []
	for row in reader:
		x.append(float(row['data']) + 1)
		y.append(float(row['model']) + 1)
	return [x,y]

a = getXY(inputFileName)
plt.subplot('111')
plt.xlabel('Travelers (US Census Data)')
plt.ylabel('Travelers (Radiation Model)')
plt.yscale('log')
plt.xscale('log')
plt.xlim([1e-1,1e6])
plt.ylim([1e-1,1e6])
plt.scatter(a[0], a[1], marker='o', c='gray', lw=0, s=5)
plt.plot([1e-1,1e6],[1e-1,1e6], c='black', lw=1)
plt.show()