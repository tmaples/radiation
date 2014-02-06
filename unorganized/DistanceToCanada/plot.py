import matplotlib.pyplot as grapher
import pylab
import csv

def getXY(fileName):
	inFile = open(fileName)
	reader = csv.reader(inFile, delimiter=',', quotechar='"')
	x = []
	y = []
	for row in reader:
		if int(round(float(row[1]))) != 0:
			x.append(float(row[0]))
			y.append(float(row[1]))
	return [x,y]

figure = grapher.figure()
a = getXY('distFromBorderVsError.csv')

plot = figure.add_subplot(111, ylabel='error', xscale='log', xlabel='distance (km)', title='Distance to Canada vs Error')
p1 = grapher.scatter(a[0], a[1], marker='o', c='b', lw=0, s=20)
# grapher.legend([p1], ["Canada"], loc=3)
# grapher.xlim(xmin=0)
# grapher.ylim(ymin=0)
grapher.show()
