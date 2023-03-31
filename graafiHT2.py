# Graafialgoritmit syksy 2021
# Ohjelmointiharkkatyö 2
# Aapo Hetemaa

from graafi3 import Graph
# from graafiHT1 import CountShortest
from PQ import PQ
from disjoint import disjoint_set
from copy import deepcopy as copy

#! /usr/bin/env python


## Read set
def ReadNodes(filename):
    ff = open(filename, 'r')
    x = ff.readlines()[0].split()
    S = []
    for i in x:
        S.append(int(i))
    return S

# Input: kaksi virtausfunktiota f1 ja f2 painotetussa graafissa
# Output: näiden kahden virtauksen summavirtaus
def SumFlow(f1, f2):
    f = copy(f1)
    for (u, v) in f2:
        if not (u, v) in f:
            f[(u, v)] = f2[(u, v)]
        else:
            f[(u, v)] += f2[(u, v)]
    return f


# Tekee residuaaliverkon Gr, eli "vähentää" graafista G virtauksen f
def MakeResidual(G, f):
    Gr = copy(G)
    for (u, v) in f:
        c = 0
        ## Copy the weight
        if (u, v) in Gr.W:
            c = Gr.W[(u, v)]
        # calculate residual capasity
        cf = c - f[(u, v)]
        if cf < 0:
            print(f[(u,v)], c)
            raise Exception("Kapasiteetin ylitys kaaressa (" + str(u) + ", " + str(v) + ")")
        if not v in Gr.AL[u]:
            Gr.addEdge(u, v)
        Gr.W[(u, v)] = cf
    return Gr


def FindAugPath(Gr, s, t):
    laskuri = 0
    # Dict, josta löytyy aina solmun kohdalta sitä edeltävä solmu
    pred = {}
    pred[s] = s
    B = {}
    B[s] = 0
    Q = [s]
    # Tehokkuutta voidaan lisätä hieman lopettamalla heti kun polun toinen pää
    # löytyy
    tNotFound = True
    # Tästä alkaa modattu BFS-algoritmi
    while Q and tNotFound:
        u = Q.pop(0)
        d = B[u]
        for v in Gr.adj(u):
            laskuri += 1
            # Huomioidaan vain ne kaaret, joissa on kapasiteettia jäljellä
            if Gr.W[(u, v)] > 0 and v not in B:
                pred[v] = u
                B[v] = d+1
                Q.append(v)
                if v == t:
                    tNotFound = False

    # Jos polkue ei löydetty
    if t not in pred:
        return [], laskuri
    aug = []
    aug.append(t)
    node = pred[t]
    aug.append(node)
    # Listassa nyt t ja pred[t]. Loopataan kunnes tulee s vastaan
    while node != s:
        node = pred[node]
        aug.append(node)
    aug.reverse()
    return aug, laskuri


# Relaxation function for maxing Djikstra
def relax(u, v, g, D):
    dd = g.W[(u, v)]
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
    print(Q.H, len(Q.H))
    while not Q.empty():
        (d, u) = Q.pop()
        for v in g.adj(u):
            if not Q.done(v):
                if relax(u,v,g,D):
                    Q.push((D[v], v))
    return D


def MakeAugFlow(Gr, s, t, path):
    f = {}
    if not path:
        return f
    if path[0] != s:
        raise Exception("Path not from s")
    if path[-1] != t:
        raise Exception("Path not to t")

    # Etsitään pienin kapasiteetti cfp polulla
    cfp = Gr.W[(path[0], path[1])]
    u = s
    for v in path[1:]:
        cap = Gr.W[(u, v)]
        if cap < cfp:
            cfp = cap
        u = v

    u = s
    # Ja nyt joka kaaren virtaukseksi asetetaan pienimmän kapasiteetin verran
    # virtausta
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
    #pp = FindAugPath(G, s, t)
    pp = FindAugPath(G, s, t)
    # 0. jäsen on palautettu jäännöspolku
    p = pp[0]
    # 1. jäsen on funktion sisäisen laskurin tulos
    laskuri += pp[1]
    fp = MakeAugFlow(G, s, t, p)
    # Lisätään täydentävä virtaus päävirtaukseen
    f = SumFlow(f, fp)
    # Jäännösverkko
    Gr = MakeResidual(G, f)
    i = 0
    # indeksi on varmistamassa, ettei algoritmi tee ikuisesti ohjelmaa
    # (suurella graafilla mahdollista)
    while p and i < 1000:
        i += 1
        pp = FindAugPath(Gr, s, t)
        p = pp[0]
        laskuri += pp[1]
        fp = MakeAugFlow(Gr, s, t, p)
        f = SumFlow(f, fp)
        Gr = MakeResidual(G, f)
    print("Laskuri laski: " + str(laskuri))
    return f


if __name__ == "__main__":
    G = Graph("testgraph_weighted")
    S = ReadNodes("testset_flow")
    s = S[0]
    t = S[1]
    f = FordFulkerson(G, s, t)
    print(f)
