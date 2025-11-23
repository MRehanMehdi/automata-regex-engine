# modules/dfa_builder.py

class DFABuilder:
    def __init__(self, nfa_transitions, nfa_start, nfa_final):
        """
        Initialize the DFA Builder.
        Parameters:
        - nfa_transitions: dict {state: {symbol: [next_states]}}
        - nfa_start: start state of NFA
        - nfa_final: final state of NFA
        """
        self.nfa = nfa_transitions
        self.nfa_start = nfa_start
        self.nfa_final = nfa_final
        self.symbols = self.get_symbols()
        self.dfa = {}
        self.start_state = None
        self.final_states = set()

    def get_symbols(self):
        """Get all symbols used in NFA except ε"""
        symbols = set()
        for paths in self.nfa.values():
            symbols.update(paths.keys())
        symbols.discard('ε')
        return symbols

    def epsilon_closure(self, states):
        """Compute ε-closure of a set of NFA states"""
        stack = list(states)
        closure = set(states)
        while stack:
            state = stack.pop()
            for next_state in self.nfa.get(state, {}).get('ε', []):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return closure

    def move(self, states, symbol):
        """Move NFA states on a given symbol"""
        result = set()
        for state in states:
            result.update(self.nfa.get(state, {}).get(symbol, []))
        return result

    def build_dfa(self):
        """Construct DFA using subset construction"""
        start_set = frozenset(self.epsilon_closure([self.nfa_start]))
        unmarked = [start_set]
        dfa_states_map = {start_set: "D0"}
        self.start_state = "D0"
        self.dfa["D0"] = {}
        state_count = 1

        while unmarked:
            current_set = unmarked.pop()
            current_name = dfa_states_map[current_set]
            for symbol in self.symbols:
                move_set = self.move(current_set, symbol)
                closure_set = frozenset(self.epsilon_closure(move_set))
                if not closure_set:
                    continue
                if closure_set not in dfa_states_map:
                    dfa_states_map[closure_set] = f"D{state_count}"
                    self.dfa[dfa_states_map[closure_set]] = {}
                    unmarked.append(closure_set)
                    state_count += 1
                self.dfa[current_name][symbol] = dfa_states_map[closure_set]

        # Identify final states
        for nfa_set, dfa_name in dfa_states_map.items():
            if self.nfa_final in nfa_set:
                self.final_states.add(dfa_name)

        return self.dfa, self.start_state, self.final_states


# =======================
# Example usage
# =======================
if __name__ == "__main__":
    from modules.regex_parser import RegexParser
    from modules.nfa_builder import NFABuilder

    regex = "ed+ee+f(ddd+dd+d)*"
    parser = RegexParser(regex)
    parser.validate()
    parser.add_concatenation()
    postfix = parser.to_postfix()

    builder = NFABuilder()
    nfa = builder.build_from_postfix(postfix)

    dfa_builder = DFABuilder(nfa.transitions, nfa.start_state, nfa.final_state)
    dfa_transitions, start_state, final_states = dfa_builder.build_dfa()

    print("DFA Transition Table:")
    for state, paths in dfa_transitions.items():
        print(f"{state}: {paths}")

    print("\nStart State:", start_state)
    print("Final States:", final_states)
