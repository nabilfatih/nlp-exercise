from grammar import Grammar, Symbol
import pandas as pd

# H 3.2
def is_in_language(words: list, grammar: Grammar) -> bool:
    n = len(words)
    table = make_table(n, words, grammar, parsing=False)
    return grammar.start_symbol in table[0][n], pd.DataFrame(table)
    
# H 3.2 PARSING
class ParseTree:
    """ Represents a node in a parse tree with a symbol and optional children """
    def __init__(self, symbol, children=None):
        self.symbol = symbol
        self.children = children if children else []

    def __repr__(self):
        return f"[{self.symbol} [{' '.join(map(str, self.children))}]]" if self.children else str(self.symbol)

def parse(words: list, grammar: Grammar) -> list:
    n = len(words)
    table = make_table(n, words=words, grammar=grammar, parsing=True)

    # Extract parse trees that derive the entire sentence from the start symbol
    possible_parses = [tree for tree in table[0][n] if tree.symbol == grammar.start_symbol]

    if possible_parses:
        print("Possible parses:")
    else:
        print("No valid parse found for the sentence.")

    return possible_parses


def make_table(n, words, grammar, parsing=False):
    # init table
    table = [[[] if parsing else set() for _ in range(n + 1)] for _ in range(n + 1)]
    
    # Initialize all terminals in the table
    
    
    
    for i in range(n):
        symbol = Symbol(words[i])
        for rule in grammar.rules:
            if len(rule.rhs) == 1 and rule.rhs[0] == symbol:
                if parsing:
                    table[i][i + 1].append(ParseTree(rule.lhs, [ParseTree(symbol)]))
                else:
                    table[i][i + 1].add(rule.lhs)
                    
    """ EXAMPLE PART 1
    print(nicer_cky_table(table))
                0      1         2       3         4     5       6     7
            0  {}  {$NP}        {}      {}        {}    {}      {}    {}
            1  {}     {}  {$V, $N}      {}        {}    {}      {}    {}
            2  {}     {}        {}  {$Det}        {}    {}      {}    {}
            3  {}     {}        {}      {}  {$V, $N}    {}      {}    {}
            4  {}     {}        {}      {}        {}  {$P}      {}    {}
            5  {}     {}        {}      {}        {}    {}  {$Det}    {}
            6  {}     {}        {}      {}        {}    {}      {}  {$N}
            7  {}     {}        {}      {}        {}    {}      {}    {}
    """

    # Initialize all NON!!!-terminals in the table
    for length in range(2, n + 1):
        for start in range(n - length + 1):
            end = start + length
            for mid in range(start + 1, end):
                for rule in grammar.rules:
                    if len(rule.rhs) == 2:
                        left, right = rule.rhs
                        if parsing:
                            for left_tree in table[start][mid]:
                                for right_tree in table[mid][end]:
                                    if left_tree.symbol == left and right_tree.symbol == right:
                                        table[start][end].append(ParseTree(rule.lhs, [left_tree, right_tree]))
                        else:
                            if left in table[start][mid] and right in table[mid][end]:
                                table[start][end].add(rule.lhs)
                                
    """ EXAMPLE PART 2
    print(nicer_cky_table(table))
                0      1         2       3         4     5       6      7
            0  {}  {$NP}        {}      {}      {$S}    {}      {}   {$S}
            1  {}     {}  {$V, $N}      {}     {$VP}    {}      {}  {$VP}
            2  {}     {}        {}  {$Det}     {$NP}    {}      {}  {$NP}
            3  {}     {}        {}      {}  {$V, $N}    {}      {}     {}
            4  {}     {}        {}      {}        {}  {$P}      {}  {$PP}
            5  {}     {}        {}      {}        {}    {}  {$Det}  {$NP}
            6  {}     {}        {}      {}        {}    {}      {}   {$N}
            7  {}     {}        {}      {}        {}    {}      {}     {}
    """
        
    return table


