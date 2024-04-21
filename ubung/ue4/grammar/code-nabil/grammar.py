import re
from collections import defaultdict
from typing import List, Tuple, Mapping


class Symbol:
    """symbols of the grammar"""

    terminal: bool
    symbol: str

    def __init__(self, symbol: str):
        self.terminal = not symbol.startswith("$")
        self.symbol = symbol if self.terminal else symbol[1:]

    def __repr__(self):
        return ("" if self.terminal else "$") + self.symbol

    def __eq__(self, other):
        return self.symbol == other.symbol and self.terminal == other.terminal

    def __hash__(self):
        # Ensure that Symbol objects are hashable
        return hash((self.symbol, self.terminal))


class GrammarRule:
    """
    simple sequence rule.
    We don't support anything more complex;
    alternatives will have to be split into multiple sub-rules """

    lhs: Symbol
    rhs: List[Symbol]  # it's a list of Symbols

    def __init__(self, lhs: Symbol, rhs: list):
        self.lhs, self.rhs = lhs, rhs

    def __eq__(self, other):
        return self.lhs == other.lhs and self.rhs == other.rhs

    def __repr__(self):
        return str(self.lhs) + " = " + " ".join([str(s) for s in self.rhs]) + ";"
    
    def __hash__(self):
        # Ensure that GrammarRule objects are hashable
        return hash((self.lhs, tuple(self.rhs)))


class Grammar:
    language: str
    start_symbol: Symbol
    rules: List[GrammarRule] = []  # list of GrammarRules
    symbols: Mapping[str, Symbol] = {}  # map from strings to symbols
    rule_map: Mapping[tuple, GrammarRule] # map from RHSs to the matching rules

    """initialize a new grammar from a srgs grammar file"""
    def __init__(self, lines, grammar_format="SRGS"):  # FIXME: maybe implement JSGF import in the future
        assert grammar_format == "SRGS", "illegal format descriptor: {}".format(grammar_format)
        lines = [re.sub("//.*$", "", line) for line in lines]  # remove comment lines
        lines = [line.strip() for line in lines if not re.match(r"^ *$", line)]  # remove empty lines
        assert lines.pop(0).lower() == "#abnf v1.0 utf-8;", "maybe something is wrong with header?"
        lang = re.match(r"language\s+(\S*)\s*;", lines.pop(0).lower())
        assert lang and len(lang.groups()) == 1, "cannot find correct language tag: {}".format(lang)
        self.language = lang.group(0)
        for line in lines:
            match = re.match(r"((?:public)?)\s*(\$\S+)\s*=\s*(.*)\s*;", line)
            assert match and len(match.groups()) == 3, "cannot parse line {}".format(line)
            is_public = match.group(1) != ""
            lhs = self.get_symbol(match.group(2))
            rhs = [self.get_symbol(s) for s in re.split(r"\s+", match.group(3))]
            rule = GrammarRule(lhs, rhs)
            self.rules.append(rule)
            if is_public:
                self.start_symbol = lhs
        self.build_rule_map()

    def build_rule_map(self):
        self.rule_map = defaultdict(lambda: [])
        for r in self.rules:
            self.rule_map[tuple(r.rhs)].append(r)


    def get_symbol(self, symbol: str):
        if symbol not in self.symbols:
            self.symbols[symbol] = Symbol(symbol)
        return self.symbols[symbol]

    def __repr__(self):
        return "#ABNF V1.0 utf-8\n" + \
               "language " + self.language + "\n" + \
               "\n".join([str(r) if r.lhs != self.start_symbol else "public " + str(r) for r in self.rules])

    # H 3.1
    def is_CNF(self):
        for rule in self.rules:
            if len(rule.rhs) == 1 and rule.rhs[0].terminal: # terminal rhs
                continue
            if len(rule.rhs) == 2 and not rule.rhs[0].terminal and not rule.rhs[1].terminal: # non-terminal rhs
                continue
            return False
        return True
    
    # H 4.1.2
    def is_relaxedCNF(self) -> bool:
        for rule in self.rules:
            if len(rule.rhs) > 2:
                return False  # Rule is not binary
            if len(rule.rhs) == 2:
                if any(not symbol.terminal for symbol in rule.rhs):
                    return False  # Binary rule produces a terminal
            elif len(rule.rhs) == 1:
                if rule.rhs[0].terminal:
                    return False  # Unary rule produces a terminal
        return True
    
    # H 4.1.3
    def normalize_to_relaxedCNF(self):
        # Create dictionaries to store normalized rules, public rules, and start symbol
        normalized_rules = {}
        public_rules = {}
        start_symbol = None

        # Iterate over each rule in the grammar
        for rule in self.rules:
            # Track public rules and start symbol
            if "public" in str(rule):
                public_rules[rule.lhs] = rule.rhs
            if rule.lhs == self.start_symbol:
                start_symbol = rule.lhs

            if len(rule.rhs) > 2:
                # If the rule has more than two symbols on the right-hand side, split it into binary rules
                lhs = rule.lhs
                non_terminals = [Symbol(f"${lhs.symbol}_NT{i}") for i in range(len(rule.rhs) - 1)]
                for i, rhs_symbol in enumerate(rule.rhs[:-1]):
                    new_rule = GrammarRule(lhs, [rhs_symbol, non_terminals[i]])
                    normalized_rules.setdefault(lhs, set()).add(tuple(new_rule.rhs))
                    lhs = non_terminals[i]
                new_rule = GrammarRule(lhs, [rule.rhs[-1]])
                normalized_rules.setdefault(lhs, set()).add(tuple(new_rule.rhs))
            elif len(rule.rhs) == 1 and not rule.rhs[0].terminal:
                # If the rule is unary, replace it with a binary rule
                new_symbol = Symbol(f"${rule.lhs.symbol}_NT")
                new_rule = GrammarRule(rule.lhs, [rule.rhs[0], new_symbol])
                normalized_rules.setdefault(rule.lhs, set()).add(tuple(new_rule.rhs))
            else:
                # Keep the rule unchanged
                normalized_rules.setdefault(rule.lhs, set()).add(tuple(rule.rhs))

        # Update the grammar with normalized rules, public rules, and start symbol
        self.rules = [GrammarRule(lhs, list(rhs_list)) for lhs, rhs_list in normalized_rules.items()]
        self.rules.extend([GrammarRule(lhs, list(rhs_list)) for lhs, rhs_list in public_rules.items()])
        self.start_symbol = start_symbol

    def __repr__(self):
        # Format the grammar rules as a string
        grammar_str = "#ABNF V1.0 utf-8;\n"
        grammar_str += f"{self.language}\n"

        for rule in self.rules:
            if "public" in str(rule):
                grammar_str += "public "
            grammar_str += f"{str(rule.lhs)} = "
            grammar_str += " | ".join(str(sym) for sym in rule.rhs)
            grammar_str += ";\n"

        # remove parentheses and commas
        return grammar_str.replace("(", "").replace(")", "").replace(",", "")

