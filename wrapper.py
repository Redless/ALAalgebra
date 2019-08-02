from Grammar import grammar
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from planner.rulesets import *

#simply add "from servtrain.Grammar import grammar" to make rulesets.py do what you want. add grammar_parse_rule to the thing where it is. stringify the paths circa 180
#in modular agent, switch from vectorized planner to FoPlanner. 

def custom_feature_set():
    return [grammar_parser_rule]

def custom_function_set():
    return [grammar_parser_rule]

def tree_features(tree, path):
    ret = []
    node_str = ""
    for l in tree.leaves():
        node_str += l
    ret.append((('tree-label', str(path)), tree.label()))
    ret.append((('value', str(path)), node_str))
    if len(tree) < 2:
        return ret
    left_rt = tree_features(tree[0], ('left-tree', path))
    right_rt = tree_features(tree[1], ('right-tree', path))
    return ret + left_rt + right_rt

from agents.ModularAgent import *
from planners.fo_planner import FoPlanner
