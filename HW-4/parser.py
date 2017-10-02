import sys, fileinput
import collections
import math


def read_cfg():
    """
    Reads normalized Probabilistic CFG from the file having rules in format
    NT -> T # P or NT -> NT NT # P where NT is non-terminal, T is terminal
    and P is probability value of the rule
    :return: a tuple of tuples with each tuple having three elements:
    left symbol, right terminal or tuple of right symbols (always 2)
    and probability value
    a dictionary with terminal elements to check unknown words in original sentences
    """
    cfg_file = "train.trees.cfg.lower"
    cfg = ()
    terminals_dict = {}
    for line in fileinput.input(cfg_file):
        tokens = line.split(" ")
        # print tokens
        if len(tokens) == 5: # terminal rule
            cfg = cfg + ((tokens[0], tokens[2], tokens[4].rstrip()),)
            terminals_dict[tokens[2]] = tokens[2]
        elif len(tokens) == 6: #non-terminal rule
            cfg = cfg + ((tokens[0], (tokens[2], tokens[3]), tokens[5].rstrip()),)
        else:
            cfg = cfg + ((),)
    # for left, right, p in cfg:
    #     print left, right, p
    #print terminals_dict
    return cfg, terminals_dict


def build(CFG):
    G = collections.defaultdict(list)
    for left, right, p in CFG:
        G[right].append((left, math.log10(float(p))))
    return G

def show_cell(T, i, j):
    for x, (p, l, r) in T[i][j].iteritems():
        print "[%d,%d,%s]=%g: %r and %r" % (i, j, x, math.exp(p), l, r)

def pcky(G, W):
    # create a list of lists of empty dicts something like: [[{}, {}, ...], [{}, {}, ...], ... ]
    T = [[{} for j in range(len(W)+1)] for i in range(len(W))]
    for j in range(1, len(W)+1):
        for left, p in G.get(W[j-1], {}):
            T[j-1][j][left] = (p, (W[j-1], j, j), (W[j-1], j, j))
        for i in range(j-2, -1, -1):
            for k in range(i+1, j):
                for x, (px, lx, rx) in T[i][k].iteritems():
                    for y, (py, ly, ry) in T[k][j].iteritems():
                        for left, p in G.get((x, y), {}):
                            pnew = px + py + p
                            if left not in T[i][j] or T[i][j][left][0] < pnew:
                                T[i][j][left] = (pnew, (x, i, k), (y, k, j))
            # print i, j
            # show_cell(T, i, j)
    return T

def select_max_rule(T, start, end):
    if start == end:
        return {}
    max_rule = {}
    max_rule["probability"] = 0
    for x, (p, l, r) in T[start][end].iteritems():
        if math.exp(p) > max_rule["probability"]:
            max_rule["left"] = x
            max_rule["right"] = (l, r)
            max_rule["probability"] = p
    return max_rule

def make_tree(T, x, start, end):
    if start == end:
        return ""
    (p, l, r) = T[start][end][x]
    if l == r:
        return "(%s %s)" % (x, l[0])
    result = "(%s %s %s)" % (x, make_tree(T, l[0], l[1], l[2]), make_tree(T, r[0], r[1], r[2]))
    return result


if __name__ == '__main__':

    file_obj = open("parser.output", "w")
    CFG, terminals = read_cfg()
    CFG_dict = build(CFG)
    datafile = "dev.strings"
    #datafile = "test.txt"
    sentnum = 1
    for line in fileinput.input(datafile):
        line = line.split("\n")[0]
        print sentnum
        sentnum += 1
        W = line.split(" ")
        origin_W = list(W)
        print W
        #W = ['time', 'flies', 'like', 'an', 'arrow']
        #print terminals
        for i in range(len(W)):
            W[i] = W[i].lower()
            if W[i] not in terminals:
                W[i] = "<unk>"
        #print W
        T = pcky(CFG_dict, W)
        #show_cell(T, 0, len(W))
        max_rule = select_max_rule(T, 0, len(W))
        left = max_rule.get("left")
        if left is None:
            print "No parse tree available"
            file_obj.write("\n")
            continue

        result_unk = make_tree(T, left, 0, len(W))
        print "Before replacing: "
        print result_unk

        # now replace every terminal with actual word in sentence
        # this way all <unk>s are replaced as well as cases are restored
        wordnum = 0
        result = result_unk
        i = 0
        result_i = 0
        while i < len(result_unk):
            if result_unk[i].isalpha() and result_unk[i].islower():
                j = i
                while result_unk[j] != ')':
                    j += 1
                # now i to j is the string to be replaced
                result_j = result_i + (j-i)
                result = result[:result_i] + origin_W[wordnum] + result[result_j:]
                i = j
                result_i += len(origin_W[wordnum])
                wordnum += 1
            if result_unk[i] == '<':
                result = result[:result_i] + origin_W[wordnum] + result[result_i+5:]
                result_i += len(origin_W[wordnum])
                i += 5
                wordnum += 1
            else:
                result_i += 1
                i += 1

        print "After replacing: "
        print result
        print "Probability: ", max_rule["probability"] #gives log probability base 10
        file_obj.write(result+"\n")

    file_obj.close()

## First string output:
# (TOP (S (NP (DT The) (NN flight)) (VP (MD should) (VP (VB be) (NP (CD eleven) (RB a.m) (NN tomorrow))))) (PUNC .))
## log-probability of first string base 10 = -16.2231146715

## Output from evalb.py script on initial parser (PCKY without modifications)
# dev.parses.post 440 brackets
# dev.trees       474 brackets
# matching        405 brackets
# precision       0.920454545455
# recall  0.854430379747
# F1      0.886214442013





