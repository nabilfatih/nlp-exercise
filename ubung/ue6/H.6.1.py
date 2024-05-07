from collections import defaultdict
import random

# Sample text with the prefix 'LAM' included in it
text = "LAMbda functions are anonymous functions in Python. LAMinate the document before submission."

# Function to build the N-gram model from the given text
def build_ngram_model(text, N):
    ngrams = defaultdict(list)
    # Create all possible N-grams
    for i in range(len(text) - N):
        key = text[i:i+N-1]  # Extract the prefix of length N-1
        value = text[i+N-1]  # The next character after the prefix
        ngrams[key].append(value)
    return ngrams

# Function to generate text using the N-gram model
def generate_text(ngrams, prefix, length):
    if len(prefix) != N-1:
        raise ValueError("Prefix length must be N-1.")
    
    output = prefix  # Start the output with the given prefix
    for _ in range(length):
        choices = ngrams.get(prefix, None)  # Get possible next characters
        if not choices:
            break  # No possible extensions, stop generation
        next_char = random.choice(choices)  # Randomly select the next character
        output += next_char  # Add the selected character to the output
        prefix = prefix[1:] +next_char  # Update the prefix
    return output

# Parameters for the N-gram model
N = 4  # Using trigrams (N=4 means we consider three characters and predict the fourth)
prefix = 'LAM'
length = 100  # Generate 100 characters

# Build the model and generate text
ngrams = build_ngram_model(text, N)
generated_text = generate_text(ngrams, prefix, length)

# Print the generated text
print(generated_text)


"""
1. N too large: If N is too large, you might not find any matches for the given prefix in the text, leading to very short or no output.

2. Representation of N-gram data: In this script, we used a dictionary to map prefixes to possible continuations.
   This is memory intensive but fast for lookup. An alternative could be using a trie (prefix tree), 
   which might save memory at the cost of potentially slower lookups.
"""