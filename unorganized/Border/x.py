# dsMex = []
# dsCan = []
# regMex = []
# regCan = []

# def process(line, mylist, uid):
# 	line = line.strip().split(',');
# 	if line[1] == uid:
# 		mylist.append(line[0]+','+line[2])

# for line in open('ds'):
# 	process(line, dsMex, '303')
# 	process(line, dsCan, '301')
# for line in open('reg'):
# 	process(line, regMex, '303')
# 	process(line, regCan, '301')

# open('dsMex','w').write('\n'.join(dsMex))
# open('dsCan','w').write('\n'.join(dsCan))
# open('regMex','w').write('\n'.join(regMex))
# open('regCan','w').write('\n'.join(regCan))



mexBorder = [line.strip() for line in open('akBorderCounties')]
mexMovement = [line.strip().split(',') for line in open('regCan')]
allMovement = [line.strip().split(',') for line in open('reg')]

sumBorder = 0
sumOther = 0

for item in mexMovement:
	if item[0][:2] != '02':
		continue
	if item[0] in mexBorder:
		sumBorder += int(item[1])
	else:
		sumOther += int(item[1])

print 'Sum Border: ' + str(sumBorder)
print 'Sum Other: ' + str(sumOther)

sumAllBorder = 0
sumAllOther = 0

for item in allMovement:
	if item[0][:2] != '02':
		continue
	if item[0] in mexBorder:
		sumAllBorder += int(item[2])
	else:
		sumAllOther += int(item[2])

print 'Sum All Border: ' + str(sumAllBorder)
print 'Sum All Other: ' + str(sumAllOther)

print 'Fraction Border: ' + str(float(sumBorder)/sumAllBorder)
print 'Fraction Other: ' + str(float(sumOther)/sumAllOther)

