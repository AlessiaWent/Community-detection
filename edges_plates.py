#The program computes the plate links within a subset of the nodes (suggested size: 1M) and creates an output file containing lines of the form vertex1-vertex2-weight for each such link
#Usage: ./edges_plates.py cftable nproc output_file
import codecs
from igraph import *
import time
from point_plates import Point, DBSCAN
import multiprocessing
from multiprocessing import Process
from Queue import Empty
from multiprocessing import Queue
from multiprocessing.managers import SyncManager
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

#reads the table containing ID_SOGGETTO and ID_CF for each node in the wanted subset of the dataset
cfed = {}
cfed_rev = {}
cf = open(sys.argv[1], 'r')
for line in cf:
    line = line.strip().split(' ')
    cfed[line[0]] = line[1]
    cfed_rev[line[1]] = line[0]
cf.close()

#reads the data which is necessary to compute the plate links
soggent = {}
sogg = open('soggetti_an.csv', 'r')
for line in sogg:
    line = line.strip().split(',')
    soggent[line[0]] = []
sogg.close()

f2 = open('rolestable', 'r')
next(f2)
for line in f2:
    line = line.strip().split(' ')
    for a in line[1:]:
        soggent[a].append(line[0])
f2.close()

oggpla = {}
f3 = open('true_plates_table', 'r')
for line in f3:
    line = line.strip().split(' ')
    try:
        oggpla[line[0]].append(line[1])
    except KeyError:
        oggpla[line[0]] = line[1]
f3.close()

entpla = {}
f1 = open('link_pre_veicoli_an.csv')
next(f1)
for line in f1:
    line = line.strip().split(',')
    try:
        entpla[line[1]] = oggpla[line[0]]
    except KeyError:
        pass
f1.close()

print " complete reading dataset"
print 'initialization time  (including reading data ) =', time.time() - t_zero

print "start working in parallel"


M = [Point(name, soggent, entpla) for name in cfed.keys()]
n = len(M)
g = Graph()
g.add_vertices([cfed[p.name] for p in M])
nproc = int(sys.argv[2])

s = time.time()
nsquares = 100
q = Queue()
processes_list = []

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

tab = open(sys.argv[3], 'w')
for r in all_results:
    for k in r:
        tab.write(k[0]+'\t'+k[1]+'\t'+str(k[2])+'\n')
tab.close()

print 'TT ='+str(time.time() - t_zero)
