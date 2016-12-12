#The program reads a file containing the edges and corresponding weights, performs DBSCAN and outputs Table 4
#Usage: ./label_prop.py cftable nproc edges_file output_file
import codecs
from igraph import *
import time
from point_ccred import Point, DBSCAN
import multiprocessing
from multiprocessing import Process
from Queue import Empty
from multiprocessing import Queue
from multiprocessing.managers import SyncManager
from functools import partial
import sys

#Computes the measures required for Table 4 for communities from beg to end
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

#reads the table containing ID_SOGGETTO and ID_CF for each node in the wanted subset of the dataset
cfed = {}
cfed_rev = {}
cf = open(sys.argv[1], 'r')
for line in cf:
    line = line.strip().split(' ')
    cfed[line[0]] = line[1]
    cfed_rev[line[1]] = line[0]
cf.close()

print "reading all needed data" 

edges = []
weights = []

edg = open(sys.argv[3], 'r')
for line in edg:
    k = line.strip().split('\t')
    edges.append((k[0], k[1]))
    weights.append(float(k[2]))    

print " complete reading dataset"
print 'initialization time  (including reading data ) =', time.time() - t_zero

print "start working in parallel"

n = len(cfed)
g = Graph()
g.add_vertices(cfed.values())
nproc = int(sys.argv[2])

s = time.time()

g.add_edges(edges)
g.es["weight"] = weights
g.simplify()
g.vs["group"] = None
g.vs["checked"] = None

print 'Time to copy edges =', time.time() - s

#DBSCAN with minPts = 15
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

f2 = Queue()

out = time.time()
other_results2 = []

for proc_num in range(nproc):
        beg = proc_num*step
        if proc_num < rem:
            beg += proc_num
        else:
            beg += rem
        end = beg + step
        if proc_num < rem:
            end += 1
        print beg, end
        proc = Process(target=writeslice2, args=[beg,end,g, f2])
        proc.start()
        print 'proc_num =', proc_num

while len(other_results2) < nproc:
    print len(other_results2), 'processes'
    other_results2.append(f2.get())

#writes results in output file
tab = open(sys.argv[4], 'w')
tab.write('ID_COMMUNITY,#NODES,#EDGES,AVG_#EDGES,MAX_DIST,CENTRALIZATION\n')
for r in other_results2:
    for k in r:
        tab.write(','.join(k))
        tab.write('\n')
tab.close()

print 'OT2 =', time.time() - out

print 'TT ='+str(time.time() - t_zero)
