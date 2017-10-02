#!/usr/bin/env python

import sys, fileinput
import tree

file_obj = open("train.trees.pre", "w")

for line in fileinput.input(sys.argv[1:]):
    t = tree.Tree.from_str(line)

    # Binarize, inserting 'X*' nodes.
    t.binarize()

    # Remove unary nodes
    t.remove_unit()

    # The tree is now strictly binary branching, so that the CFG is in Chomsky normal form.

    # Make sure that all the roots still have the same label.
    assert t.root.label == 'TOP'

    file_obj.write("%s\n" % t)
    # print t

file_obj.close()
