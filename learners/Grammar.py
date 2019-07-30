import pickle

from nltk import ViterbiParser
from nltk import PCFG

#grammar = pickle.load(open('learners/grammar.pickle', 'rb'))

grammar = PCFG.fromstring("""
        S -> side eqside [1.0]
        eqside -> eq side [1.0]
        eq -> '=' [1.0]
        side -> side plusterm [0.3] | side minusterm [0.3] | term [0.4]
        plusterm -> plus term [1.0]
        minusterm -> minus term [1.0]
        plus -> '+' [1.0]
        minus -> '-' [1.0]
        term -> number parenside [0.2] | number variable [0.2] | number [0.2] | number vardivnum [0.2] | number divnum [0.1] | variable [0.1]
        vardivnum -> variable divnum [1.0]
        divnum -> div number [1.0]
        div -> '/' [1.0]
        number -> digit number [0.5]| digit [0.5]
        variable -> 'x' [1.0]
        parenside -> lparen siderparen [1.0]
        lparen -> '(' [1.0]
        siderparen -> side rparen [1.0]
        rparen -> ')' [1.0]
        digit -> '0' [.1] | '1' [.1] | '2' [.1] | '3' [.1] | '4' [.1] | '5' [.1] | '6' [.1] | '7' [.1] | '8' [.1] | '9' [.1]
""")

def tree_features(tree, path):
    ret = []
    node_str = ""
    for l in tree.leaves():
        node_str += l

    ret.append((('tree-label', path), tree.label()))
    ret.append((('value', path), node_str))

    print(len(tree))
    if len(tree) < 2:
        return ret

    left_rt = tree_features(tree[0], ('left-tree', path))
    right_rt = tree_features(tree[1], ('right-tree', path))

    return ret + left_rt + right_rt


if __name__ == "__main__":
    print(grammar)
    parser = ViterbiParser(grammar)

    sent = [c for c in "7/2=x"]
    print("sentence")
    print(sent)
    print("parse")
    print(parser.parse(sent))
    for tree in parser.parse(sent):
        print("tree")
        print(tree)
        print("features")
        print(tree_features(tree, 'some attribute'))
