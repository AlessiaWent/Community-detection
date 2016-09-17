import pp
import time

class Point(object):
    def __init__(self, name, rolesdict, entdict):
        self.visited = False
        self.checked = False
        self.name = name
        self.neigh = []
	self.ent = []
        try:
	    self.ent = rolesdict[self.name]
	except KeyError:
	    pass
	self.ci = []
	for e in self.ent:
	    try:
		if entdict[e] != '':
		    self.ci.append(entdict[e])
	    except KeyError:
		pass
    def distance(self, other):
        if len([a for a in self.ci if a in other.ci]) or len([a for a in self.ent if a in other.ent]):
            return 0.001
    def __str__(self):
        return str(self.name)

def slice(self, beg, end):
    t = time.time()
    result = []
    for j in range(beg,end):
        row = []
        for k in range(self.npoints):
            if j!= k and self.points[j].distance(self.points[k]) != None and self.points[j].distance(self.points[k]) < self.epsilon:
               row.append(k)
        result.append(row)
    print beg, time.time() - t
    return result

class DBSCAN(object):
    def __init__(self, epsilon, minPts, M, server):
        self.epsilon = epsilon
        self.minPts = minPts
        self.points = M
        self.npoints = len(M)
        self.clusters = []
        step = self.npoints/server.get_ncpus()+1
	t = time.time()
	jobs = [server.submit(slice,(self,i,min(i+step, self.npoints)), (),('time',)) for i in range(0, self.npoints, step)]
        print 'jobs time =', time.time()-t
	i = 0
        for job in jobs:
           result = [[self.points[k] for k in ks] for ks in job()]
           for j in range(len(result)):
                self.points[i + j].neigh = result[j]
           i = i + len(result) 
    def createCluster(self, p):
        self.clusters.append([p])
        p.visited = True
    def expandCluster(self, c):
        for p in c:
            if p.checked:
                continue
            if len(p.neigh) >= self.minPts:
                for q in p.neigh:
                    if q.visited == False:
                        q.visited = True
                        c.append(q)
            p.checked = True
