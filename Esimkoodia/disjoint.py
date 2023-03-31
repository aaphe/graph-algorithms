#! /usr/bin/env python


""" Implements the disjoint set data structure """
class disjoint_set:
    def __init__(self):
        self.depth = {}
        self.rep = {}
        pass
    def MakeSet(self,x):
        if x in self.rep:
            raise Exception("Make set called illegally")
        ## only works for hashable ##
        self.depth[x] = 0
        self.rep[x] = None
    def Find(self,x):
        if not x in self.rep:
            raise Exception("illegal find")
        if self.rep[x] == None:
            return x
        u = Find(self.rep[x])
        self.rep[x] = u
        return u
    def Union(self,x,y):
        u = self.Find(x)
        v = self.Find(y)
        if self.depth[u] == self.depth[v]:
            self.rep[u] = v
            self.depth[v] = self.depth[v] + 1
        elif self.depth[u] < self.depth[v]:
            self.rep[u] = v
        else:
            self.rep[v] = u
    ## Get is highly inefficient! 
    def Get(self,x):
        u = set([x])
        for y in self.rep:
            if self.Find(y) == self.Find(x):
                u.add(y)
        return u
    
        
