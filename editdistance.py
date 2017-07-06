#!/usr/bin/python

import Levenshtein

stra = "asdfadfas"
strb = "afdasdfsa"

print Levenshtein.distance(stra, strb)
print Levenshtein.hamming(stra, strb)
print Levenshtein.ratio(stra, strb)
print Levenshtein.jaro(stra, strb)
print Levenshtein.jaro_winkler(stra, strb)
