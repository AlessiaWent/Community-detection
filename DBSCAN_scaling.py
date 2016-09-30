import time
import pp
import sys
import collections
from idkscaling import Point, DBSCAN
#DBSCAN program
#Usage: python DBSCAN_scaling.py nproc cftable

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
	try:
            soggent[a].append(line[0])
	except KeyError:
	    pass
f2.close()

cfed = []
cf = open(sys.argv[2], 'r')
for line in cf:
    line = line.strip().split(' ')
    cfed.append(line[0])
cf.close()
M = [Point(name, soggent, entci) for name in cfed]

s = time.time()
#Parallel part is included in initialization of DBSCAN object, see idkscaling.py
C = DBSCAN(1.0, 7, M, job_server)
print 'PT =', time.time() - s

print C.npoints

print sum(1 for i in range(C.npoints) if len(C.points[i].neigh) >= C.minPts)

print sum(1+len(C.points[i].neigh) for i in range(C.npoints) if len(C.points[i].neigh) >= C.minPts)

for p in C.points:
    if p.visited:
        continue
    if len(p.neigh) < C.minPts:
        continue
    C.createCluster(p)
    C.expandCluster(C.clusters[-1])
print 'Number of clusters:', len(C.clusters), 'Number of points in clusters:', sum(len(C.clusters[i]) for i in range(len(C.clusters)))

print 'TT =', time.time() - t
job_server.print_stats()
