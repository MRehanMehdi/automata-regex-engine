# utils/helpers.py

def print_transition_table(transitions, title="Transition Table"):
    """
    Nicely print the transition table.

    Parameters:
    - transitions: dict {state: {symbol: next_state(s)}}
    - title: str, title to display
    """
    print(f"\n=== {title} ===")
    for state, paths in transitions.items():
        formatted_paths = {}
        for symbol, dest in paths.items():
            if isinstance(dest, (list, set)):
                formatted_paths[symbol] = ",".join(sorted(dest))
            else:
                formatted_paths[symbol] = dest
        print(f"{state}: {formatted_paths}")
    print("=" * (len(title) + 10))


def format_state_set(state_set):
    """
    Convert a set of states into a readable string for DFA states.
    Example: {'q1', 'q2'} -> 'q1,q2'
    """
    return ",".join(sorted(state_set))


def highlight_start_final(state, start_state, final_states):
    """
    Return a string highlighting start and final states.

    Example:
    - Start state -> green or with arrow
    - Final state -> marked with *
    """
    if state == start_state:
        return f"-> {state}"  # start state indicator
    elif state in final_states:
        return f"*{state}"  # final state indicator
    else:
        return state


def flatten_list(nested_list):
    """
    Flatten a nested list into a single list.
    Example: [[1,2],[3,4]] -> [1,2,3,4]
    """
    return [item for sublist in nested_list for item in sublist]


def validate_input_string(input_string, allowed_symbols):
    """
    Validate input string against allowed DFA symbols.
    Returns True if valid, False otherwise.
    """
    for char in input_string:
        if char not in allowed_symbols:
            return False
    return True


# =======================
# Example usage
# =======================
if __name__ == "__main__":
    sample_dfa = {
        'D0': {'a': 'D1', 'b': 'D0'},
        'D1': {'a': 'D1', 'b': 'D2'},
        'D2': {'a': 'D1', 'b': 'D0'}
    }
    print_transition_table(sample_dfa, "Sample DFA")

    states_set = {'q1', 'q2', 'q0'}
    print("Formatted state set:", format_state_set(states_set))

    print(highlight_start_final('D0', 'D0', {'D2'}))  # -> D0
    print(highlight_start_final('D2', 'D0', {'D2'}))  # *D2

    print("Flatten nested list:", flatten_list([[1, 2], [3, 4]]))
    print("Validate input 'ab':", validate_input_string("ab", {'a', 'b'}))
    print("Validate input 'abc':", validate_input_string("abc", {'a', 'b'}))
