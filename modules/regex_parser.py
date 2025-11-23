# modules/regex_parser.py

class RegexParser:
    def __init__(self, regex):
        self.regex = regex.replace(" ", "")  # Remove spaces
        self.postfix = ""

    def validate(self):
        """Validate the regex for unmatched parentheses and invalid operators."""
        stack = []
        prev_char = ""
        for i, char in enumerate(self.regex):
            if char == "(":
                stack.append(i)
            elif char == ")":
                if not stack:
                    raise ValueError(f"Error: Unmatched ')' at position {i}")
                stack.pop()
            elif char in "+*":
                if prev_char in "+*(" or prev_char == "":
                    raise ValueError(f"Error: Invalid operator '{char}' at position {i}")
            prev_char = char
        if stack:
            raise ValueError(f"Error: Unmatched '(' at position {stack.pop()}")

    def add_concatenation(self):
        """Add explicit concatenation operator '.' for Thompson's construction"""
        result = ""
        operators = set("()+*")
        prev = ""
        for char in self.regex:
            if prev and (prev not in operators or prev == ")" or prev == "*") and (char not in operators or char == "("):
                result += "."
            result += char
            prev = char
        self.regex = result

    def to_postfix(self):
        """Convert infix regex to postfix using Shunting Yard algorithm"""
        precedence = {'*': 3, '.': 2, '+': 1}
        output = ""
        stack = []
        for char in self.regex:
            if char.isalnum():  # Operand
                output += char
            elif char == "(":
                stack.append(char)
            elif char == ")":
                while stack and stack[-1] != "(":
                    output += stack.pop()
                stack.pop()  # Remove '('
            else:  # Operator
                while stack and stack[-1] != "(" and precedence[stack[-1]] >= precedence[char]:
                    output += stack.pop()
                stack.append(char)
        while stack:
            output += stack.pop()
        self.postfix = output
        return self.postfix


# =======================
# Example usage
# =======================
if __name__ == "__main__":
    regex = "ed+ee+f(ddd+dd+d)*"
    parser = RegexParser(regex)
    try:
        parser.validate()
        parser.add_concatenation()
        postfix = parser.to_postfix()
        print("Cleaned Regex:", parser.regex)
        print("Postfix:", postfix)
    except ValueError as e:
        print(e)
