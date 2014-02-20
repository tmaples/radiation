import globals
import matplotlib.pyplot as plt
import csv

path = globals.projectDirectory + 'usData/'
fluxModelFileName = path + 'fluxWithinUsContiguousModel.csv'
fluxDataFileName = path + 'fluxWithinUsContiguousData.csv'
distFileName = path + 'distancesWithinUsContiguous.csv'

# distReader = csv.DictReader(open(distFileName), delimiter=',', quotechar='"')
# distances = {entry['source+dest']:float(entry['distance']) for entry in distReader}
# fluxReaderModel = csv.DictReader(open(fluxModelFileName), delimiter=',', quotechar='"')
# fluxModel = {entry['source+dest']:int(entry['flux']) for entry in fluxReaderModel}
# fluxReaderData = csv.DictReader(open(fluxDataFileName), delimiter=',', quotechar='"')
# fluxData = {entry['source+dest']:int(entry['flux']) for entry in fluxReaderData}

x = []
i, j, inc = 0, 4, 0.125
while i <= j:
	x.append(pow(10,i))
	i += inc

data = [0.0, 0.0, 0.0, 0.0001217912182899475, 0.0010080857574739338, 0.00010765616157481786, 0.000297326905822295, 0.0006472877998444428, 0.003079360558132467, 0.002758098670921706, 0.01044780298011755, 0.00828543382479786, 0.01595763585411007, 0.021253376491020985, 0.017919560720899723, 0.006888832916465204, 0.002679820968912447, 0.0009415223010081287, 0.0002770720556472251, 0.00024343749414708034, 6.953510318140166e-05, 4.263211816492391e-05, 2.4356899967593624e-05, 1.466244996844207e-05, 1.032135140712395e-05, 7.314329324953338e-06, 5.930449579821088e-06, 2.7688951508299075e-06, 1.7001871733779334e-06, 1.1622692730639445e-06, 3.4899874653806184e-08, 0.0, 0.0]
model = [0.0, 0.0, 0.0, 0.00010632029434810137, 0.0007096176933938369, 0.0002510660965716793, 0.0004453711548681073, 0.001450643580957506, 0.00732134643928983, 0.0033287144764811375, 0.00763195622762762, 0.011688862111824364, 0.02190380875897753, 0.023520533569054206, 0.013312099361580088, 0.004213348495675448, 0.0020283515519582194, 0.0011454580012806295, 0.0005095546144277444, 0.00034757635871162306, 0.00016125054282797248, 8.958680392683228e-05, 4.9621409511566995e-05, 2.365813221568073e-05, 1.3209565410046477e-05, 7.3321459074130855e-06, 3.4012704695915253e-06, 1.7593074712100707e-06, 1.0769377984928592e-06, 5.01349184599807e-07, 6.605702692506535e-09, 0.0, 0.0]

# data = [0]*len(x)
# model = [0]*len(x)

# for uid in fluxModel:
# 	dist = distances[uid]
# 	n = fluxModel[uid]
# 	for i in range(len(x)):
# 		if dist <= x[i]:
# 			model[i] += n
# 			break

# for uid in fluxData:
# 	if uid[:5] == uid[5:]:
# 		continue
# 	dist = distances[uid]
# 	n = fluxData[uid]
# 	for i in range(len(x)):
# 		if dist <= x[i]:
# 			data[i] += n
# 			break

# modelSum = sum(model)
# for i in range(len(model)):
# 	model[i] = float(model[i]) / modelSum

# dataSum = sum(data)
# for i in range(len(data)):
# 	data[i] = float(data[i]) / dataSum

# for i in range(1,len(model)):
# 	model[i] = float(model[i]) / (x[i] - x[i-1])
# 	data[i] = float(data[i]) / (x[i] - x[i-1])

plt.subplot('111')
plt.xlabel('distance (km)')
plt.ylabel('Pdist(r)')
plt.yscale('log')
plt.xscale('log')
plt.xlim([1e0,1e4])
plt.scatter(x, model, marker='o', c='r', lw=0, s=20, label='Radiation Model')
plt.scatter(x, data, marker='o', c='b', lw=0, s=20, label='US Census Data')
plt.plot(x, model, c='r', lw=1)
plt.plot(x, data, c='b', lw=1)
plt.legend(loc='lower left')
plt.show()