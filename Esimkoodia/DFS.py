#! /usr/bin/env python
""" Depth-first search example """

from graafi import Graph

""" Depth-first search from s. Returns a dictionary of nodes with 
    D[u] = (a,b), such that a is the time the node was found and b time when it was finished. """

def DFS(g, s):
    D = {}
    global color
    color = {}
    global t
    t = 0
    DFSvisit(g, s, D)
    return D, color

def DFSvisit(g, u, D):
    global color
    color[u] = "gray"
    global t
    D[u] = [t, -1]
    for v in g.adj(u):
        if not v in D:
            t += 1
            DFSvisit(g,v, D)
    t+=1
    D[u][1] = t
    color[u] = "black"


""" testcode """
if __name__ == "__main__":
    g = Graph('testgraph')
    D, color = DFS(g,1)
    print D
    print color

