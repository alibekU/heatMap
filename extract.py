# drawing a heat map for given files

import matplotlib.pyplot as plt
import numpy as np

dir1 = "/mnt/synology/KAZ_ANNOVAR/merge.KAZ.1000G/fst_index"
dir2 = "/mnt/synology/KAZ_ANNOVAR/merge.KAZ.HGDP/fst_index"
file = "rog.rog.txt.out.mean.txt"
project1 = '1000G'
project2 = 'HGDP'

newNames1 = ['ASW', 'ACB', 'LWK', 'GWD', 'MSL', 'YRI', 'ESN', 'PEL', 'KHV', 'CHB', 'CHS', 'CDX', 'JPT', 'KAZ', 'MXL', 'PJL', 'GIH', 'BEB', 'STU', 'ITU', 'PUR', 'CLM', 'FIN', 'IBS', 'TSI', 'CEU', 'GBR']

def process(str):
	arr = str.rstrip('\n').split('\t')
	arr = arr[1:]
	return map(lambda x: float('nan') if x =='-' else float(x), arr)

def drawHeatMap(data,names,project):
	fig, ax = plt.subplots()
	cmp = plt.cm.Reds_r
	cmp.set_bad('w',1.)

	ax.set_xticks(np.arange(0,len(names)))
	ax.set_yticks(np.arange(0,len(names)))
	
	ax.invert_yaxis()	
	ax.xaxis.tick_top()
	ax.yaxis.tick_left()
	
	ax.set_xticklabels(names,minor=False)
	ax.set_yticklabels(names,minor=False)
	
	ax.set_frame_on(False)
	ax.grid(False)

	plt.xticks(rotation=90)
	
	for t in ax.xaxis.get_major_ticks():
		t.tick1On = False
		t.tick2On = False
	for t in ax.yaxis.get_major_ticks():
		t.tick1On = False
		t.tick2On = False

	fname = ''.join(['heatMap_', project, '.svg'])
	ax.imshow(data,interpolation='nearest',cmap=cmp)
	plt.savefig(fname, format = 'svg', dpi = 1200) 
	plt.close()

def getData(dir, file, newNames = []):
	input = '/'.join([dir, file])

	f = open(input)

	header = f.readline()
	names = header.rstrip('\n').split('\t')[1:]
	n = len(names)
	
	if len(newNames) == 0:
		data = []
		for line in f:
			data.append(process(line))
		newNames = names
		data = np.array(data)
	
	elif len(newNames) != len(names):
		raise Error("New order of labels does not match the one in the file %s." % input)
	
	else:
		data = np.zeros((n,n))
		# using dict to map old row and column according to the order in newNames
		dict = {}
		for i, name in enumerate(newNames):
			dict[name] = i
		
		# traversing the file line by line
		for i, line in enumerate(f):
			row = process(line)
			# since matrix is symmetric, we only need to read half of it
			# in this case, reading the upper triangle
			for j in range(i, n, 1):
				rowName = names[i]
				if i != j:
					columnName = names[j]
					# row is the i-th line
					data[dict[rowName], dict[columnName]] = row[j]
					# symmetry
					data[dict[columnName], dict[rowName]] = row[j]
				else:
					data[dict[rowName], dict[rowName]] = row[j]
	f.close()
	
	return {'data':data, 'names':newNames}

res = getData(dir1, file, newNames1)
drawHeatMap(res['data'], res['names'], project1)

res = getData(dir2, file)
drawHeatMap(res['data'], res['names'], project2)
