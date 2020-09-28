#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def log(Par):
    # this is not important from the viewpoint of logic
    # hide it from calling tree
    pass

def double(P):
    return P+P

def add(P1, P2):
    log(P1)
    log(P2)
    return P1 + P2

def main():
    breakpoint()
    A = 4
    B = 5
    Result = (add(A, double(B)))
    print(Result)

main()
