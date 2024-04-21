from grammar import *
from parse import *
from parser import * # type: ignore

# H 4 (Testing)

# Define a non-normalized grammar
# Example of a non-normalized grammar
non_normalized_grammar_str = """
#ABNF V1.0 utf-8;
language en;
public $S = $NP $VP;
$NP = I;
$NP = $Det  $N;
$Det = the;
$Det = a;
$Det = my;
$Det = her;
$N = duck;
$N = telescope;
$VP = $VP $PP;
$VP = $V $NP;
$V = saw;
$N = saw;
$V = duck;
$NP = $NP $PP;
$PP = $P $NP;
$P = with;
"""

# Test parsing with the non-normalized grammar
def test_parsing():
    # Create a non-normalized grammar object
    non_normalized_grammar = Grammar(non_normalized_grammar_str.split("\n"))

    # Test parsing a sentence
    words = ["I", "saw", "the", "duck", "with", "a", "telescope"]
    parses = parse(words, non_normalized_grammar)
    for pars in parses:
        print(pars)

# Test normalization of the non-normalized grammar
def test_normalization():
    # Create a non-normalized grammar object
    non_normalized_grammar = Grammar(non_normalized_grammar_str.split("\n"))

    # Normalize the grammar
    non_normalized_grammar.normalize_to_relaxedCNF()

    # Print the normalized grammar
    print(non_normalized_grammar)

# Test removal of extra nodes introduced during normalization
def test_extra_node_removal():
    # Define a parse tree with extra nodes introduced during normalization
    parse_tree = ParseTree(Symbol("$S"), [
        ParseNode(Symbol("$NP"), [
            ParseNode(Symbol("$Det"), [ParseNode(Symbol("the"))]),
            ParseNode(Symbol("$N"), [ParseNode(Symbol("duck"))]),
            ParseNode(Symbol("$NP_NT"), [  # Extra node introduced during normalization
                ParseNode(Symbol("$Det"), [ParseNode(Symbol("the"))]),
                ParseNode(Symbol("$N"), [ParseNode(Symbol("telescope"))])
            ])
        ]),
        ParseNode(Symbol("$VP"), [
            ParseNode(Symbol("$V"), [ParseNode(Symbol("saw"))]),
            ParseNode(Symbol("$NP"), [
                ParseNode(Symbol("$Det"), [ParseNode(Symbol("the"))]),
                ParseNode(Symbol("$N"), [ParseNode(Symbol("duck"))])
            ]),
            ParseNode(Symbol("$PP"), [
                ParseNode(Symbol("$P"), [ParseNode(Symbol("with"))]),
                ParseNode(Symbol("$NP"), [
                    ParseNode(Symbol("$Det"), [ParseNode(Symbol("a"))]),
                    ParseNode(Symbol("$N"), [ParseNode(Symbol("telescope"))])
                ])
            ])
        ])])

    # Print the parse tree before removing extra nodes
    print("Parse Tree before extra node removal:")
    print(parse_tree)

    # Remove extra nodes introduced during normalization
    parse_tree.remove_normalized_nodes()

    # Print the parse tree after removing extra nodes
    print("Parse Tree after extra node removal:")
    print(parse_tree)

# Run the tests
if __name__ == "__main__":
    print("Testing Parsing:")
    test_parsing()
    print("\nTesting Normalization:")
    test_normalization()
    print("\nTesting Extra Node Removal:")
    test_extra_node_removal()
