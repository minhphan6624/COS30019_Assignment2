class HornClause:
    def __init__(self, clause):
        self.premises = []
        self.conclusion = None
        self.parse_clause(clause)

    # Parse the premise and conclusion of a Horn Clause
    def parse_clause(self, clause):
        parts = clause.split('=>')
        self.conclusion = parts[1].strip()
        self.premises = parts[0].strip().split('&')

    # Get all the propositional symbols in the clause:
    def get_symbols(self):
        symbols = set(self.premises)
        symbols.add(self.conclusion.strip())
        return symbols

    # Display function for debugging purposes
    def display(self):
        print(', '.join(self.premises),
              "=>", self.conclusion)
