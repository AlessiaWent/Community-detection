import codecs
from igraph import *
import time
import pp
from point_igr import Point
import math
import multiprocessing
from multiprocessing.managers import SyncManager
from functools import partial

def SManager():
    m = SyncManager()
    m.start()
    return m

def slice(i,a):
    points = a[0]
    dict = a[1]
    n = len(points)
    s = time.time()
    beg = int(math.sqrt(i)*n/8)
    end = int(math.sqrt(i+1)*n/8)
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



t = time.time()
#ppservers = ()
#if len(sys.argv) > 1:
#    ncpus = int(sys.argv[1])
    # Creates jobserver with ncpus workers
#    job_server = pp.Server(ncpus, ppservers=ppservers)
#else:
    # Creates jobserver with automatically detected number of workers
#    job_server = pp.Server(ppservers=ppservers)

#print "Starting pp with", job_server.get_ncpus(), "workers"

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
cf = open('cftable_3small', 'r')
for line in cf:
    line = line.strip().split(' ')
    cfed[line[0]] = int(line[1])
cf.close()
#BaseManager.register("Point", Point)
print 'registration'
sm = SManager()
print 'mg'
M = sm.list([Point(name, soggent, entci) for name in cfed.keys()])
print 'M processed'
n = len(M)
print n
g = Graph(7626691)
#m = job_server.get_ncpus()
s = time.time()
#jobs = [job_server.submit(slice,(M,int(math.sqrt(i)*n/math.sqrt(m)),int(math.sqrt(i+1)*n/math.sqrt(m)),cfed),(),('time','math')) for i in range(m)]
pool = multiprocessing.Pool(processes = 64)
result = pool.map(partial(slice,a = (M,cfed)),range(64))
print result, len(result)
edges = []
weights = []
i = 0
#for job in jobs:
#    result = job()
for j in result:
    for k in j:
        edges.append((k[0], k[1]))
        weights.append(k[2])
    #i = i + len(result)
g.add_edges(edges)
g.es["weight"] = weights
print 'PT (including copying results) =', time.time() - s
#for i in range(len(M)):
#    p = M[i]
#    for j in range(i):
#	q = M[j]
#	if p.link(q) != None:
#	    g.add_edge(cfed[p.name], cfed[q.name], weight = p.link(q))
comm = g.community_label_propagation(weights = g.es["weight"])
print '#clusters with more than 1 element: ', len([i for i in comm if len(i) > 1])
#for i in comm:
#    if len(i) > 1:
#	print i

print 'TT =', time.time() - t
#job_server.print_stats()
