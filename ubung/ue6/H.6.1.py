import argparse
import random

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--random-seed', type=int, default=1,
                    help='set random seed for replicability; 0 implies truly random seed')
parser.add_argument('--source', type=str, required=True)
parser.add_argument('-N', type=int, default=3)
parser.add_argument('--start', type=str, required=True)
parser.add_argument('--length', type=int, default=5000)

# let's represent n-grams in the following way
# for each n-gram prefix we keep a hash which includes the count at key, say, 0,
# and next characters (i.e., full n-grams) in keys corresponding to the character.


def ngrams_from_text(f, N):
    prefix = list(f.read(N - 1))
    last = f.read(1)
    while last != '':
        yield prefix, last
        prefix = prefix[1:] + list(last)
        last = f.read(1)


def get_base_node(model, prefix):
    """from our model tree, get the node that represents the prefix"""
    node = model
    for c in prefix:
        if c not in node:
            node[c] = {}
        node = node[c]
    return node


def add_ngram_to_model(model, prefix, last):
    base = get_base_node(model, prefix)
    if last not in base:
        base[last] = 0
    base[last] += 1


def generate(model, start):
    start = list(start)
    while True:
        base = get_base_node(model, start)
        chars, counts = zip(*base.items())
        char_list = random.choices(population=chars, weights=counts, k=1)
        start = start[1:] + char_list
        yield char_list[0]


def estimate_model(args):
    model = {}
    with open(args.source, 'r', encoding='utf-8') as f:
        ngram_source = ngrams_from_text(f, args.N)
        for ngram in ngram_source:
            add_ngram_to_model(model, ngram[0], ngram[1])
    return model


if __name__ == '__main__':
    args = parser.parse_args()
    model = estimate_model(args)
    assert len(args.start) == args.N - 1
    print(args.start, end='')
    i = 0
    for c in generate(model, args.start):
        print(c, end='')
        i += 1
        if i > args.length:
            break
    print()