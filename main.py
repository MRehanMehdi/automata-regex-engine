# main.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QTextEdit, QVBoxLayout, QHBoxLayout, QGroupBox, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from modules.regex_parser import RegexParser
from modules.nfa_builder import NFABuilder
from modules.dfa_builder import DFABuilder
from modules.dfa_minimizer import DFAMinimizer
from modules.visualizer import Visualizer
from modules.simulator import Simulator


class TOAGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Theory of Automata Project")
        self.setGeometry(100, 100, 950, 750)
        self.init_ui()

    def init_ui(self):
        # -------------------------
        # Fonts
        # -------------------------
        label_font = QFont("Arial", 11, QFont.Bold)
        input_font = QFont("Arial", 10)
        button_font = QFont("Arial", 10, QFont.Bold)

        # -------------------------
        # Labels and Inputs
        # -------------------------
        self.regex_label = QLabel("Enter Regular Expression:")
        self.regex_label.setFont(label_font)
        self.regex_input = QLineEdit()
        self.regex_input.setFont(input_font)
        self.regex_input.setPlaceholderText("Example: (ed+ee+f(ddd+dd+d)*)")

        self.string_label = QLabel("Enter Test String:")
        self.string_label.setFont(label_font)
        self.string_input = QLineEdit()
        self.string_input.setFont(input_font)
        self.string_input.setPlaceholderText("Type string to simulate on DFA")

        # -------------------------
        # Buttons
        # -------------------------
        self.build_nfa_button = QPushButton("Build NFA")
        self.build_nfa_button.setFont(button_font)
        self.build_nfa_button.setToolTip("Click to build NFA from regex")
        self.build_nfa_button.clicked.connect(self.build_nfa)

        self.build_dfa_button = QPushButton("Build DFA")
        self.build_dfa_button.setFont(button_font)
        self.build_dfa_button.setToolTip("Click to build DFA from NFA")
        self.build_dfa_button.clicked.connect(self.build_dfa)

        self.build_min_dfa_button = QPushButton("Build Minimized DFA")
        self.build_min_dfa_button.setFont(button_font)
        self.build_min_dfa_button.setToolTip("Click to minimize DFA")
        self.build_min_dfa_button.clicked.connect(self.build_min_dfa)

        self.simulate_button = QPushButton("Simulate String")
        self.simulate_button.setFont(button_font)
        self.simulate_button.setToolTip("Simulate string on minimized DFA")
        self.simulate_button.clicked.connect(self.simulate_string)

        # -------------------------
        # Group Boxes for clarity
        # -------------------------
        regex_group = QGroupBox("Regular Expression Input")
        regex_layout = QVBoxLayout()
        regex_layout.addWidget(self.regex_label)
        regex_layout.addWidget(self.regex_input)
        regex_group.setLayout(regex_layout)

        buttons_group = QGroupBox("Automata Operations")
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.build_nfa_button)
        buttons_layout.addWidget(self.build_dfa_button)
        buttons_layout.addWidget(self.build_min_dfa_button)
        buttons_group.setLayout(buttons_layout)

        simulate_group = QGroupBox("String Simulation")
        simulate_layout = QVBoxLayout()
        simulate_layout.addWidget(self.string_label)
        simulate_layout.addWidget(self.string_input)
        simulate_layout.addWidget(self.simulate_button)
        simulate_group.setLayout(simulate_layout)

        # -------------------------
        # Output Display
        # -------------------------
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        self.output_display.setFont(QFont("Courier New", 10))
        self.output_display.setStyleSheet("background-color: #f5f5f5;")

        # -------------------------
        # Main Layout
        # -------------------------
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        main_layout.addWidget(regex_group)
        main_layout.addWidget(buttons_group)
        main_layout.addWidget(simulate_group)
        main_layout.addWidget(QLabel("Output:"))
        main_layout.addWidget(self.output_display)
        self.setLayout(main_layout)

        # -------------------------
        # Automata placeholders
        # -------------------------
        self.nfa = None
        self.dfa_transitions = None
        self.dfa_start = None
        self.dfa_finals = None
        self.min_dfa_transitions = None
        self.min_dfa_start = None
        self.min_dfa_finals = None

    # -------------------------
    # Helper function to display transition tables in GUI
    # -------------------------
    def display_transition_table(self, transitions, name):
        table_str = f"=== {name} ===\n"
        for state, trans in transitions.items():
            table_str += f"{state}: {trans}\n"
        table_str += "=" * 30 + "\n"
        self.output_display.append(f"<pre>{table_str}</pre>")

    # -------------------------
    # Build NFA
    # -------------------------
    def build_nfa(self):
        regex = self.regex_input.text()
        try:
            parser = RegexParser(regex)
            parser.validate()
            parser.add_concatenation()
            postfix = parser.to_postfix()
            self.output_display.append(f"<b>Postfix Expression:</b> {postfix}\n")

            nfa_builder = NFABuilder()
            self.nfa = nfa_builder.build_from_postfix(postfix)
            self.display_transition_table(self.nfa.transitions, "NFA Table")
            self.output_display.append("NFA built successfully.\n")

            Visualizer(
                transitions=self.nfa.transitions,
                start_state=self.nfa.start_state,
                final_states=[self.nfa.final_state],
                title="NFA Diagram"
            ).draw()

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    # -------------------------
    # Build DFA
    # -------------------------
    def build_dfa(self):
        if not self.nfa:
            QMessageBox.warning(self, "Error", "Build NFA first!")
            return
        try:
            dfa_builder = DFABuilder(self.nfa.transitions, self.nfa.start_state, self.nfa.final_state)
            self.dfa_transitions, self.dfa_start, self.dfa_finals = dfa_builder.build_dfa()
            self.display_transition_table(self.dfa_transitions, "DFA Table")
            self.output_display.append("DFA built successfully.\n")

            Visualizer(
                transitions=self.dfa_transitions,
                start_state=self.dfa_start,
                final_states=self.dfa_finals,
                title="DFA Diagram"
            ).draw()

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    # -------------------------
    # Build Minimized DFA
    # -------------------------
    def build_min_dfa(self):
        if not self.dfa_transitions:
            QMessageBox.warning(self, "Error", "Build DFA first!")
            return
        try:
            minimizer = DFAMinimizer(self.dfa_transitions, self.dfa_start, self.dfa_finals)
            self.min_dfa_transitions, self.min_dfa_start, self.min_dfa_finals = minimizer.minimize()
            self.display_transition_table(self.min_dfa_transitions, "Minimized DFA Table")
            self.output_display.append("DFA Minimization completed.\n")

            Visualizer(
                transitions=self.min_dfa_transitions,
                start_state=self.min_dfa_start,
                final_states=self.min_dfa_finals,
                title="Minimized DFA Diagram"
            ).draw()

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    # -------------------------
    # Simulate string (with colors)
    # -------------------------
    def simulate_string(self):
        input_string = self.string_input.text()
        if not self.min_dfa_transitions:
            QMessageBox.warning(self, "Error", "Please build the automata first!")
            return

        simulator = Simulator(self.min_dfa_transitions, self.min_dfa_start, self.min_dfa_finals)
        try:
            steps, accepted = simulator.simulate(input_string)
            self.output_display.append('<b>String Simulation Steps:</b>')

            for current, symbol, next_state in steps:
                if next_state is None:
                    # Invalid transition - red
                    self.output_display.append(
                        f'<span style="color:red;">{current} --{symbol}--> None (Invalid transition)</span>'
                    )
                elif next_state in self.min_dfa_finals and len(steps) == steps.index((current, symbol, next_state)) + 1:
                    # Last step ends in final state - green
                    self.output_display.append(
                        f'<span style="color:green;">{current} --{symbol}--> {next_state}</span>'
                    )
                else:
                    # Normal transition - blue
                    self.output_display.append(
                        f'<span style="color:blue;">{current} --{symbol}--> {next_state}</span>'
                    )

            # Final result
            result_color = "green" if accepted else "red"
            self.output_display.append(
                f'\n<b>String Result: <span style="color:{result_color};">'
                f'{"Accepted" if accepted else "Rejected"}</span></b>\n'
            )

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))


# =======================
# Run the GUI
# =======================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TOAGUI()
    window.show()
    sys.exit(app.exec_())
