from ctypes import *
import os
import numpy as np
from numpy.ctypeslib import ndpointer
from scipy.optimize import minimize

N = 5867
N_DATA_COL = 3138

libFileName = os.path.dirname(os.path.abspath(__file__)) + '/radiation.so'
LIB = cdll.LoadLibrary(libFileName)

class County(Structure):
	_fields_ = [('c', c_char), ('pop', c_int), ('lat', c_double), ('lng', c_double), ('valid', c_int)]

COUNTIES = None
VALID = None
DATA = None
ROW_NAMES = []
DATA_COL_NAMES = []

def setValid(*regions):
	global VALID
	VALID = []
	for region in regions:
		VALID += [line.strip() for line in open('regions/' + region)]

def loadCounties():
	global COUNTIES, ROW_NAMES, DATA_COL_NAMES
	
	inputData = sorted([line.strip().split(',') for line in open('counties')])

	CountyArray = County * N
	COUNTIES = CountyArray()
	for i in range(N):
		uid, pop, lat, lng = inputData[i]
		valid = 1 if not VALID or uid in VALID else 0
		ROW_NAMES.append(uid)
		if uid[0] == 'U':
			DATA_COL_NAMES.append(uid)
		COUNTIES[i] = County(uid[0], int(pop), float(lat), float(lng), valid)
	DATA_COL_NAMES += ['C', 'M']
	LIB.loadCounties.argtypes = [POINTER(CountyArray)]
	LIB.loadCounties.restype = None
	LIB.loadCounties(COUNTIES)

	print 'Counties loaded.'

def probability(parameters):
	gammaC, gammaM = parameters

	if COUNTIES is None:
		loadCounties()
	
	P = np.zeros(N * N).reshape((N, N))
	LIB.probability.argtypes = [ndpointer(np.float64, flags='C_CONTIGUOUS'), c_double, c_double]
	LIB.probability.restype = None
	LIB.probability(P, c_double(gammaC), c_double(gammaM))

	return P

def loadData():
	global DATA, ROW_NAMES, DATA_COL_NAMES
	
	if COUNTIES is None:
		loadCounties()
	
	inFile = [line.strip().split(',') for line in open('data')]
	commuters = {}
	for source, dest, n in inFile:
		if source == dest:
			continue
		n = int(n)
		if source not in commuters:
			commuters[source] = {}
		commuters[source][dest] = n
	
	DATA = np.zeros(N * N_DATA_COL).reshape((N, N_DATA_COL))
	for i in range(len(DATA)):
		for j in range(len(DATA[0])):
			row = ROW_NAMES[i]
			col = DATA_COL_NAMES[j]
			if row in commuters and col in commuters[row]:
				DATA[i][j] = commuters[row][col]
	
	print 'Data loaded.'

def flux(parameters):
	if DATA is None:
		loadData()
	
	include = [1.0 if not VALID or col in VALID else 0 for col in DATA_COL_NAMES]
	include[N_DATA_COL - 2] = 1.0 if 'C' in [x[0] for x in VALID] else 0
	include[N_DATA_COL - 1] = 1.0 if 'M' in [x[0] for x in VALID] else 0
	include = np.array(include)

	P = probability(parameters)
	F = np.zeros(N * N).reshape((N, N))

	LIB.flux.argtypes = [ndpointer(np.float64, flags='C_CONTIGUOUS'), 
									ndpointer(np.float64, flags='C_CONTIGUOUS'),
									ndpointer(np.float64, flags='C_CONTIGUOUS'),
									ndpointer(np.float64, flags='C_CONTIGUOUS')]
	LIB.flux.restype = None
	LIB.flux(F, DATA, include, P)

	return F

def logLikelihood(parameters):
	if DATA is None:
		loadData()
	print parameters
	P = probability(parameters)
	
	LIB.logLikelihood.argtypes = [ndpointer(np.float64, flags='C_CONTIGUOUS'), 
									ndpointer(np.float64, flags='C_CONTIGUOUS')]
	LIB.logLikelihood.restype = c_double
	
	return LIB.logLikelihood(DATA, P)

def maximumLikelihood():
	return minimize(logLikelihood, [0.5, 0.5], method='L-BFGS-B', bounds=[(1e-10, 1.0), (1e-10, 1.0)])

# setValid('us','mexico')
print maximumLikelihood()

