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
        return hash(self.symbol)


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
        normalized_rules = []  # New set of rules after normalization
        for rule in self.rules:
            if len(rule.rhs) > 2:
                # Replace rule with equivalent binary rules
                lhs = rule.lhs
                non_terminals = [Symbol(f"${lhs.symbol}_NT{i}") for i in range(len(rule.rhs) - 1)]
                for i, rhs_symbol in enumerate(rule.rhs[:-1]):
                    normalized_rules.append(GrammarRule(lhs, [rhs_symbol, non_terminals[i]]))
                    lhs = non_terminals[i]
                normalized_rules.append(GrammarRule(lhs, [rule.rhs[-1]]))
                # Mark original rule and new non-terminal symbols as normalized
                rule.lhs.normalized = True
                for symbol in non_terminals:
                    symbol.normalized = True
            elif len(rule.rhs) == 1 and not rule.rhs[0].terminal:
                # Replace unary rule with equivalent binary rule
                new_symbol = Symbol(f"${rule.lhs.symbol}_NT")
                normalized_rules.append(GrammarRule(rule.lhs, [rule.rhs[0], new_symbol]))
                # Mark original rule and new non-terminal symbol as normalized
                rule.lhs.normalized = True
                new_symbol.normalized = True
            else:
                # Keep the rule unchanged
                normalized_rules.append(rule)
        # Update grammar with normalized rules
        self.rules = normalized_rules

