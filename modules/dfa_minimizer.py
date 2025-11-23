# modules/dfa_minimizer.py

from collections import defaultdict

class DFAMinimizer:
    def __init__(self, dfa_transitions, start_state, final_states):
        """
        Initialize the DFA Minimizer.

        Parameters:
        - dfa_transitions: dict {state: {symbol: next_state}}
        - start_state: DFA start state
        - final_states: list of final states
        """
        self.dfa = dfa_transitions
        self.start_state = start_state
        self.final_states = set(final_states)
        self.states = set(dfa_transitions.keys())
        self.symbols = set()
        for paths in dfa_transitions.values():
            self.symbols.update(paths.keys())

    def minimize(self):
        """Apply Hopcroft's Algorithm to minimize DFA"""
        # Initial partition: final and non-final states
        P = [self.final_states, self.states - self.final_states]
        W = [self.final_states.copy()]  # Worklist

        while W:
            A = W.pop()
            for c in self.symbols:
                # States that go to A on symbol c
                X = set()
                for s in self.states:
                    if c in self.dfa[s] and self.dfa[s][c] in A:
                        X.add(s)
                new_P = []
                for Y in P:
                    inter = Y & X
                    diff = Y - X
                    if inter and diff:
                        new_P.extend([inter, diff])
                        if Y in W:
                            W.remove(Y)
                            W.extend([inter, diff])
                        else:
                            if len(inter) <= len(diff):
                                W.append(inter)
                            else:
                                W.append(diff)
                    else:
                        new_P.append(Y)
                P = new_P

        # Map old states to new representative states
        state_map = {}
        for group in P:
            rep = sorted(group)[0]  # pick smallest name as representative
            for s in group:
                state_map[s] = rep

        # Build minimized DFA
        minimized = {}
        for old_state in self.dfa:
            rep = state_map[old_state]
            if rep not in minimized:
                minimized[rep] = {}
            for symbol, dest in self.dfa[old_state].items():
                minimized[rep][symbol] = state_map[dest]

        minimized_start = state_map[self.start_state]
        minimized_final = set(state_map[s] for s in self.final_states)

        return minimized, minimized_start, minimized_final


# =======================
# Example usage
# =======================
if __name__ == "__main__":
    # Example DFA
    dfa_transitions = {
        'q0': {'a': 'q1', 'b': 'q0'},
        'q1': {'a': 'q1', 'b': 'q2'},
        'q2': {'a': 'q1', 'b': 'q0'}
    }
    start_state = 'q0'
    final_states = ['q2']

    print("Original DFA Transition Table:")
    for s, paths in dfa_transitions.items():
        print(f"{s}: {paths}")

    minimizer = DFAMinimizer(dfa_transitions, start_state, final_states)
    min_dfa, min_start, min_final = minimizer.minimize()

    print("\nMinimized DFA Transition Table:")
    for s, paths in min_dfa.items():
        print(f"{s}: {paths}")

    print("\nStart State:", min_start)
    print("Final States:", min_final)
