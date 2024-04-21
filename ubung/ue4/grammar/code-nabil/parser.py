from grammar import *
from parse import *

# H 3.2
def is_in_language(words: list, grammar: Grammar) -> bool:
    # Initialize chart to store constituents that can generate substrings
    n = len(words)
    chart = [[set() for _ in range(n + 1)] for _ in range(n + 1)]

    # Initialize chart with lexical items (words)
    for i in range(1, n + 1):
        word = words[i - 1]
        for rule in grammar.rule_map[(Symbol(word),)]:
            chart[i - 1][i].add(rule.lhs)

    # CKY algorithm for parsing
    for length in range(2, n + 1):
        for start in range(n - length + 1):
            end = start + length
            for mid in range(start + 1, end):
                for rule in grammar.rules:
                    if len(rule.rhs) == 2:  # Consider only binary rules
                        left, right = rule.rhs
                        if left in chart[start][mid] and right in chart[mid][end]:
                            chart[start][end].add(rule.lhs)

    # Check if the start symbol is in the last cell of the chart
    return grammar.start_symbol in chart[0][n]

# H 4.1.1
def parse(words: list, grammar: Grammar) -> list:
    # Function to recursively build parse trees
    def build_trees(chart, start, end, symbol):
        # Base case: if only one word, return a parse node with the word as terminal
        if end - start == 1:
            return [ParseNode(symbol, [ParseNode(Symbol(words[start]))])]
        
        # Recursive case: build trees using binary rules
        trees = []
        for mid in range(start + 1, end):
            for rule in grammar.rules:
                if len(rule.rhs) == 2:  # Consider only binary rules
                    left, right = rule.rhs
                    if left in chart[start][mid] and right in chart[mid][end]:
                        left_trees = build_trees(chart, start, mid, left)
                        right_trees = build_trees(chart, mid, end, right)
                        # Combine left and right trees with current non-terminal symbol
                        for lt in left_trees:
                            for rt in right_trees:
                                trees.append(ParseNode(symbol, [lt, rt]))

        # Apply unary rules after considering binary rules
        changed = True
        while changed:
            changed = False
            for rule in grammar.rules:
                if len(rule.rhs) == 1:  # Consider only unary rules
                    rhs_symbol = rule.rhs[0]
                    if rhs_symbol in chart[start][end]:
                        trees.extend(build_trees(chart, start, end, rule.lhs))
                        changed = True
        return trees

    # Initialize chart to store constituents that can generate substrings
    n = len(words)
    chart = [[set() for _ in range(n + 1)] for _ in range(n + 1)]

    # Initialize chart with lexical items (words)
    for i in range(1, n + 1):
        word = words[i - 1]
        for rule in grammar.rule_map[(Symbol(word),)]:
            chart[i - 1][i].add(rule.lhs)

    # CKY algorithm for parsing
    for length in range(2, n + 1):
        for start in range(n - length + 1):
            end = start + length
            for mid in range(start + 1, end):
                for rule in grammar.rules:
                    if len(rule.rhs) == 2:  # Consider only binary rules
                        left, right = rule.rhs
                        if left in chart[start][mid] and right in chart[mid][end]:
                            chart[start][end].add(rule.lhs)

    # Generate parse trees using the built chart
    trees = build_trees(chart, 0, n, grammar.start_symbol)
    # Return list of parse trees
    return [ParseTree(grammar.start_symbol, [tree]) for tree in trees]



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
