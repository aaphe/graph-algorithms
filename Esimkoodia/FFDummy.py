#! /usr/bin/env python

## Dummy toteutus Ford Fulkersonille.

from graafi3 import Graph
from copy import deepcopy as copy


## Read set
def ReadNodes(filename):
    ff = open(filename, 'r')
    x = ff.readlines()[0].split()
    S = []
    for i in x:
        S.append(int(i))
    return S


def SumFlow(f1, f2):
    f = copy(f1)
    for (u, v) in f2:
        if not (u, v) in f:
            f[(u, v)] = f2[(u, v)]
        else:
            f[(u, v)] += f2[(u, v)]
    return f


## Tekee residuaaliverkon
def MakeResidual(G, f):
    Gr = copy(G)
    for (u, v) in f:
        c = 0
        ## Copy the weight
        if (u, v) in Gr.W:
            c = Gr.W[(u, v)]
        # calculate residual capasity
        cf = c - f[(u, v)]
        if not v in Gr.AL[u]:
            Gr.addEdge(u, v)
        Gr.W[(u, v)] = cf
    return Gr


## This is not implemented. Implement the augmenting path algorithm here
def FindAugPath(Gr, s, t):
    aug = []
    ## Laskuri laskee montako kaarta selataan
    laskuri = 0
    ## Katsoo ainoastaan ovatko s ja t naapureita, ei muuta
    for u in Gr.adj(s):
        laskuri += 1
        if u == t and Gr.W[(s, u)] > 0:
            aug.append(s)
            aug.append(t)
            break
    return (aug, laskuri)


## This is only a template, and does not work. Edit it to make it proper!
def MakeAugFlow(Gr, s, t, path):
    f = {}
    if not path:
        return f
    if path[0] != s:
        raise Exception("Path not from s")
    if path[-1] != t:
        raise Exception("Path not to t")
    u = s
    ## This is the minimum capacity on the path. Find it!
    cfp = Gr.W[(s, t)]
    #
    # Tahan tarvitaan implementaatio cfp:n laskemiselle
    #
    for v in path:
        # Skip loops and first
        if v == u:
            continue
        f[(u, v)] = cfp
        f[(v, u)] = -cfp
        if Gr.W[(u, v)] < cfp:
            raise Exception("illegal residual flow")
        u = v
    return f


def FordFulkerson(G, s, t):
    # laskuri laskee montako kaarta selataan
    laskuri = 0
    f = {}
    pp = FindAugPath(G, s, t)
    p = pp[0]
    laskuri += pp[1]
    fp = MakeAugFlow(G, s, t, p)
    f = SumFlow(f, fp)
    Gr = MakeResidual(G, f)
    i = 0
    while p and i < 1000:
        i += 1
        pp = FindAugPath(Gr, s, t)
        p = pp[0]
        laskuri += pp[1]
        fp = MakeAugFlow(Gr, s, t, p)
        f = SumFlow(f, fp)
        Gr = MakeResidual(Gr, f)
    print("Laskuri laski: " + str(laskuri))
    return f


if __name__ == "__main__":
    G = Graph("testgraph_weighted")
    S = ReadNodes("testset_flow")
    s = S[0]
    t = S[1]
    f = FordFulkerson(G, s, t)
    print
    f