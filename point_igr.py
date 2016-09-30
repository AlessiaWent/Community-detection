import pp
#module for igraph program

class Point(object):
    def __init__(self, name, rolesdict, entdict):
        self.visited = False
        self.checked = False
        self.name = name
        self.neigh = []
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

