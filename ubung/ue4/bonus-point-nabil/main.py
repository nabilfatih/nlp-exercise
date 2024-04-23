# Define the context-free grammar
grammar = {
    "$S": [("$NP", "$VP")],
    "$NP": [("$NNP",), ("$JJ", "$NNS")],
    "$VP": [("$VBZ", "$NP")],
    "$NNP": [("Noah",)],
    "$JJ": [("expensive",)],
    "$NNS": [("restaurants",)],
    "$VBZ": [("likes",)],
}

# Define the knowledge base for semantic analysis
knowledge_base = {
    "Noah": "Noah",
    "expensive": "expensive",
    "restaurants": "restaurants",
    "likes": lambda x, y: f"{x} likes {y}",
}

def parse_sentence(tokens, start_symbol="$S"):
    if start_symbol not in grammar:
        return None
    
    for production in grammar[start_symbol]:
        parse_tree = {}
        index = 0
        for symbol in production:
            if index >= len(tokens):
                break
            if symbol.startswith("$"):
                subtree = parse_sentence(tokens[index:], symbol)
                if subtree is None:
                    break
                parse_tree[symbol] = subtree
                index += len(subtree.get("tokens", []))
            else:
                if tokens[index] == symbol:
                    parse_tree[symbol] = tokens[index]
                    index += 1
                else:
                    break
        else:
            return {"symbol": start_symbol, "production": production, "subtree": parse_tree, "tokens": tokens[:index]}
    return None

def evaluate_semantics(parse_tree):
    symbol = parse_tree["symbol"]
    production = parse_tree["production"]
    if symbol not in knowledge_base:
        return None
    if len(production) == 1:
        return knowledge_base[symbol]
    else:
        args = [parse_tree["subtree"][symbol] if symbol in parse_tree["subtree"] else symbol for symbol in production[1:]]
        return knowledge_base[symbol](*args)

def parse_and_evaluate(sentence):
    tokens = sentence.split()
    parse_tree = parse_sentence(tokens)
    if parse_tree is None:
        return "Unable to parse sentence."
    semantics = evaluate_semantics(parse_tree)
    if semantics is None:
        return "Unable to evaluate semantics."
    return semantics

# Example parses
print(parse_and_evaluate("Noah likes expensive restaurants"))
