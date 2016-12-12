#The program reads a file containing the edges and corresponding weights, performs label propagation and outputs Table 1
#Usage: ./label_prop.py cftable nproc edges_file output_file
import codecs
from igraph import *
import time
from point_mix import Point
import random
import multiprocessing
from multiprocessing import Process
from Queue import Empty
from multiprocessing import Queue
from multiprocessing.managers import SyncManager
from functools import partial
import sys
import logging

#Computes the measures required for Table 1 for communities from beg to end
def writeslice1(beg,end,g,cfed_rev,que):
    result = []
    subs = [g.induced_subgraph([v for v in g.vs() if v["group"] == k-1]) for k in range(beg,end)]
    for ind in range(beg,end):
        sub = subs[ind-beg]
	if sub.vcount() > 1:
            evcent = sub.evcent()
            prank = sub.pagerank()
            closeness = sub.closeness()
            betweenness = sub.betweenness()
            for v in sub.vs():
                deg = sub.degree(v)
                i = v["name"]
                result.append(cfed_rev[i]+","+i+","+str(ind-1)+","+str(deg)+","+str(deg/float(sub.vcount()))+","+str(closeness[sub.vs.find(i).index])+","+str(betweenness[sub.vs.find(i).index])+','+str(evcent[v.index])+','+str(prank[v.index])+"\n")
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

print " complete reading dataset"
print 'initialization time  (including reading data ) =', time.time() - t_zero

g = Graph()
g.add_vertices(cfed.values())
nproc = int(sys.argv[2])

n = len(cfed)
edges = []
weights = []

s = time.time()

edg = open(sys.argv[3], 'r')
for line in edg:
    k = line.strip().split('\t')
    edges.append((k[0], k[1]))

g.add_edges(edges)
g.simplify()
to_remove = g.vs.select(_degree = 0)
g.delete_vertices(to_remove)
g.es["weight"] = weights

print 'Time to copy edges =', time.time() - s
random.seed(1234)
comm = g.community_label_propagation(weights = g.es["weight"])
g.vs["group"] = comm.membership
print '#clusters with more than 1 element: ', len([i for i in comm if len(i) > 1])

print '\n'

f = Queue()

out = time.time()
other_results = []

nclu = max(comm.membership) + 2
step = nclu/nproc
if nclu%nproc > 0:
    step += 1

for proc_num in range(nproc):
        beg = proc_num*step
        end = min((proc_num+1)*step,nclu-1)
	proc = Process(target=writeslice1, args=[beg,end,g, cfed_rev,f])
        proc.start()
        print 'proc_num ='+str(proc_num)

while len(other_results)< nproc:
    print str(len(other_results))+'processes'
    other_results.append(f.get())

#writes results in output file
tab = open(sys.argv[4], 'w')
tab.write('ID_SOGGETTO,ID_CF,ID_COMMUNITY,DEGREE,NORM_DEGREE,CLOSENESS,BETWEENNESS,EIG_CENTRALITY,PAGERANK\n')
for r in other_results:
    for k in r:
        tab.write(k)
tab.close()

print 'OT ='+str(time.time() - out)

print 'TT ='+str(time.time() - t_zero)
