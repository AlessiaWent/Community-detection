#The program takes as input two cf-tables for two different subsets of the nodes (suggested size: 1M), computes the links between a node in the first subset and a node in the second subset, and creates an output file containing lines of the form vertex1-vertex2-weight for each such link
#Usage: ./edges_plates.py cftable1 nproc cftable2 output_file
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
    di2 = a[3]
    s = time.time()
    result = []
    for p in points_i:
        b = di[p.name]
        for q in points_j:
            c = di2[q.name]
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

#reads the tables containing ID_SOGGETTO and ID_CF for each node in the wanted subsets of the dataset
cfed = {}
cf = open(sys.argv[1], 'r')
for line in cf:
    line = line.strip().split(' ')
    cfed[line[0]] = line[1]
cf.close()

cfed2 = {}
cf = open(sys.argv[3], 'r')
for line in cf:
    line = line.strip().split(' ')
    cfed2[line[0]] = line[1]
cf.close()
print "reading all needed data" 

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
P = [Point(name, soggent, entpla) for name in cfed2.keys()]
t = len(P)
g = Graph()
g.add_vertices([cfed[p.name] for p in M])
g.add_vertices([cfed2[p.name] for p in P])
nproc = int(sys.argv[2])

s = time.time()
nsquares_i = 50
nsquares_j = 100
q = Queue()
processes_list = []

tot_proc = nsquares_i*nsquares_j

all_results = []

for i in range(nsquares_i):
    for j in range(nsquares_j):
        proc = Process(target=slice, args=[i, j, (M[10000*i:min(10000*(i+1),n)],P[10000*j:min(10000*(j+1),t)], cfed, cfed2),q])
        proc.start()
        print 'proc_num =', (i, j)
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

#writes links in output file
tab = open(sys.argv[4], 'w')
for r in all_results:
    for k in r:
        tab.write(k[0]+'\t'+k[1]+'\t'+str(k[2])+'\n')
tab.close()

print 'TT ='+str(time.time() - t_zero)
