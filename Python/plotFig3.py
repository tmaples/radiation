import globals
import matplotlib.pyplot as plt
import numpy as np
import csv

path = globals.projectDirectory
countyFileName = path + 'usData/usDivisions.csv'
divisionFileName = path + 'canadaData/canadaDivisions.csv'
subdivisionFileName = path + 'canadaData/other/canadaSubdivisionPopulation.csv'

counties = [int(entry['population']) for entry in csv.DictReader(open(countyFileName))]
divisions = [int(entry['population']) for entry in csv.DictReader(open(divisionFileName))]
subdivisions = [int(line.strip().split(',')[-1]) for line in open(subdivisionFileName)]

plt.subplot('311')
plt.xlabel('Population')
plt.ylabel('Frequency')
plt.title('US counties')
plt.xscale('log')
plt.hist(counties, bins=np.logspace(0, 8, 75), color='gray')

plt.subplot('312')
plt.xlabel('Population')
plt.ylabel('Frequency')
plt.title('Canadian divisions')
plt.xscale('log')
plt.hist(divisions, bins=np.logspace(0, 8, 75), color='gray')

plt.subplot('313')
plt.xlabel('Population')
plt.ylabel('Frequency')
plt.title('Canadian subdivisions')
plt.xscale('log')
plt.hist(subdivisions, bins=np.logspace(0, 8, 75), color='gray')

plt.tight_layout()
plt.show()