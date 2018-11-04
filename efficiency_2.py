import sys
import argparse
import os.path
from os import path
import matplotlib
import matplotlib.pyplot as plot
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import math

#Make tables of data for each source

def get_parser():
	parser = argparse.ArgumentParser(description='efficiency plot from fitted disc source data')
	parser.add_argument('input', metavar='FILE', help='.dat file generated from ge_spec_3.py')
	parser.add_argument('title', help = 'title the plot')
	parser.add_argument('output', help = 'output pdf plot of efficiency')

	return parser

def get_args(parser):
	args = parser.parse_args()
	return args
def efficiency(a,t,i,n):
	e = n/(a*t*i)
	return e
def err_A(A):
	activity_error = 0.05*A
	return activity_error
def err_e(A, t, I, err_N, N, err_A):
	er1 = err_N/(A*t*I)
	er2 = N*err_A/((A**2)*t*I)
	error_e = math.sqrt(er1**2 + er2**2)
	return error_e
args = get_args(get_parser())
file = open(args.input, 'r')
i = 0
data = [[]]
for line in file.readlines():
	i +=1
	if i==1:
		continue
	line = line.split(' ')
	#print(data[(i-1)])
	data[i-2].append(line[0])
	data[i-2].append(float(line[3]))
	data[i-2].append(float(line[11]))
	data[i-2].append(float(line[16]))
	data.append([])

file.close()

#edit "data" table to reflect branching ratio and livetime (hard coded because these are looked up)

Branching_ratios = [0.00638, 0.00453, 0.0214, 0.851, 0.0364, 0.9998, 0.9985, 0.1068, 0.994, 0.9998] #in order of entries in file test_2.dat

Live_times = [69, 216, 147, 45, 49, 16, 34] #in seconds, in order of Ba, Cs, Cd, Co60, Co57, Na, Mn from files in this directory dated august through september in seconds

Activities = [40700, 19314, 39220, 37000, 39960, 49580, 50690] #same order as above in Bq

#assemble data in form: [isotope name, peak E, n counts in peak,branching ratio I,  A activity, T live time]

#Add activity data from table of activities:
for i in range(10):
	data[i].append(Branching_ratios[i])
	if i<3:
		data[i].append(Activities[0])
		data[i].append(err_A(Activities[0]))
		data[i].append(Live_times[0])
		continue
	if i<4:
		data[i].append(Activities[1])
		data[i].append(err_A(Activities[1]))
		data[i].append(Live_times[1])
		continue
	if i<5:
		data[i].append(Activities[2])
		data[i].append(err_A(Activities[2]))
		data[i].append(Live_times[2])
		continue
	if i<7: 
		data[i].append(Activities[3])
		data[i].append(err_A(Activities[3]))
		data[i].append(Live_times[3])
		continue
	if i<8: 
		data[i].append(Activities[4])
		data[i].append(err_A(Activities[4]))
		data[i].append(Live_times[4])
		continue
	if i<9: 
		data[i].append(Activities[5])
		data[i].append(err_A(Activities[5]))
		data[i].append(Live_times[5])
		continue
	if i<10: 
		data[i].append(Activities[6])
		data[i].append(err_A(Activities[6]))
		data[i].append(Live_times[6])
		continue

for i in range(10):
	print(data[i])
#calculate efficiencies
efficiencies = [[],[], []]
for i in range(10):
	a = float(data[i][5])
	a_er = float(data[i][6])
	t = float(data[i][7])
	j = float(data[i][4])
	n = float(data[i][2])
	n_er = float(data[i][3])
	e = efficiency(a,t,j,n)
	e_error = err_e(a,t,j,n_er, n, a_er)
	efficiencies[0].append(float(data[i][1]))
	efficiencies[1].append(e)
	efficiencies[2].append(e_error)

print(efficiencies)
plot.plot(efficiencies[0], efficiencies[1], 'ro', markersize=4.0)
plot.errorbar(efficiencies[0], efficiencies[1], yerr = efficiencies[2], elinewidth=2.0, capsize=4.0, ls='none')
plot.xlabel('E (keV)', fontsize=14)
plot.ylabel('efficiency', fontsize=14)
plot.title(args.title, fontsize=18)
output = PdfPages(args.output)
output.savefig(transparent=True)
plot.close()
output.close()

f = open('all_data_and_errors.dat', 'w')
f.write('Isotope''       ''Peak (keV)''      ''Area (n)''           ' 'Area (n) error''       ''Branching ratio I''       ' 'Livetime t''      ''Activity''     ' 'Activity error''    ''Efficiency''            ''Efficiency error')
f.write('\n')
for i in range(10):
	f.write('\n')
	f.write(str(data[i][0]))
	f.write('        ')
	f.write(str(data[i][1]))
	f.write('   ')
	f.write(str(data[i][2]))
	f.write('      ')
	f.write(str(data[i][3]))
	f.write('              ')
	f.write(str(data[i][4]))
	f.write('               ')
	f.write(str(data[i][7]))
	f.write('          ')
	f.write(str(data[i][5]))
	f.write('         ')
	f.write(str(data[i][6]))
	f.write('         ')
	f.write(str(efficiencies[1][i]))
	f.write('          ')
	f.write(str(efficiencies[2][i]))
	f.write('\n')

f.close()
