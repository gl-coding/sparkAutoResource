#!/usr/bin/python

def classify(string):
    if string.find("Kmeans") != -1:
        return "kmeans"
    elif string.find("bfs") != -1:
        return "bfs"
    elif string.find("lp") != -1:
        return "lp"
    elif string.find("NaiveBayesClassifier") != -1:
        return "nb"
    elif string.find("NaiveBayesTrainer") != -1:
        return "nbt"
    elif string.find("Sort") != -1:
        return "sort"
    elif string.find("WordCount") != -1:
        return "wc"
    elif string.find("cc") != -1:
        return "cc"
    elif string.find("pr") != -1:
        return "pr"

def readfile(filename):
    res = ""
    for line in open(filename):
        res += line
    return res

#print classify(readfile("/home/guolei/scala/KMeans-cluster/kmeans"))
#print classify(readfile("/home/guolei/scala/NaiveBayes/nb"))
#print classify(readfile("/home/guolei/scala/NaiveBayesTrainer/nbt"))
#print classify(readfile("/home/guolei/scala/Spark-Graphx/pr"))
#print classify(readfile("/home/guolei/scala/Spark-Graphx/cc"))
#print classify(readfile("/home/guolei/scala/Spark-Graphx/bfs"))
#print classify(readfile("/home/guolei/scala/Spark-Graphx/lp"))
#print classify(readfile("/home/guolei/scala/Sort/sort"))
#print classify(readfile("/home/guolei/scala/WordCount-cluster/wc"))
