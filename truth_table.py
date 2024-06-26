from GenericSentence import *
from Tokenizer import *

from itertools import *
import re

# Generate all possible models based on a list of prop symbols


def generate_models(symbols):
    return list(product([True, False], repeat=len(symbols)))

# Truth-checking a fact in a model


def evaluate_fact(fact, model={}):
    return model.get(fact, False)

# Truth-checking a Horn Clause in a model


def evaluate_horn_clause(clause, model={}):
    premise_true = all(model.get(premise, False)
                       for premise in clause.premises)

    conclusion_true = model.get(clause.conclusion, False)

    # a => b <==> ~a v b
    return (not premise_true) or conclusion_true

# Check if the KB is true in a model


def evaluate_hornkb(kb, model={}):
    # Evaluate each fact
    if kb.facts:
        for fact in kb.facts:
            if not evaluate_fact(fact, model):
                return False  # Short-circuit if any fact is false

    # Evaluate each clause
    for clause in kb.clauses:
        if not evaluate_horn_clause(clause, model):
            return False  # Short-circuit if any clause is false

    return True

# Main evaluation function for Horn KB


def truth_table_check_hornkb(kb, query):
    entailed = True
    count = 0

    # Generate all symbols
    symbols = kb.get_all_symbols()

    # Handling edge cases where query is not a symbol included in KB
    if query not in symbols:
        return ("NO", count)

    # Generate the models
    models = generate_models(symbols)
    for model in models:
        symbol_model = dict(zip(symbols, model))

        # Check for models where KB is true)
        if evaluate_hornkb(kb, symbol_model):

            count += 1
            # If the query is not true in that model
            if not evaluate_fact(query, symbol_model):
                entailed = False

    return ("YES", count) if entailed else ("NO", count)

# --------------- Generic KB ---------------------


# Evaluate an expression in RPN (Postfix representation)


def evaluate_rpn(expression, model):
    stack = []
    for token in expression:
        if token.isalnum():  # operand
            # Retrieve the boolean value from the model
            stack.append(model.get(token, False))
        else:  # operator
            if token == '~':
                operand = stack.pop()
                stack.append(not operand)
            else:
                right = stack.pop()
                left = stack.pop()
                if token == '&':
                    stack.append(left and right)
                elif token == '||':
                    stack.append(left or right)
                elif token == '=>':
                    stack.append(not left or right)
                elif token == '<=>':
                    stack.append(left == right)

    return stack.pop()


def evaluate_generic_sentence(sentence, model={}):
    rpn = sentence.to_rpn()

    result = evaluate_rpn(rpn, model)

    return result


# Check truth value of a generic KB


def evaluate_generic_kb(kb, model={}):
    for fact in kb.facts:
        if not evaluate_fact(fact, model):
            return False

    for sentence in kb.generic_sentences:
        if not evaluate_generic_sentence(sentence, model):
            return False

    return True


def truth_table_check_generickb(kb, query):
    entailed = True
    count = 0

    # Get all prop symbols from a KB
    symbols = kb.get_all_symbols()

    if not query.get_symbols().issubset(symbols):
        return ("NO", count)

    # Generate all models
    models = generate_models(symbols)

    for model in models:
        symbol_model = dict(zip(symbols, model))

        # If the kb is true in a model
        if evaluate_generic_kb(kb, symbol_model):
            count += 1
            # Check if the query is also true
            if not evaluate_generic_sentence(query, symbol_model):
                entailed = False

    return ("YES", count) if entailed else ("NO", count)
