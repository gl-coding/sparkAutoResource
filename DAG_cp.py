#!/usr/bin/python

class Vectex():
    vid = 1
    label = ""
    innum = 0
    outnum = 0

    def __cmp__(self, other):
        if self.label < other.label:
            return -1
        elif self.label == other.label:
            if self.innum < other.innum:
                return -1
            elif self.innum == other.innum:
                if self.outnum < other.outnum:
                    return -1
                elif self.outnum == other.outnum:
                    return 0
                else:
                    return 1
            else: 
                return 1
        else:
            return 1

class Graph():
    vectex = []
    def equal(self, other):
        if len(self.vectex) != len(other.vectex):
            return False
        else:
            flag = True
            for v in range(0, len(self.vectex)):
                if self.vectex != other.vectex: 
                    flag = False
            return flag

g = Graph()
vectex1 = Vectex()
vectex2 = Vectex()
vectex2.vid = 1
vectex2.label = ""
vectex2.innum = 0
vectex2.outnum = 0

b = vectex1 == vectex2

print b

l = []
l.append(vectex2)
l.append(vectex1)

ll = sorted(l)

print ll[0].vid
print ll[1].vid

g = Graph()
g.vectex.append(vectex1)
vectex1.vid = 1
print g.vectex[0].vid
