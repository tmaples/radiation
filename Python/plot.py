import matplotlib.pyplot as grapher
import pylab
import csv

def getXY(fileName):
	inFile = open(fileName)
	reader = csv.reader(inFile, delimiter=',', quotechar='"')
	x = []
	y = []
	for row in reader:
		x.append(float(row[0]))
		y.append(float(row[1]))
	return [x,y]

figure = grapher.figure()
a = getXY('distanceToWorkCan')

plot = figure.add_subplot(111, yscale='log', ylabel='number', xscale='log', xlabel='distance (km)', title='Distance To Work')
plot.set_ylim(1, 1e7)
plot.set_xlim(1e1, 1e4)
p1 = grapher.scatter(a[0], a[1], marker='o', c='b', lw=0, s=40)
grapher.legend([p1], ["Canada"], loc=3)
grapher.show()