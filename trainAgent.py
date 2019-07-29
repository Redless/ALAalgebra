import requests
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import ../db.py
from nltk import ViterbiParser
from nltk.grammar import PCFG


grammar = PCFG.fromstring("""
    S -> side eqside [0.766312]
    side -> side plusterm [0.215816]
    side -> side minusterm [0.204728]
    side -> number variable [0.192571]
    number -> digit number [0.2953]
    digit -> '2' [0.20094]
    number -> '8' [0.0512296]
    variable -> 'x' [1.0]
    minusterm -> minus term [1.0]
    minus -> '-' [1.0]
    term -> digit number [0.185462]
    digit -> '6' [0.062679]
    number -> '0' [0.0918352]
    plusterm -> plus term [1.0]
    plus -> '+' [1.0]
    term -> number divnum [0.205817]
    number -> '2' [0.114112]
    divnum -> div number [1.0]
    div -> '/' [1.0]
    number -> '5' [0.0972758]
    eqside -> eq negside [0.402479]
    eq -> '=' [1.0]
    negside -> minus side [1.0]
    digit -> '1' [0.356414]
    S -> negside eqside [0.233688]
    side -> number divnum [0.0921555]
    digit -> '7' [0.0299559]
    number -> '3' [0.0644647]
    eqside -> eq side [0.597521]
    side -> 'x' [0.0759721]
    side -> '6' [0.00732374]
    digit -> '9' [0.0175681]
    number -> '6' [0.0557699]
    number -> '4' [0.0737897]
    number -> '7' [0.0733781]
    digit -> '3' [0.150809]
    term -> number variable [0.314671]
    side -> number divnumvar [0.0415636]
    divnumvar -> divnum variable [1.0]
    side -> digit number [0.074099]
    number -> dot number [0.0103797]
    dot -> '.' [1.0]
    number -> '1' [0.0461748]
    term -> 'x' [0.032113]
    digit -> '8' [0.0327874]
    digit -> '4' [0.0841404]
    digit -> '5' [0.0397696]
    number -> '9' [0.0262901]
    side -> '1' [0.0088784]
    side -> number parenside [0.0178505]
    parenside -> lparen siderparen [1.0]
    lparen -> '(' [1.0]
    siderparen -> side rparen [0.841012]
    term -> '5' [0.0212008]
    rparen -> ')' [1.0]
    term -> number parenside [0.0322466]
    term -> '3' [0.00984322]
    side -> parenside divnum [0.00844759]
    term -> parenside divnum [0.00383039]
    digit -> '0' [0.0249365]
    side -> '3' [0.00307185]
    term -> '4' [0.0399964]
    term -> '9' [0.0138963]
    term -> '1' [0.0294406]
    side -> '5' [0.00533828]
    term -> '8' [0.0189293]
    side -> '4' [0.00842886]
    side -> '2' [0.0126808]
    term -> '2' [0.035008]
    term -> number divnumvar [0.0251203]
    side -> '0' [0.0074174]
    side -> number vardivnum [0.00829774]
    vardivnum -> variable divnum [1.0]
    term -> number vardivnum [0.00944237]
    side -> dot number [0.0017045]
    side -> number starnum [0.00129243]
    starnum -> star number [1.0]
    star -> '*' [1.0]
    side -> '9' [0.00340901]
    term -> '7' [0.0130946]
    siderparen -> negside rparen [0.158988]
    term -> dot number [0.00218243]
    term -> number starnum [0.0014698]
    term -> '0' [0.00080171]
    side -> '8' [0.00681801]
    side -> '7' [0.00213531]
    term -> '6' [0.00543381]
""")

agentID = 1

url = "http://127.0.0.1:8000/"

fdir = "/Users/gabriel/"
fname = "examples2"

parser = ViterbiParser(grammar)

with open(fdir + fname) as fin:
    sentences = set()

    for eq in fin:
        eq = eq.split("\t")[2]
        eq = eq.lower()
        eq = filter(lambda ch: ch in "()1234567890+-*/.;=x", eq)
        proc = ""
        for i in eq:
            proc += i
        past = False
        for sin in proc.split(";"):
            if past:
                if parser.parse(past) and parser.parse(sin):
                    obj = {
                      "selection": "eqn",
                      "action": "UpdateTextField",
                      "inputs": {
                          "value": sin,
                      },
                      "reward": 1,
                      "state": {
                          "equation": {"id":"eqn","value":past,"contentEditable":True},
                      }
                    }
                    trainReq = requests.post(url+"train/"+str(agentID)+"/", json=obj)
                    print(trainReq.status_code, trainReq.reason)

            past = sin
