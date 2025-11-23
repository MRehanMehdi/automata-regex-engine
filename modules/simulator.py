# modules/simulator.py

class Simulator:
    """
    DFA Simulator class.
    Simulates DFA behavior on a given input string.
    """

    def __init__(self, dfa_transitions, start_state, final_states):
        """
        Initialize the simulator with DFA.

        Parameters:
        - dfa_transitions: dict {state: {symbol: next_state}}
        - start_state: starting state of DFA
        - final_states: list of final states
        """
        self.dfa = dfa_transitions
        self.start_state = start_state
        self.final_states = final_states

    def simulate(self, input_string):
        """
        Simulate the DFA on input string.

        Parameters:
        - input_string: string to simulate on DFA

        Returns:
        - transitions_list: list of tuples (current_state, symbol, next_state)
        - accepted: boolean indicating if string is accepted
        """
        current_state = self.start_state
        transitions_list = []

        for symbol in input_string:
            if symbol not in self.dfa[current_state]:
                # Invalid symbol or missing transition
                transitions_list.append((current_state, symbol, None))
                return transitions_list, False
            next_state = self.dfa[current_state][symbol]
            transitions_list.append((current_state, symbol, next_state))
            current_state = next_state

        accepted = current_state in self.final_states
        return transitions_list, accepted


# =======================
# Example usage / testing
# =======================
if __name__ == "__main__":
    # Example DFA transition table
    dfa_transitions = {
        'q0': {'a': 'q1', 'b': 'q0'},
        'q1': {'a': 'q1', 'b': 'q2'},
        'q2': {'a': 'q1', 'b': 'q0'}
    }
    start_state = 'q0'
    final_states = ['q2']

    simulator = Simulator(dfa_transitions, start_state, final_states)

    test_string = "aabb"
    transitions, accepted = simulator.simulate(test_string)

    print("Simulation Steps:")
    for current, symbol, next_state in transitions:
        if next_state is not None:
            print(f"{current} --{symbol}--> {next_state}")
        else:
            print(f"{current} --{symbol}--> None (Invalid transition)")

    print("\nString Result:", "Accepted" if accepted else "Rejected")
