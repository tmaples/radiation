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
border = getXY('movementToCanadaObservedVsExpectedBorder')
nonBorder = getXY('movementToCanadaObservedVsExpectedNonBorder')

plot = figure.add_subplot(111, yscale='log', ylabel='Expected', xscale='log', xlabel='Observed', title='Movement to Canada')
# plot.set_ylim(1, 1e7)
# plot.set_xlim(1e1, 1e4)
p1 = grapher.scatter(border[0], border[1], marker='o', c='b', lw=0, s=20)
# p2 = grapher.scatter(nonBorder[0], nonBorder[1], marker='o', c='g', lw=0, s=20)
# grapher.legend([p1], ["Canada"], loc=3)
grapher.xlim(xmin=0)
grapher.ylim(ymin=0)
grapher.show()
