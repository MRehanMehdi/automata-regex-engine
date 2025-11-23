# modules/visualizer.py

import networkx as nx
import matplotlib.pyplot as plt


class Visualizer:
    def __init__(self, transitions, start_state, final_states, title="Automaton"):
        """
        Initialize the visualizer.

        Parameters:
        - transitions: dict {state: {symbol: [next_states]}} for NFA or DFA
        - start_state: starting state string
        - final_states: list of final states
        - title: title of the graph
        """
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states
        self.title = title

    def draw(self):
        """
        Draw the automaton graph using matplotlib and networkx.
        Applies HCI-friendly layout and styling.
        """
        G = nx.DiGraph()

        # Add edges
        for state, paths in self.transitions.items():
            for symbol, dest_states in paths.items():
                if isinstance(dest_states, list):
                    for dest in dest_states:
                        G.add_edge(state, dest, label=symbol)
                else:
                    G.add_edge(state, dest_states, label=symbol)

        # HCI-friendly layout using shell_layout for clarity
        layers = [self.start_state] + [s for s in G.nodes() if s != self.start_state]
        pos = nx.shell_layout(G, nlist=[layers])  # clear separation

        # Node colors
        node_colors = []
        for node in G.nodes():
            if node == self.start_state:
                node_colors.append("#7CFC00")  # bright green for start
            elif node in self.final_states:
                node_colors.append("#87CEEB")  # skyblue for final
            else:
                node_colors.append("#FFFFFF")  # white for normal

        # Draw nodes
        nx.draw_networkx_nodes(
            G, pos,
            node_size=2000,
            node_color=node_colors,
            edgecolors="black",
            linewidths=2
        )

        # Draw node labels
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")

        # Draw edges
        nx.draw_networkx_edges(
            G, pos,
            arrowstyle="->",
            arrowsize=20,
            connectionstyle="arc3,rad=0.2",
            edge_color="black",
            width=2
        )

        # Draw edge labels
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(
            G, pos,
            edge_labels=edge_labels,
            font_color='red',
            font_size=10,
            label_pos=0.5
        )

        plt.title(self.title, fontsize=16, fontweight="bold")
        plt.axis("off")
        plt.tight_layout()
        plt.show()


# =======================
# Example usage
# =======================
if __name__ == "__main__":
    nfa_transitions = {
        'q0': {'ε': ['q1', 'q2']},
        'q1': {'a': ['q1']},
        'q2': {'b': ['q2']},
        'q3': {}
    }
    start_state = 'q0'
    final_states = ['q3']

    visualizer = Visualizer(nfa_transitions, start_state, final_states, title="Example NFA")
    visualizer.draw()
