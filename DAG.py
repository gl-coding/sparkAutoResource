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

    def toStr(self):
        return self.label + ":" + str(self.innum) + ":" + str(self.outnum)

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

    def getSize(self):
        return len(vectex)
    
    def toStr(self):
        res = ""
        for v in self.vectex:
            print v.toStr()
        #return "aaaaaaaaaa"
        
        
def readGraphSeq(filename):
    #print "start=========================================================="
    Graphs = []
    l = []
    for line in open(filename):
        arg = line.strip("\n")
        l.append(arg)
    labelmap = {}
    edgemapIn = {}
    edgemapOut = {}
    #g = Graph()
    for idx in range(0, len(l)):
        line = l[idx]
        #print line
        if line.startswith("t"):
            g = Graph()
            g.vectex = []
            labelmap = {}
            edgemapIn = {}
            edgemapOut = {}
        elif line.startswith("v"):
            k = line.split(" ")[1]
            v = line.split(" ")[2]
            labelmap[k] = v
        else:
            start = line.split(" ")[1]
            end   = line.split(" ")[2]
            if edgemapIn.has_key(end):
                edgemapIn[end] += 1
            else:
                edgemapIn[end] = 1

            if edgemapOut.has_key(start):
                edgemapOut[start] += 1
            else:
                edgemapOut[start] = 1
        #print labelmap
        #print edgemapIn
        #print edgemapOut
        if idx == len(l)-1 or l[idx+1].startswith("t"):
            #print len(labelmap)
            for m in labelmap:
                #print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
                #print "label:" + m
                v = Vectex()
                v.vid = m
                v.label = labelmap[m]
                if edgemapIn.has_key(m):
                    v.innum = int(edgemapIn[m])
                if edgemapOut.has_key(m):
                    v.outnum = int(edgemapOut[m])
                #print len(g.vectex)
                g.vectex.append(v)
            g.vectex = sorted(g.vectex)
            #print g.toStr()
            Graphs.append(g)
    return Graphs

def normal_leven(gs1, gs2):
      len_str1 = len(gs1) + 1
      len_str2 = len(gs2) + 1
      #create matrix
      matrix = [0 for n in range(len_str1 * len_str2)]
      #init x axis
      for i in range(len_str1):
          matrix[i] = i
      #init y axis
      for j in range(0, len(matrix), len_str1):
          if j % len_str1 == 0:
              matrix[j] = j // len_str1

      for i in range(1, len_str1):
          for j in range(1, len_str2):
              if gs1[i-1].equal(gs2[j-1]):
                  cost = 0
              else:
                  cost = 1
              matrix[j*len_str1+i] = min(matrix[(j-1)*len_str1+i]+1,
                                          matrix[j*len_str1+(i-1)]+1,
                                          matrix[(j-1)*len_str1+(i-1)] + cost)

      return matrix[-1]
  
def getSimilarity(gs1, gs2):
    distance = normal_leven(gs1, gs2)*1.0
    res = 0.0
    res = 1 - distance/(len(gs1)+len(gs2))
    return res

filelist = []
filelist.append("kmeans")
filelist.append("bfs")
filelist.append("pr")
filelist.append("lp")
filelist.append("cc")
filelist.append("nb")
filelist.append("nbt")
filelist.append("wc")
filelist.append("sort")

basedir = "/home/guolei/sparkInfo/graphs/"

testcase = "title"

for f in filelist:
    testcase += "\t" + f
    
#print testcase
    
for src in filelist:
    res = src
    for tar in filelist:
        srcfile = basedir + src + ".g"
        tarfile = basedir + tar + ".g"
        gs1 = readGraphSeq(srcfile)
        gs2 = readGraphSeq(tarfile)
        sim = getSimilarity(gs1, gs2)
        res += "\t" + str(sim)
    print testcase
    print res
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
        

exit()
gs1 = readGraphSeq("graph.log")
gs2 = readGraphSeq("graph1.log")

#for i in range(0, len(gs2)):
#    print "======================="
#    gs1[i].toStr()
#    print "======================="
#    gs2[i].toStr()
#    print "======================="
#    print gs1[i].equal(gs2[i])

#print normal_leven(gs1, gs2)
print getSimilarity(gs1, gs2)
