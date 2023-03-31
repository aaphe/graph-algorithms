#! /usr/bin/env python
""" Dijkstra-search example """

from graafi import Graph


## Our own implementation for priorityqueue
class PQ:
    def __init__(self):
        self.H = []
        self.Index = {}

    def __contains__(self, key):
        if key in self.Index and self.Index[key] > 0:
            return True
        return False

    def empty(self):
        if len(self.H) > 0:
            return False
        return True
    
    def done(self,value):
        if value in self.Index and self.Index[value] < 0:
            return True
        return False

    def push(self,a):
        if a[1] in self:
            self.update(a)
        i = len(self.H)
        self.H.append(a)
        while i > 0:
            j = (i-1)/2
            if self.H[j] > a:
                self.H[i] = self.H[j]
                self.H[j] = a
                i = j
            else:
                break
        self.Index[a[1]] = i

    def pop(self):
        togo = self.H[0]
        a = self.H.pop()
        if a == togo:
            self.Index[a[1]] = -1
            return togo
        self.H[0] = a
        i = 0
        while (2*i + 1) < len(self.H):
            left = 2*i + 1
            right = 2*i + 2
            if self.H[left] < a:
                if right >= len(self.H) or self.H[right] > self.H[left]:
                    self.H[i] = self.H[left]
                    self.H[left] = a
                    i = left
                    self.Index[self.H[i][1]] = i
                    continue
            if right < len(self.H) and self.H[right] < a:
                self.H[i] = self.H[right]
                self.H[right] = a
                i = right
                continue
            break
        self.Index[a[1]] = i
        self.Index[togo[1]] = -1
        return togo

    def update(self, a):
        value = a[0]
        oldvalue = self.H[i][0]
        key = a[1]
        i = self.Index[key]
        self.H[i] = a 
        ## Decrease priority, i.e., move up
        if oldvalue > value:
            while i > 0:
                j = (i-1) / 2
                if self.H[j] <= a:
                    self.Index[key] = i
                    return
                self.H[i] = self.H[j]
                self.H[j] = a
                i = j
            self.Index[key] = 0
        ## Increase prioerity: Not allowed
        else:
            raise Exception("key value increase not allowed")




""" dijkstra search from s. Returns a dictionary of nodes with 
    D[u] = d, such that d is the distance from s """

## This is the relaxation function. Returns "true" if and only if the 
## distance is smaller from u to v. 
def relax(u,v,g,D):
    dd = g.W[(u,v)]
    if not v in D:
        D[v] = D[u] + dd
        return True
    if D[v] > D[u] + dd:
        D[v] = D[u] + dd
        return True
    return False



def Dijkstra(g, s):
    Q = PQ()
    D = {}
    D[s] = 0
    Q.push((0,s))
    print Q.H, len(Q.H)
    while not Q.empty():
        (d, u) = Q.pop()
        for v in g.adj(u):
            if not Q.done(v):
                if relax(u,v,g,D):
                    Q.push((D[v], v))
    return D



""" testcode """
if __name__ == "__main__":
    g = Graph('testgraph_weighted')
    D = Dijkstra(g,1)
    print D

