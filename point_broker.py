class Point(object):
    def __init__(self, name, rolesdict, entdict):
        self.name = name
        self.ent = rolesdict[self.name]
        self.ci = []
        for e in self.ent:
            try:
                if entdict[e] != '':
                    self.ci.append(entdict[e])
            except KeyError:
                pass
    def link(self, other):
        if len([a for a in self.ci if a in other.ci]) or len([a for a in self.ent if a in other.ent]):
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

