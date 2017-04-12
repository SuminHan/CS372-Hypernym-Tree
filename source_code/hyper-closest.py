# last revision: 2015-06-10 21:30
# hyper-closest.py

import nltk, os
from nltk.corpus import wordnet as wn, brown, gutenberg, stopwords

NUMBER_TO_LOOK = 300

def dist(IL1, IL2):
	d = 0
	L1 = IL1[:NUMBER_TO_LOOK]
	L2 = IL2[:NUMBER_TO_LOOK]
	for e in L1:
		d += (L1.index(e) - L2.index(e))**2 if e in L2 else len(L2)**2
	return d

# Load Categories...
D = {}
Dcorrect = {}
for ctg in brown.categories():
	file_pop = open('category_'+ctg+'_popular.txt', 'r')
	popL = []
	for line in file_pop:
		c, s = line[:-1].split('\t')
		popL.append(s)
	D[ctg] = popL
	file_pop.close()

result_file = open('dist_result.txt', 'w')
correct_file = open('dist_correct.txt', 'w')
correct_file.write("NUMBER_TO_LOOK:%d\n"%(NUMBER_TO_LOOK))
for nctg in brown.categories():
	print(nctg)
	flist = brown.fileids(categories=nctg)
	number_of_files = 0
	number_of_correct = 0
	for f in flist:
		file_inf = open('./'+nctg+'/net-' + nctg + '-' + f + '-info.txt', 'r')
		number_of_files += 1
		fname = file_inf.readline()[len('#FILE:'):-1]
		vertex = int(file_inf.readline()[len('#Vertices '):-1])
		arcs = int(file_inf.readline()[len('#Arcs '):-1])
		maxpath = int(file_inf.readline()[len('#MaxPath '):-1])
		leafn = int(file_inf.readline()[len('#LeafN '):-1])
		rcs = file_inf.readline()

		DL = []
		#Rank, Count, Synset = file_inf[5]
		for line in file_inf:
			r, c, s = line[:-1].split('\t')
			DL.append(s)

		thatctg = ''
		thatdist = -1

		caldist = [(dist(D[actg], DL), actg) for actg in brown.categories()]
		caldist.sort()
		thatctg = caldist[0][1]
		print(nctg + '-' + f + '\t' + thatctg + '\t' + str(1 if nctg == thatctg else 0))
		number_of_correct += 1 if nctg == thatctg else 0
		result_file.write(nctg + '-' + f + '\t' + thatctg + '\t' + str(1 if nctg == thatctg else 0) + '\n')
	correct_file.write(nctg + '\t' + str(float(number_of_correct)*100/number_of_files) + '\n')
correct_file.close()
result_file.close()
