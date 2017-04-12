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
for ctg in brown.categories():
	file_pop = open('category_'+ctg+'_popular.txt', 'r')
	popL = []
	for line in file_pop:
		c, s = line[:-1].split('\t')
		popL.append(s)
	D[ctg] = popL
	file_pop.close()

result_file = open('news_closest_reuters.txt', 'w')


fn = 0
file_name = './_reuters/net-' + str(fn) + '-info.txt'
while os.path.isfile(file_name):
	file_inf = open(file_name, 'r')

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

	caldist = [(dist(D[actg], DL), actg) for actg in brown.categories()]
	caldist.sort()
	print(fname + '\t' + caldist[0][1] + '\t' + caldist[1][1] + '\t' + caldist[2][1])
	result_file.write(fname + '\t' + caldist[0][1] + '\t' + caldist[1][1] + '\t' + caldist[2][1] + '\n')

	#for next loop
	fn += 1
	file_name = './_reuters/net-' + str(fn) + '-info.txt'
result_file.close()
