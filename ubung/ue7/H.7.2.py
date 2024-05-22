import sys
from collections import defaultdict, Counter
import random
import math

class NGramModel:
    def __init__(self, n):
        self.n = n
        self.ngrams = defaultdict(Counter)
        self.start_symbol = "<s>"
        self.end_symbol = "</s>"

    def update(self, text):
        # Split the text into lines
        lines = text.strip().split('\n')
        for line in lines:
            # Prepend <s> symbols and append </s>
            tokens = [self.start_symbol] * (self.n - 1) + line.split() + [self.end_symbol]
            # Generate n-grams for the current line
            for i in range(len(tokens) - self.n + 1):
                context = tuple(tokens[i:i + self.n - 1])
                next_word = tokens[i + self.n - 1]
                self.ngrams[context][next_word] += 1

    def generate(self, length):
        # Start with the initial context of <s> symbols
        context = (self.start_symbol,) * (self.n - 1)
        result = list(context)
        for _ in range(length):
            next_word = self.choose_word(context)
            if next_word == self.end_symbol:
                break
            result.append(next_word)
            context = tuple(result[-(self.n - 1):])
        return ' '.join(result[self.n - 1:])

    def choose_word(self, context):
        # Choose the next word based on the context using the probability distribution
        possible_words = list(self.ngrams[context].keys())
        probabilities = list(self.ngrams[context].values())
        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]
        return random.choices(possible_words, probabilities)[0]

    def get_probability(self, context, word):
        # Get the probability of the given word in the given context
        if context in self.ngrams and word in self.ngrams[context]:
            total = sum(self.ngrams[context].values())
            return self.ngrams[context][word] / total
        else:
            # Return a very small probability for unknown words
            return 1e-6

    def calculate_cross_entropy(self, text):
        # Calculate the cross-entropy of the model on the given text
        tokens = [self.start_symbol] * (self.n - 1) + text.split() + [self.end_symbol]
        log_prob_sum = 0
        for i in range(len(tokens) - self.n + 1):
            context = tuple(tokens[i:i + self.n - 1])
            word = tokens[i + self.n - 1]
            prob = self.get_probability(context, word)
            log_prob_sum += math.log(prob)
        cross_entropy = -log_prob_sum / len(tokens)
        return cross_entropy

    def calculate_perplexity(self, text):
        # Calculate the perplexity of the model on the given text
        cross_entropy = self.calculate_cross_entropy(text)
        perplexity = math.exp(cross_entropy)
        return perplexity

    def print_model(self):
        # Print the n-grams and their counts
        for context, counter in self.ngrams.items():
            print(f"{context}: {dict(counter)}")

if __name__ == "__main__":
    n = int(sys.argv[1])
    model = NGramModel(n)
    
    # Read the training text file
    with open(sys.argv[2], 'r', encoding='utf-8') as f:
        text = f.read()
    model.update(text)
    model.print_model()
    
    # Example: Generate text of length 50
    generated_text = model.generate(50)
    print("Generated Text:")
    print(generated_text)
    
    # Read the test text file
    with open(sys.argv[3], 'r', encoding='utf-8') as f:
        test_text = f.read()
    
    # Calculate and print cross-entropy and perplexity for the test data
    cross_entropy = model.calculate_cross_entropy(test_text)
    perplexity = model.calculate_perplexity(test_text)
    print(f"Cross-Entropy: {cross_entropy}")
    print(f"Perplexity: {perplexity}")
