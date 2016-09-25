import codecs
from igraph import *
import time
import pp
from point_igr import Point
import math
import sys

def slice(points, beg, end, cfed):
    s = time.time()
    result = []
    for i in range(beg, end):
        p = points[i]
	row = []
        for j in range(i):
            q = points[j]
	    c = cfed[q.name]
            if p.link(q) != None:
		l = p.link(q)
                row.append([c, l])
	result.append(row)
    print beg, time.time() - s
    return result



t = time.time()
ppservers = ()
if len(sys.argv) > 1:
    ncpus = int(sys.argv[1])
    # Creates jobserver with ncpus workers
    job_server = pp.Server(ncpus, ppservers=ppservers)
else:
    # Creates jobserver with automatically detected number of workers
    job_server = pp.Server(ppservers=ppservers)

print "Starting pp with", job_server.get_ncpus(), "workers"

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

cfed = {}
cf = open(sys.argv[2], 'r')
for line in cf:
    line = line.strip().split(' ')
    cfed[line[0]] = line[1]
cf.close()

M = [Point(name, soggent, entci) for name in cfed.keys()]
n = len(M)
g = Graph()
g.add_vertices([cfed[p.name] for p in M])
m = job_server.get_ncpus()

s = time.time()
jobs = [job_server.submit(slice,(M,int(math.sqrt(i)*n/math.sqrt(m)),int(math.sqrt(i+1)*n/math.sqrt(m)),cfed),(),('time','math')) for i in range(m)]

edges = []
weights = []
i = 0
for job in jobs:
    result = job()
    for j in range(len(result)):
        c = cfed[M[i+j].name]
        for k in result[j]:
            edges.append((c, k[0]))
	    weights.append(k[1])
    i = i + len(result)
g.add_edges(edges)
g.es["weight"] = weights

print 'PT (including copying results) =', time.time() - s

comm = g.community_label_propagation(weights = g.es["weight"])
print '#clusters with more than 1 element: ', len([i for i in comm if len(i) > 1])
g.vs["group"] = comm.membership

print '\n'
shortest = g.shortest_paths()

tab = open('table_3', 'w') 
for i in cfed.keys():
    shortest = g.shortest_paths(source = g.vs.find(cfed[i]).index)
    tab.write(str(shortest[0])+"\n")
tab.close()
print 'TT =', time.time() - t
job_server.print_stats()
