# last revision: 2015-06-10 22:42
# news_chosun.py



# -- coding: euc-kr  --
__author__ = 'Daddywhale'

import nltk, os
import urllib, sys
from nltk.corpus import wordnet as wn, brown, gutenberg, stopwords
from bs4 import BeautifulSoup
import re
reload(sys)
sys.setdefaultencoding('euc_kr')


def newsToken() :
    rtnDict = {}

    base_url = "http://english.chosun.com"
    start_url = "http://english.chosun.com/svc/hotissue_list.html?code=The%20Buzz&pn="
    to_visit_list=[]
    for i in range(5) :
        news_page = start_url + str(i)
        html = urllib.urlopen(news_page).read()
        soup = BeautifulSoup(html)
        headlines = soup.findAll("dt", { "class" : "arti_tit_2nd" })

        for headline in headlines :
            regexp = '''href=["'](.[^"']+)["']'''
            for e in re.findall(regexp, str(headline)) :
                to_visit_list.append(base_url + str(e))

    for s in to_visit_list :
        #print s
        html = urllib.urlopen(s).read()
        soup = BeautifulSoup(html)
        article = soup.findAll("div", { "class" : "article"})
        result_string = ""
        regexp = '''<p>(.+)</p>'''
        for e in re.findall(regexp, str(article)) :
            result_string += e

        result_string = re.sub(r'<br>', r'', result_string)
        result_token = result_string.split()
        rtnDict[s] = result_token
        #print result_token
    return rtnDict


NUMBER_TO_LOOK = 300
chosun_news = newsToken()

def addToList(L, e):
    if e not in L:
        L.append(e)

# Display for user input (no input will make the program behaves for all category)
stpwd = stopwords.words('english')

file_number = 0
if not os.path.exists('./_chosun'): os.mkdir('./_chosun')
for f in chosun_news:
    fn = str(file_number)
    file_net = open('./_chosun/net-' + fn + '.net', 'w')
    file_clu = open('./_chosun/net-' + fn + '.clu', 'w')
    file_inf = open('./_chosun/net-' + fn + '-info.txt', 'w')
    file_number += 1
    W = []      # Checked Word list
    V = []      # Node list
    E = []      # Edge list
    EforV = {}  # Edge list for each Node
    EforVn = {} # Number of Edges for each Node
    leafN = 0
    maxPath = 0

    for w in chosun_news[f]:
        if w.lower() not in stpwd and w not in W and w.isalpha():
            addToList(W, w)
            syns = wn.synsets(w)
            if syns != []:
                ws = syns[0] # use the first synset
                leafN += 1
                for path in ws.hypernym_paths():
                    if(len(path) > maxPath): maxPath = len(path)
                    addToList(V, path[0].name()) # adding first node
                    for i in range(1, len(path)):
                        addToList(V, path[i].name())
                        addToList(E, (V.index(path[i].name()), V.index(path[i-1].name())))
    
    file_net.write('*Vertices %d\n' % (len(V)))
    for index, word in enumerate(V):
        file_net.write('%d \"%s\"\n' % (index+1, word))
    file_net.write('*Arcs : 1 "SAMPLEK"\n')
    for v, w in E:
        file_net.write('%d %d\n' % (v+1, w+1))
    file_inf.write('#FILE:' + f + '\n')
    file_inf.write('#Vertices %d\n' % (len(V)))
    file_inf.write('#Arcs %d\n' % (len(E)))
    file_inf.write('#MaxPath %d\n' % (maxPath))
    file_inf.write('#LeafN %d\n' % (leafN))

    for v, w in E:
        if w not in EforV:
            EforV[w] = []
        if w not in EforVn:
            EforVn[w] = 0
        EforV[w].append(w)
        EforVn[w]+=1
    fd = nltk.FreqDist(EforVn)
    fdL = [w for w, c in fd.most_common(NUMBER_TO_LOOK)]

    file_inf.write('Rank\tCount\tSynset\n')
    for r, w in enumerate(fdL):
        file_inf.write('%d\t%d\t%s\n' % (r, fd[w], V[w]))

    file_clu.write('*Vertices %d\n' % (len(V)))
    for index, word in enumerate(V):
        file_clu.write('%d\n' % (3 if index in fdL[:20] else 1))
    
    print(fdL)
    print([V[w] for w in fdL])
    file_net.close()
    file_clu.close()
    file_inf.close()



