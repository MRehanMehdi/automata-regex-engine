# modules/nfa_builder.py

class State:
    """Represents a single NFA state"""
    def __init__(self, name):
        self.name = name

class NFA:
    """Represents an NFA with transitions"""
    def __init__(self, start_state, final_state, transitions):
        self.start_state = start_state
        self.final_state = final_state
        self.transitions = transitions  # {state: {symbol: [next_states]}}

class NFABuilder:
    def __init__(self):
        self.state_count = 0  # for unique state names

    def new_state(self):
        self.state_count += 1
        return f"q{self.state_count}"

    def build_basic(self, symbol):
        """Build NFA for single symbol"""
        start = self.new_state()
        end = self.new_state()
        transitions = {start: {symbol: [end]}, end: {}}
        return NFA(start, end, transitions)

    def concatenate(self, nfa1, nfa2):
        """Concatenate two NFAs"""
        # Merge transitions
        for state, paths in nfa2.transitions.items():
            if state not in nfa1.transitions:
                nfa1.transitions[state] = paths
        # Add ε-transition from nfa1 final to nfa2 start
        nfa1.transitions[nfa1.final_state]['ε'] = [nfa2.start_state]
        return NFA(nfa1.start_state, nfa2.final_state, nfa1.transitions)

    def union(self, nfa1, nfa2):
        """Union (OR) of two NFAs"""
        start = self.new_state()
        end = self.new_state()
        transitions = {start: {'ε': [nfa1.start_state, nfa2.start_state]}, end: {}}
        # Merge nfa1 transitions
        for state, paths in nfa1.transitions.items():
            transitions[state] = paths
        # Merge nfa2 transitions
        for state, paths in nfa2.transitions.items():
            transitions[state] = paths
        # Add ε-transitions from nfa1 and nfa2 finals to new end
        transitions[nfa1.final_state]['ε'] = [end]
        transitions[nfa2.final_state]['ε'] = [end]
        return NFA(start, end, transitions)

    def kleene_star(self, nfa):
        """Apply Kleene star (*) to NFA"""
        start = self.new_state()
        end = self.new_state()
        transitions = {start: {'ε': [nfa.start_state, end]}, end: {}}
        # Merge nfa transitions
        for state, paths in nfa.transitions.items():
            transitions[state] = paths
        # Add ε-transitions from old final to nfa start and new end
        transitions[nfa.final_state]['ε'] = [nfa.start_state, end]
        return NFA(start, end, transitions)

    def build_from_postfix(self, postfix):
        """Construct NFA from postfix regex"""
        stack = []
        for char in postfix:
            if char.isalnum():
                stack.append(self.build_basic(char))
            elif char == '.':
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                stack.append(self.concatenate(nfa1, nfa2))
            elif char == '+':
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                stack.append(self.union(nfa1, nfa2))
            elif char == '*':
                nfa = stack.pop()
                stack.append(self.kleene_star(nfa))
            else:
                raise ValueError(f"Unknown symbol in postfix: {char}")
        return stack.pop()


# =======================
# Example usage
# =======================
if __name__ == "__main__":
    from modules.regex_parser import RegexParser

    regex = "ed+ee+f(ddd+dd+d)*"
    parser = RegexParser(regex)
    parser.validate()
    parser.add_concatenation()
    postfix = parser.to_postfix()
    print("Postfix:", postfix)

    builder = NFABuilder()
    nfa = builder.build_from_postfix(postfix)

    print("\nNFA Transition Table:")
    for state, paths in nfa.transitions.items():
        print(f"{state}: {paths}")

    print("\nStart State:", nfa.start_state)
    print("Final State:", nfa.final_state)
