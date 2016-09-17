import time
#from pathos.threading import ThreadPool
import pp
import sys
import collections
from idkscaling import Point, DBSCAN

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
cf = open('cftable_filtered', 'r')
for line in cf:
    line = line.strip().split(' ')
    cfed.append(line[0])
cf.close()
M = [Point(name, soggent, entci) for name in cfed]
#mat = open('prova_matrix', 'w')
#for i in range(len(M)):
#	mat.write(' '.join([str(M[i].distance(M[j])) for j in range(i+1, len(M)) if M[i].distance(M[j]) != None]))
#mat.close()
s = time.time()
C = DBSCAN(1.0, 7, M, job_server)
print 'PT =', time.time() - s
print C.npoints
#inputs = ()
#results = []
#step = C.npoints/ncpus
#rest = C.npoints%ncpus
#for index in xrange(ncpus):
#    start = index * step
#    if index < rest:
#	start += index
#    else:
#	start += rest
#    end = start + step
#    if index < rest:
#	end += 1
#    inputs = inputs + ((start, end),)  
#jobs = [(inp, job_server.submit(C.setNeighs, (inp,),(), ('time',))) for inp in inputs]
#job_server.wait()
#for inp, job in jobs:
#    pippo = job()
#    results = results + pippo
#for l in results:
#    C.points[l[0]].neigh = l[1]
#for start, end in inputs:
#    print start, end, [i.name for i in M[start:end] if i.neigh != []]
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
#for i in range(len(C.clusters)):
#	for j in range(i):
#		if len([p for p in C.clusters[i] if p in C.clusters[j]]) > 0:
#			print [p for p in C.clusters[i] if p in C.clusters[j]], C.clusters[i], i, j
#	print [item for item, count in collections.Counter(C.clusters[i]).items() if count > 1]
#print [i.name for i in C.clusters[3729]]
#print C.clusters[3729][0].ci, C.clusters[3729][0].ent, C.clusters[3729][0].neigh
#c = C.clusters[0]
#print len(c), [i.name for i in c]
#for p in c:
#    print [i.name for i in p.neigh], len(p.neigh), [a for a in C.clusters[0][0].ci if a in p.ci], p.distance(C.clusters[0][0]), C.clusters[0][0] in p.neigh
#for i in range(len(C.clusters)):
#    print 'Cluster', i, 'is:', ' '.join([j.name for j in C.clusters[i]])
print 'TT =', time.time() - t
#PBS -q blade
job_server.print_stats()
