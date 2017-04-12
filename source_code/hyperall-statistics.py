# last revision: 2015-06-10 21:17
# hyperall-statistics.py
# Creates statistic file.
# Computes average #files, #leaves, #maxpaths, #V, #E.
# Computes the overall popular synsets for each category.

import sys, nltk
from collections import defaultdict
from nltk.corpus import brown, gutenberg, stopwords

NUMBER_TO_LOOK = 300
output = open('category_statistics.txt', 'w')
output.write('%s\t%s\t%s\t%s\t%s\t%s\n' % ('category', '#files', 'leaves', 'maxpaths', 'V', 'E'))
for ctg in brown.categories():
	flist = brown.fileids(categories=ctg)
	number_of_files = 0
	totv = 0
	tote = 0
	totp = 0
	totl = 0
	D = defaultdict(int)
	for f in flist:
		file_inf = open('./'+ctg+'/net-' + ctg + '-' + f + '-info.txt', 'r')
		number_of_files += 1
		fname = file_inf.readline()[len('#FILE:'):-1]
		vertex = int(file_inf.readline()[len('#Vertices '):-1])
		arcs = int(file_inf.readline()[len('#Arcs '):-1])
		maxpath = int(file_inf.readline()[len('#MaxPath '):-1])
		leafn = int(file_inf.readline()[len('#LeafN '):-1])
		#Rank, Count, Synset = file_inf[5]
		rcs = file_inf.readline()

		totv += vertex
		tote += arcs
		totp += maxpath
		totl += leafn
		for line in file_inf:
			r, c, s = line[:-1].split('\t')
			D[s] += int(c)

	output.write('%s\t%d\t%f\t%f\t%f\t%f\t\n' % 
					(ctg, 
					number_of_files, 
					float(totl)/number_of_files, 
					float(totp)/number_of_files, 
					float(totv)/number_of_files, 
					float(tote)/number_of_files))
	
	pop = open('category_'+ctg+'_popular.txt', 'w')
	for s, c in nltk.FreqDist(D).most_common(NUMBER_TO_LOOK):
		pop.write('%d\t%s\n' %(c, s))
	pop.close()
output.close()
