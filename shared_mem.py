import codecs
from igraph import *
import time
from point_igr import Point
import math
import multiprocessing
from multiprocessing import Process
from Queue import Empty
from multiprocessing import Queue
from functools import partial
import sys

def indices(i,k):
    j = 0
    while i >= k:
	i -= k
	k -= 1
	j += 1
    return (i+j,j)

def slice(i,j,a,que):
    points_i = a[0]
    points_j = a[1]
    di = a[2]
    nproc = a[3]
    my_proc=i
    s = time.time()
    result = []
    for p in points_i:
	b = di[p.name]
        for q in points_j:
	    c = di[q.name]
	    if p.link(q) != None and c != b:
		l = p.link(q)
                result.append([b, c, l])
    que.put(result)


if len(sys.argv) <2:
    print 'please provide me input file' 
    sys.exit()

if len(sys.argv) <3:
    print 'please provide me number of processors'
    sys.exit()


t_zero = time.time()

cfed = {}
cf = open(sys.argv[1], 'r')
for line in cf:
    line = line.strip().split(' ')
    cfed[line[0]] = int(line[1])
cf.close()

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

print " complete reading dataset"
print 'initialization time  (including reading data ) =', time.time() - t_zero

print "start working in parallel"


M = [Point(name, soggent, entci) for name in cfed.keys()]
n = len(M)
g = Graph(7626691)
nproc = int(sys.argv[2])

s = time.time()
nsquares = n/10000
#nsquares = 10
q = Queue()
processes_list = []

edges = []
weights = []
tot_proc = nsquares*(nsquares+1)/2

all_results = []

for proc_num in range(nsquares*(nsquares+1)/2):
	i, j = indices(proc_num,nsquares)
        proc = Process(target=slice, args=[i, j, (M[n/nsquares*i:n/nsquares*(i+1)],M[n/nsquares*j:n/nsquares*(j+1)], cfed, nproc),q])
        proc.start()
	print 'proc_num =', proc_num
        processes_list.append(proc)
        while len(processes_list) >= nproc:
            time.sleep(1)
            try:
                while True:
                    all_results.append(q.get(block = False))
            except Empty:
                pass
            processes_list = [p for p in processes_list if p.is_alive()]

while len(all_results)< tot_proc:
    all_results.append(q.get())

for r in all_results:
    for k in r:
	edges.append((k[0], k[1]))
        weights.append(k[2])

[p.join() for p in processes_list]

g.add_edges(edges)
g.es["weight"] = weights

print 'PT (including copying results) =', time.time() - s
comm = g.community_label_propagation(weights = g.es["weight"])
print '#clusters with more than 1 element: ', len([i for i in comm if len(i) > 1])

print 'TT =', time.time() - t_zero
