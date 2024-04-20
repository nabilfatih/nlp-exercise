import grammar
import parse
import parser # type: ignore

with open("../data/telescope.srgs", "r") as f:
    lines = f.readlines()
    #print("".join(lines))
    gr = grammar.Grammar(lines)
print(gr)

# H 3.1
# check if it is CNF
print(gr.is_CNF())

print(parser.example_telescope_parse().to_dot())

sentence = "I saw the duck with a telescope"
tokens = sentence.split(" ")

# H 3.2
isInLanguage = parser.is_in_language(tokens, gr)
print(isInLanguage)

# H 3.3
parsing_results = parser.parse(tokens, gr)
print(parsing_results)

# Example sentence that is not in the language
sentence = "I saw the duck with a telescope and a cat"
tokens = sentence.split(" ")

isInLanguage = parser.is_in_language(tokens, gr)
print(isInLanguage)

parsing_results = parser.parse(tokens, gr)
print(parsing_results)