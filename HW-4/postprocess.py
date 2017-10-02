#!/usr/bin/env python

import sys, fileinput
import tree

file_obj = open("dev.parses.post", "w")

for line in fileinput.input(sys.argv[1:]):
    t = tree.Tree.from_str(line)
    if t.root is None:
        file_obj.write("\n")
        # print
        continue
    t.restore_unit()
    t.unbinarize()

    file_obj.write("%s\n" % t)
    # print t


