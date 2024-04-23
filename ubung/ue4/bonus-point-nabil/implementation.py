# Define the knowledge base mapping words to their parts of speech
knowledge_base = {
    "Noah": "$NNP",
    "likes": "$VBZ",
    "expensive": "$JJ",
    "restaurants": "$NNS",
    "Sarah": "$NNP",
    "dislikes": "$VBZ",
    "noisy": "$JJ",
    "bars": "$NNS"
}

# Define the grammar rules along with semantic representations
grammar_rules = {
    "$S": "('Likes', 'Noah', x)",
    "$NP": "('NNP', x)",
    "$NNP": "'Noah'",
    "$VP": "('Likes', y, x)",
    "$VBZ": "(lambda f, y: all(f(x) for x in y) and ('Likes', y, x))",
    "$JJ": "(lambda x: ('Expensive', x))",
    "$NNS": "(lambda x: ('Restaurant', x))"
}

# Define a simple Likes function
def Likes(subject, object):
    return f"{subject} likes {object}"

def Expensive(adjective):
    return f"Expensive({adjective})"

def Restaurant(noun):
    return f"Restaurant({noun})"

# Convert lambda expressions to executable Python code
def convert_to_lambda(expression):
    # Replace 'x' placeholder with actual parameter name
    expression = expression.replace("x", "y")
    return eval(f"lambda y: {expression}")

# Function to evaluate the semantic representation
def evaluate_semantic_representation(semantic_representation, words):
    if isinstance(semantic_representation, tuple):
        # If it's a tuple, it represents a semantic structure
        if len(semantic_representation) == 1:
            return semantic_representation[0]
        else:
            # Build the semantic representation recursively
            return semantic_representation[0] + '(' + ', '.join(evaluate_semantic_representation(arg, words) for arg in semantic_representation[1:]) + ')'
    elif callable(semantic_representation):
        # If it's a function, call it with the provided argument
        return semantic_representation(words)
    else:
        return semantic_representation

# Function to parse a sentence and return its semantic representation
def parse_sentence(sentence):
    words = sentence.split()
    semantic_representation = None

    # Parse each word in the sentence
    for word in words:
        # Look up the word in the knowledge base to get its part of speech
        if word in knowledge_base:
            pos = knowledge_base[word]
            # Look up the part of speech in the grammar rules
            if pos in grammar_rules:
                semantic_expression = grammar_rules[pos]
                semantic_function = convert_to_lambda(semantic_expression)
                if semantic_representation:
                    semantic_representation = semantic_function(semantic_representation)
                else:
                    semantic_representation = semantic_function
            else:
                print(f"No grammar rule found for part of speech: {pos}")
        else:
            # Handle unknown words
            print(f"Unknown word: {word}")

    return evaluate_semantic_representation(semantic_representation, words)

# Example sentences
sentences = [
    "Noah likes expensive restaurants",
    "Sarah dislikes noisy bars",
]

# Parse each sentence and print its semantic representation
for sentence in sentences:
    semantic_representation = parse_sentence(sentence)
    print(f"Sentence: {sentence}")
    print(f"Semantic Representation: {semantic_representation}\n")
