from collections import defaultdict
from HornKB import *

def bc_entails(KB, query, inferred=None):

    # Initialize inferred dictionary if not provided
    if inferred is None:
        inferred = defaultdict(bool)

    # Check if the query is already a known fact
    if query in KB.facts:
        inferred[query] = True
        return True, list(inferred.keys())

    # Explore each clause in the KB to see if it can conclude the query
    for clause in KB.clauses:
        if clause.conclusion == query:
            # All premises of the clause must be proven true
            all_premises_proven = True

            for premise in clause.premises:
                if not inferred[premise]:
                    # Recursively prove each premise; memoize the result
                    result, _ = bc_entails(KB, premise, inferred)
                    if result:
                        inferred[premise] = True
                    else:
                        all_premises_proven = False
                        break

            if all_premises_proven:
                inferred[query] = True
                return True, list(inferred.keys())

    return False, list(inferred.keys())
