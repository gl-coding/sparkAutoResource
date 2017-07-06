#!/usr/bin/pythona

def VF2Equal(Graph1, Graph2):
    partialG1 = partialSort(Graph1)
    partialG2 = partialSort(Graph2)
    if partialG1 != partialG2:
        return False
    return VF2.equal(Graph1, Graph2)
