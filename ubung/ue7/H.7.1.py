import sys
from collections import defaultdict, Counter
import random

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
        possible_words = list(self.ngrams[context].keys())
        probabilities = list(self.ngrams[context].values())
        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]
        return random.choices(possible_words, probabilities)[0]

    def print_model(self):
        for context, counter in self.ngrams.items():
            print(f"{context}: {dict(counter)}")

if __name__ == "__main__":
    n = int(sys.argv[1])
    model = NGramModel(n)
    
    # Read the input text file
    with open(sys.argv[2], 'r', encoding='utf-8') as f:
        text = f.read()
    model.update(text)
    model.print_model()
    
    # Example: Generate text of length 50
    generated_text = model.generate(50)
    print("Generated Text:")
    print(generated_text)
