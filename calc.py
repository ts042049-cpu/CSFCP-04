# simple_add_sub_mul_calculator.py
import sys

def evaluate_term(term):
    """Evaluate a term that may include multiplication (*) but no + or -."""
    parts = term.split('*')
    result = 1.0
    for p in parts:
        if p.strip() == '':
            raise ValueError("Invalid use of '*' operator.")
        result *= float(p)
    return result

def compute_expr(expr: str):
    """Compute an expression containing +, -, * without using eval."""
    s = expr.replace(' ', '')
    if not s:
        raise ValueError("Empty expression")

    # Normalize unary + and - signs
    i = 0
    tokens = []
    current = ''
    sign = 1

    # Convert expression into a list of signed terms
    while i < len(s):
        ch = s[i]

        if ch in '+-':
            if current == '':
                # unary + or -
                sign *= -1 if ch == '-' else 1
            else:
                # end of a term
                tokens.append((sign, current))
                current = ''
                sign = -1 if ch == '-' else 1
            i += 1

        else:
            current += ch
            i += 1

    # add last term
    if current == '':
        raise ValueError("Expression ends with an operator.")
    tokens.append((sign, current))

    total = 0.0

    # Evaluate each term (handle multiplication inside)
    for sign, term in tokens:
        total += sign * evaluate_term(term)

    # Return int if whole number
    if abs(total - int(total)) < 1e-12:
        return int(total)
    return total


def repl():
    print("Basic + / - / * calculator. Type 'q' or 'quit' to exit.")
    while True:
        try:
            expr = input("Enter expression: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if expr.lower() in ('q', 'quit', 'exit'):
            print("Bye.")
            break

        if not expr:
            continue

        try:
            result = compute_expr(expr)
            print("=", result)
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        expr = " ".join(sys.argv[1:])
        try:
            print(compute_expr(expr))
        except Exception as e:
            print("Error:", e)
    else:
        repl()
