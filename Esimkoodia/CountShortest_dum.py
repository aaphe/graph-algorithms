#! /usr/bin/env python
""" Breadth-first search example """

from graafi import Graph

def ReadSet(filename):
    ff = open(filename,'r')
    x = ff.readlines()[0].split()
    S =set([])
    for i in x:
        S.add(int(i))
    return S

def CountShortest(g, S, s, t):
    return 0
   
