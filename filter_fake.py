#The program takes as input the plates table and creates a new table where the lines corresponding to fake plate numbers are removed, in order to create the plate links correctly.
#Usage: ./filter_fake.py plates_table nproc
from igraph import *
import time
import multiprocessing
from multiprocessing import Process
from Queue import Empty
from multiprocessing import Queue
from multiprocessing.managers import SyncManager
from functools import partial
import sys

if len(sys.argv) <2:
    print 'please provide me input file' 
    sys.exit()

if len(sys.argv) <3:
    print 'please provide me number of processors'
    sys.exit()

def filter(fake, slice, que):
    result = []
    for i in slice:
        if i[1] not in fake:
            result.append(i)
    que.put(result)

t_zero = time.time()

plates = []
cf = open(sys.argv[1], 'r')
for line in cf:
    line = line.strip().split(' ')
    plates.append(line)
cf.close()

n = len(plates)
print "reading all plates" 

fake = []
fakes = open('targhe_false_sissa_an.csv', 'r')
next(fakes)
for line in fakes:
    line = line.strip().split(',')
    fake.append(line[1])
fakes.close()

print "reading all fakes", len(fake)
print "start working in parallel"

nproc = int(sys.argv[2])

s = time.time()
tot_proc = 1000
q = Queue()
processes_list = []

all_results = []
step = n/tot_proc
if n%nproc > 0:
    step += 1

for proc_num in range(tot_proc):
        beg = proc_num*step
        end = min((proc_num+1)*step,n-1)
        proc = Process(target=filter, args=[fake,plates[beg:end],q])
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

tab = open('true_plates_table', 'w')
for r in all_results:
    for k in r:
        tab.write(k[0]+' '+k[1]+'\n')
tab.close()

[p.join() for p in processes_list]
print 'TT ='+str(time.time() - t_zero)
