import re

# Define the semantic actions
def Likes(subject, obj):
    return f"{subject} likes {obj}"

# Define the knowledge base
knowledge_base = {
    "Noah": "Noah",  # Meaning of "Noah" is "Noah"
    "likes": Likes,  # Meaning of "likes" is a function that applies the verb to the object
    "expensive": "expensive",  # Meaning of "expensive" is "expensive"
    "restaurants": "restaurants"  # Meaning of "restaurants" is "restaurants"
}

# Define the grammar rules with associated semantic actions
grammar_rules = {
    "$S": lambda x, y: y(x),  # Sentence rule: apply the VP to the NP
    "$NP": lambda x: knowledge_base[x],  # Noun Phrase rule: return the meaning of the noun
    "$NNP": lambda x: knowledge_base[x],  # Proper Noun rule: return the meaning of the proper noun
    "$VP": lambda x, y: y(x),  # Verb Phrase rule: apply the verb to the NP
    "$VBZ": lambda f, y: lambda x: f(x, y),  # Verb rule: return a function that applies the verb to the object
    "$JJ": lambda x: knowledge_base[x],  # Adjective rule: return the meaning of the adjective
    "$NNS": lambda x: knowledge_base[x]  # Noun (plural) rule: return the meaning of the noun (plural)
}

# Parse function
# Update the parse function to handle invalid sentences
def parse_sentence(sentence):
    tokens = re.findall(r'\$[A-Za-z]+|\w+', sentence)
    stack = []

    for token in tokens:
        if token in grammar_rules:
            if len(stack) > 1 and callable(stack[-1]) and callable(stack[-2]):
                obj = stack.pop()
                subj = stack.pop()
                stack.append(stack.pop()(subj, obj))
            stack.append(grammar_rules[token])
        else:
            if token in knowledge_base:  # Check if the token is in the knowledge base
                stack.append(token)
            else:
                return "Error: Invalid sentence"  # Return an error message for invalid tokens
    
    while len(stack) > 1:
        obj = stack.pop()
        subj = stack.pop()
        stack.append(subj + " " + obj)
    
    return stack[0]

# Example sentence
sentence = "Noah likes expensive restaurants"

# Parse the sentence
result = parse_sentence(sentence)

print("Semantic representation:", result)
