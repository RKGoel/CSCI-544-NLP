#!/usr/bin/env python

import sys, fileinput
import collections
import tree

count = collections.defaultdict(int)
file_obj = open("train.trees.pre.unk", "w")

trees = []
for line in fileinput.input(sys.argv[1:]):
    t = tree.Tree.from_str(line)
    for leaf in t.leaves():
        count[leaf.label] += 1
    trees.append(t)

for t in trees:
    for leaf in t.leaves():
        if count[leaf.label] < 2:
            leaf.label = "<unk>"
    file_obj.write("{0}\n".format(t))
    #sys.stdout.write("{0}\n".format(t))
