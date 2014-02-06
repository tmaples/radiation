import numpy

canDiv = [int(line.strip()) for line in open('canDiv')]
canSubDiv = [int(line.strip()) for line in open('canSubDiv')]
usaDiv = [int(line.strip()) for line in open('usaDiv')]

x = canDiv
print 'Canada Divisions'
print 'median: ' + str(int(numpy.median(x)))
print 'mean:   ' + str(int(numpy.mean(x)))
print 'sdev:   ' + str(int(numpy.std(x)))
x = canSubDiv
print 'Canada Sub-Divisions'
print 'median: ' + str(int(numpy.median(x)))
print 'mean:   ' + str(int(numpy.mean(x)))
print 'sdev:   ' + str(int(numpy.std(x)))
x = usaDiv
print 'USA counties'
print 'median: ' + str(int(numpy.median(x)))
print 'mean:   ' + str(int(numpy.mean(x)))
print 'sdev:   ' + str(int(numpy.std(x)))

# x = range(10,20000010,10)
# canDivy = [0]*2000000
# canSubDivy = [0]*2000000
# usaDivy = [0]*2000000


# for pop in canDiv:
# 	for i in range(2000000):
# 		if pop < x[i]:
# 			canDivy[i] += 1
# 			break

# for pop in canSubDiv:
# 	for i in range(2000000):
# 		if pop < x[i]:
# 			canSubDivy[i] += 1
# 			break

# for pop in usaDiv:
# 	for i in range(2000000):
# 		if pop < x[i]:
# 			usaDivy[i] += 1
# 			break

# canDivOut = []
# canSubDivOut = []
# canSubDivOut = []


# open('usaDiv','w').write('\n'.join(lines))