#! /usr/bin/env python

""" Monte carlo simulator for Kapularalli game """
""" the "Jump probability" is fixed at 0.001, or 1/1000 """

from graafi3 import Graph
from random import random


""" Pelaa(g,n) pelauttaa n kierrosta graafissa g """
def Pelaa(g, n):
    d = 0.001
    Nodes = [u for u in g.V]
    Points = {u: 0 for u in g.V}
    i = 0
    while i < n:
        i += 1
        j = 0
        u = Nodes[int(random()*len(Nodes))]
        k = len(Nodes) + int(2*len(Nodes)*random())
        while j < k:
            j += 1
            if random() <= d:
                u = Nodes[int(random()*len(Nodes))]
                continue
            A = g.adj(u)
            u = A[int(random()*len(A))]
        Points[u] += 1
    return [u[0] for u in sorted(Points.items(), key = lambda x: x[1], reverse = True)]

if __name__ == "__main__":
    g = Graph('HT3_testidata/walk_random_769_8651')
    u = Pelaa(g,1000)
    print(u)