#! /usr/bin/env python
from graafi import Graph
from CountShortest_dum import CountShortest

def ReadSet(filename):
    ff = open(filename,'r')
    x = ff.readlines()[0].split()
    S =set([])
    for i in x:
        S.add(int(i))
    return S

if __name__ == "__main__":
    G = Graph('testgraph_harkka')
    B = ReadSet('testset1')
    x = CountShortest(G, B, 6,4)
    print(x)
