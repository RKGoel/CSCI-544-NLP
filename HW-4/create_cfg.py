import sys, fileinput
import collections
import operator

from decimal import Decimal

import tree

rules_dict = collections.defaultdict(float)
node_freq = collections.defaultdict(int)
rules_freq = collections.defaultdict(int)
file_obj = open("train.trees.cfg.lower", "w")

for line in fileinput.input(sys.argv[1:]):
    t = tree.Tree.from_str(line)
    nodes = list(t.bottomup())
    for node in nodes:
        if len(node.children) == 0:
            continue
        node_freq[node.label] += 1

for line in fileinput.input(sys.argv[1:]):
    t = tree.Tree.from_str(line)
    nodes = list(t.bottomup())
    for node in nodes:
        str = node.label + " -> "
        if len(node.children) == 0:
            continue
        if len(node.children) == 1:
            str += node.children[0].label.lower()
        else:
            str += node.children[0].label + " " + node.children[1].label
        # for i in range(len(node.children)):
        #     str += node.children[i].label
        #     str += " "
        rules_dict[str] += float(node_freq[node.label]**-1)
        rules_freq[str] += 1

print "Rule with max freq: ", max(rules_freq.iteritems(), key=operator.itemgetter(1))[0]
print "Freq: ", max(rules_freq.iteritems(), key=operator.itemgetter(1))[1]

for rule, probability in rules_dict.items():
    file_obj.write("%s # %s\n" % (rule, probability))

file_obj.close()

## Total number of rules in grammar (case sensitive): 752
## Total number of rules in grammar (case in-sensitive): 723
## Most frequent rule: PUNC -> . (with frequency 346)