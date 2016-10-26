#File containing the definitions of the needed classes. The Point class is defined in order to deal with the credit card links

class Point(object):
    def __init__(self, name, ccdict):
        self.name = name
        self.cc = ccdict[self.name]
    def link(self, other):
        listcc = [a for a in self.cc if a in other.cc]
        if len(listcc):
            return 1
    def __str__(self):
        return str(self.name)

class DBSCAN(object):
    def __init__(self, epsilon, minPts, g):
        self.epsilon = epsilon
        self.minPts = minPts
        self.graph = g
        self.npoints = g.vcount()
        self.it = iter(range(self.npoints))
	print self.npoints
	self.clusters = []
    def createCluster(self, p):
        p["group"] = self.it.next()
	self.clusters.append([p])
    def expandCluster(self, c):
        for p in c:
            if p["checked"] != None:
                continue
            if len(self.graph.neighbors(p.index)) >= self.minPts:
                for j in self.graph.neighbors(p.index):
                    q = self.graph.vs()[j]
                    if q["group"] == None:
                        q["group"] = p["group"]
                        c.append(q)
            p["checked"] = 1

