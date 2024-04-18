from grammar import *
from parse import *


def is_in_language(words: list, grammar: Grammar) -> bool:
    n = len(words)
    chart = [[defaultdict(lambda: []) for _ in range(n - i)] for i in range(n)]
    
    # first step: initialize bottom row of the table
    # main steps for each row
    # for each cell
    # look at possible splits of left/right
    # if we find one (use symbols left/right as pairs in grammar.rule_map to look up the rules)
    # add ParseNode that points to ParseNodes in left/right cells and has lhs of rule as "symbol"
    
    return grammar.start_symbol in chart[0][0]
    
    # it is easier to start out with a parser that merely
    # checks if the sentence is in the language at all (without returning
    # the derivations).
    # eventually, once you have implemented parse() below,
    # you can simply write
    # "return len(parse(words, grammar)) > 0"


def parse(words: list, grammar: Grammar) -> list:
    """
    parses the list of words with grammar and returns the (possibly empty) list
    of possible parses. The ordering of possible parses is arbitrary.
    returns a list of ParseTree
    """
    raise NotImplementedError  # TODO: this is your job.
    l =  [x for x in chart[0][0] if x.symbol == grammar.start_symbol]  # not much better than the exception because we promise above to return all parses...
    for x in l:
        x.__class__ = ParseTree
    return l

def example_telescope_parse():
    return \
        ParseTree(Symbol("$S"),
                  [ParseNode(Symbol("$NP"),
                             [ParseNode(Symbol("I"))]),
                   ParseNode(Symbol("$VP"),
                             [ParseNode(Symbol("$VP"),
                                        [ParseNode(Symbol("$V"),
                                                   [ParseNode(Symbol("saw"))]),
                                         ParseNode(Symbol("$NP"),
                                                   [ParseNode(Symbol("$Det"),
                                                              [ParseNode(Symbol("the"))]),
                                                    ParseNode(Symbol("$N"),
                                                              [ParseNode(Symbol("duck"))])])]),
                              ParseNode(Symbol("$PP"),
                                        [ParseNode(Symbol("$P"),
                                                   [ParseNode(Symbol("with"))]),
                                         ParseNode(Symbol("$NP"),
                                                   [ParseNode(Symbol("$Det"),
                                                              [ParseNode(Symbol("a"))]),
                                                    ParseNode(Symbol("$N"),
                                                              [ParseNode(Symbol("telescope"))])])])])])
