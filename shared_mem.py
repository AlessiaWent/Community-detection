import codecs
from igraph import *
import time
import pp
from point_igr import Point
import math
import multiprocessing
from multiprocessing.managers import SyncManager
from functools import partial
import sys
#Igraph program with multiprocessing library
#Usage: python shared_mem.py cftable nproc

def SManager():
    m = SyncManager()
    m.start()
    return m

def slice(i,a):
    points = a[0]
    dict = a[1]
    nproc = a[2]
    n = len(points)
    s = time.time()
    beg = int(math.sqrt(i)*n/math.sqrt(nproc))
    end = int(math.sqrt(i+1)*n/math.sqrt(nproc))
    result = []
    for i in range(beg, end):
        p = points[i]
	b = dict[p.name]
        for j in range(i):
            q = points[j]
	    c = dict[q.name]
            if p.link(q) != None:
		l = p.link(q)
                result.append([b, c, l])
    print beg, time.time() - s
    return result


if len(sys.argv) <2:
    print 'please provide me input file' 
    sys.exit()

if len(sys.argv) <3:
    print 'please provide me number of processors'
    sys.exit()

cfed = {}
cf = open(sys.argv[1], 'r')
for line in cf:
    line = line.strip().split(' ')
    cfed[line[0]] = int(line[1])
cf.close()
t = time.time()

print "reading all needed data" 

entci = {}
f1 = open('preventivi_filtered.csv')
for line in f1:
    line = line.strip().split(',')
    entci[line[0]] = line[7]
f1.close()

soggent = {}
sogg = open('soggetti_an.csv', 'r')
for line in sogg:
    line = line.strip().split(',')
    soggent[line[0]] = []
sogg.close()

f2 = open('rolestable_filtered', 'r')
next(f2)
for line in f2:
    line = line.strip().split(' ')
    for a in line[1:]:
        soggent[a].append(line[0])
f2.close()

print "start working in parallel"

sm = SManager()

M = sm.list([Point(name, soggent, entci) for name in cfed.keys()])
n = len(M)
g = Graph(7626691)
nproc = int(sys.argv[2])

s = time.time()
pool = multiprocessing.Pool(processes = nproc)
result = pool.map(partial(slice,a = (M,cfed,nproc)),range(nproc))

edges = []
weights = []
for j in result:
    for k in j:
        edges.append((k[0], k[1]))
        weights.append(k[2])
g.add_edges(edges)
g.es["weight"] = weights

print 'PT (including copying results) =', time.time() - s

comm = g.community_label_propagation(weights = g.es["weight"])
print '#clusters with more than 1 element: ', len([i for i in comm if len(i) > 1])

print 'TT =', time.time() - t
