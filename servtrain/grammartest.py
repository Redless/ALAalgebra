import pickle

from nltk import ViterbiParser
from nltk.grammar import PCFG
from WhatLearner import pCFG_Grammar
'''
grammar = PCFG.fromstring("""
        S -> side eqside [.5] | negside eqside [0.5]
        eqside -> eq side [.5] | eq negside [0.5]
        eq -> '=' [1.0]
        plusterm -> plus term [1.0]
        minusterm -> minus term [1.0]
        plus -> '+' [1.0]
        minus -> '-' [1.0]
        negside -> minus side [1.0]
        vardivnum -> variable divnum [1.0]
        varstarnum -> variable starnum [1.0]
        divnum -> div number [1.0]
        starnum -> star number [1.0]
        div -> '/' [1.0]
        star -> '*' [1.0]
        number -> digit number [.333] | digit [.334] | dot number [.333]
        side -> side plusterm [.334] | side minusterm [.333] | term [.333]
        term -> number parenside [.16666] | number variable [.16666] | number [.1] | number vardivnum [.1] | number divnum [.16666] | variable [.16666] | number starnum [.00004] | parenside divnum [.06666] | number divnumvar [.06666]
        dot -> '.' [1.]
        divnumvar -> divnum var [1.]
        variable -> 'x' [1.0]
        parenside -> lparen siderparen [1.0]
        lparen -> '(' [1.0]
        siderparen -> side rparen [.5] | negside rparen [.5]
        rparen -> ')' [1.0]
        digit -> '0' [.1] | '1' [.1] | '2' [.1] | '3' [.1] | '4' [.1] | '5' [.1] | '6' [.1] | '7' [.1] | '8' [.1] | '9' [.1]
""")#'''

grammar = PCFG.fromstring("""
    S -> negside eqside [0.5]
    S -> side eqside [0.5]
    digit -> '0' [0.1]
    digit -> '1' [0.1]
    digit -> '2' [0.1]
    digit -> '3' [0.1]
    digit -> '4' [0.1]
    digit -> '5' [0.1]
    digit -> '6' [0.1]
    digit -> '7' [0.1]
    digit -> '8' [0.1]
    digit -> '9' [0.1]
    div -> '/' [1.0]
    divnum -> div number [1.0]
    divnumvar -> divnum variable [1.0]
    dot -> '.' [1.0]
    eq -> '=' [1.0]
    eqside -> eq negside [0.5]
    eqside -> eq side [0.5]
    lparen -> '(' [1.0]
    minus -> '-' [1.0]
    minusterm -> minus term [1.0]
    negside -> minus side [1.0]
    number -> '0' [.05]
    number -> '1' [.05]
    number -> '2' [.05]
    number -> '3' [.05]
    number -> '4' [.05]
    number -> '5' [.05]
    number -> '6' [.05]
    number -> '7' [.05]
    number -> '8' [.05]
    number -> '9' [.05]
    number -> digit number [.05]
    number -> dot number [0.45]
    parenside -> lparen siderparen [1.0]
    plus -> '+' [1.0]
    plusterm -> plus term [1.0]
    rparen -> ')' [1.0]
    side -> '0' [.04]
    side -> '1' [.04]
    side -> '2' [.04]
    side -> '3' [.04]
    side -> '4' [.04]
    side -> '5' [.04]
    side -> '6' [.04]
    side -> '7' [.04]
    side -> '8' [.04]
    side -> '9' [.04]
    side -> 'x' [.04]
    side -> digit number [.04]
    side -> dot number [.04]
    side -> number divnum [.04]
    side -> number divnumvar [.04]
    side -> number parenside [.04]
    side -> number starnum [.04]
    side -> number vardivnum [.04]
    side -> number variable [.04]
    side -> parenside divnum [.04]
    side -> side minusterm [.04]
    side -> side plusterm [.16]
    siderparen -> negside rparen [0.5]
    siderparen -> side rparen [0.5]
    star -> '*' [1.0]
    starnum -> star number [1.0]
    term -> '0' [.05]
    term -> '1' [.05]
    term -> '2' [.05]
    term -> '3' [.05]
    term -> '4' [.05]
    term -> '5' [.05]
    term -> '6' [.05]
    term -> '7' [.05]
    term -> '8' [.05]
    term -> '9' [.05]
    term -> 'x' [.05]
    term -> digit number [.05]
    term -> dot number [.05]
    term -> number divnum [.05]
    term -> number divnumvar [.05]
    term -> number parenside [.05]
    term -> number starnum [.05]
    term -> number vardivnum [.05]
    term -> number variable [.05]
    term -> parenside divnum [.05]
    vardivnum -> variable divnum [1.0]
    variable -> 'x' [1.0]
    varstarnum -> variable starnum [1.0]
""")

if __name__ == "__main__":
    print(grammar)
    #sentences = set()

    fdir = "/Users/gabriel/"
    fname = "examples2"

    #sent = ['2', '8', 'x', '-', '5', '7', '.', '6', '=', '-', '1', '0', 'x']
    #sent = [i for i in "28x-57.6=-10x"]
    #print("impo")
    #for n in parser.parse(sent):
    #    print(n)

    #exit()

    with open(fdir + fname) as fin:
        sentences = set()

        for eq in fin:
            eq = eq.split("	")[2]
            eq = eq.lower()
            eq = filter(lambda ch: ch in "()1234567890+-*/.;=x", eq)
            proc = ""
            for i in eq:
                proc += i
            for sin in proc.split(";"):
                print(sin)
                sentences.add(sin)

    sents = [[c for c in s] for s in sentences]

    prob_inducer = pCFG_Grammar()

    prob_inducer.grammar = grammar

    parser = ViterbiParser(grammar)

    test = '(5-9x)-5+18=-2/7x'
    #test = '5+18=2/7x'
    for i in parser.parse([i for i in test]): print(i)

    print("INDUCING WEIGHTS:")

    prob_inducer.induce_weights(sentences)

    grammar = prob_inducer.grammar

    print("GRAMMAR:")
    print(grammar)

    total = 0
    gotten = 0

    parser = ViterbiParser(grammar)

    for sent in sents:
        gotone = False
        print("now parsing:")
        print(sent)
        print(parser.parse(sent))
        total += 1
        for tree in parser.parse(sent):
            if not gotone:
                gotone = True
                gotten += 1
            print("tree:")
            print(tree)

    print("TOTAL EQUATIONS:",total)
    print("SUCCESSFULLY PARSED:",gotten)

    print(grammar)
