import codecs
from igraph import *
import time
from point_igr import Point, DBSCAN
import math
import multiprocessing
from multiprocessing import Process
from Queue import Empty
from multiprocessing import Queue
from multiprocessing.managers import SyncManager
from functools import partial
import sys
import logging

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

def writeslice1(beg,end,g,cfed_rev,que):
    result = []
    subs = [g.induced_subgraph([v for v in g.vs() if v["group"] == k]) for k in range(beg,end)]
    for ind in range(beg,end):
        sub = subs[ind-beg]
        evcent = sub.evcent()
        prank = sub.pagerank()
        closeness = sub.closeness()
        betweenness = sub.betweenness()
        for v in sub.vs():
            deg = sub.degree(v)
            i = v["name"]
            result.append(cfed_rev[i]+","+i+","+str(ind)+","+str(deg)+","+str(deg/float(sub.vcount()))+","+str(closeness[sub.vs.find(i).index])+","+str(betweenness[sub.vs.find(i).index])+','+str(evcent[v.index])+','+str(prank[v.index])+"\n")
    que.put(result)

def writeslice2(beg,end,g,que):
    result = []
    subs = [g.induced_subgraph([v for v in g.vs() if v["group"] == k]) for k in range(beg,end)]
    for i in range(beg,end):
        sub = subs[i-beg]
        nnodes = len(sub.vs())
        if nnodes > 1:
            shortest = sub.shortest_paths()
            degs = sub.degree()
            degmax = max(degs)
            nedges = len(sub.es())
            if nnodes > 2:
                centr = sum([degmax - x for x in degs])/float((nnodes - 1)*(nnodes - 2))
            else:
                centr = 0
            result.append([str(i),str(nnodes),str(nedges),str(2*nedges/float(nnodes)),str(max(max(shortest))),str(centr)])
    que.put(result)

if len(sys.argv) <2:
    print 'please provide me input file' 
    sys.exit()

if len(sys.argv) <3:
    print 'please provide me number of processors'
    sys.exit()


t_zero = time.time()

cfed = {}
cfed_rev = {}
cf = open(sys.argv[1], 'r')
for line in cf:
    line = line.strip().split(' ')
    cfed[line[0]] = line[1]
    cfed_rev[line[1]] = line[0]
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
g = Graph()
g.add_vertices([cfed[p.name] for p in M])
nproc = int(sys.argv[2])

s = time.time()
nsquares = 100
q = Queue()
processes_list = []

edges = []
weights = []
tot_proc = nsquares*(nsquares+1)/2

all_results = []

for proc_num in range(nsquares*(nsquares+1)/2):
	i, j = indices(proc_num,nsquares)
        proc = Process(target=slice, args=[i, j, (M[10000*i:min(10000*(i+1),n)],M[10000*j:min(10000*(j+1),n)], cfed, nproc),q])
        proc.start()
	print 'proc_num =', proc_num
        processes_list.append(proc)
        while len(processes_list) >= nproc:
            time.sleep(1)
            try:
                while True:
                    all_results.append(q.get(block = False))
            except Empty:
		print 'coda vuota'
                pass
            processes_list = [p for p in processes_list if p.is_alive()]
            print '#processi =', len(processes_list)

while len(all_results)< tot_proc:
    print len(all_results), ' processes'
    all_results.append(q.get())

for r in all_results:
    for k in r:
	edges.append((k[0], k[1]))
        weights.append(k[2])

[p.join() for p in processes_list]

g.add_edges(edges)
g.es["weight"] = weights
g.simplify()
g.vs["group"] = None
g.vs["checked"] = None

print 'PT (including copying results) =', time.time() - s
C = DBSCAN(0.5,15,g)
for p in C.graph.vs():
    if p["group"] != None:
        continue
    if len(g.neighbors(p.index)) < C.minPts:
        continue
    C.createCluster(p)
    C.expandCluster(C.clusters[-1])

print 'Number of clusters:', len(C.clusters), 'Number of points in clusters:', sum(len(C.clusters[i]) for i in range(len(C.clusters)))
print '\n'

f = Queue()

out = time.time()
other_results = []

nclu = max(g.vs["group"]) + 1
step = nclu/nproc
if nclu%nproc > 0:
    step += 1

for proc_num in range(nproc):
        beg = proc_num*step
        end = min((proc_num+1)*step,nclu)
	proc = Process(target=writeslice1, args=[beg,end,g, cfed_rev, f])
        proc.start()
        print 'proc_num ='+str(proc_num)

while len(other_results)< nproc:
    print str(len(other_results))+'processes'
    other_results.append(f.get())

'scrivo tutto'

tab = open('table_1_db_complete', 'w')
tab.write('ID_SOGGETTO,ID_CF,ID_COMMUNITY,DEGREE,NORM_DEGREE,CLOSENESS,BETWEENNESS,EIG_CENTRALITY,PAGERANK\n')
for r in other_results:
    for k in r:
        tab.write(k)
tab.close()

print 'OT ='+str(time.time() - out)
f2 = Queue()

out = time.time()
other_results2 = []

for proc_num in range(nproc):
        beg = proc_num*step
        end = min((proc_num+1)*step,nclu)
        proc = Process(target=writeslice2, args=[beg,end,g, f2])
        proc.start()
        print 'proc_num =', proc_num

while len(other_results2) < nproc:
    print len(other_results2), 'processes'
    other_results2.append(f2.get())

tab = open('table_4_db_complete', 'w')
tab.write('ID_COMMUNITY,#NODES,#EDGES,AVG_#EDGES,MAX_DIST,CENTRALIZATION\n')
for r in other_results2:
    for k in r:
        tab.write(','.join(k))
        tab.write('\n')
tab.close()

print 'OT2 =', time.time() - out

print 'TT ='+str(time.time() - t_zero)
