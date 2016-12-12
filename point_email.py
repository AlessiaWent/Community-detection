#File containing the definitions of the needed classes. The Point class is defined in order to deal with the email links

class Point(object):
    def __init__(self, name, emdict):
        self.name = name
        self.em = emdict[self.name]
    def link(self, other):
        listem = [a for a in self.em if a in other.em]
        if len(listem):
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

