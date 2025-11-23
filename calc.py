# simple_add_sub_mul_div_calculator.py
import sys

def evaluate_term(term):
    """Evaluate a term that may include * and / operators but no + or -."""
    # Split by * and / but keep operators
    parts = []
    num = ''
    for ch in term:
        if ch in '*/':
            parts.append(num)
            parts.append(ch)
            num = ''
        else:
            num += ch
    parts.append(num)

    # Now evaluate left-to-right
    result = float(parts[0])

    i = 1
    while i < len(parts):
        op = parts[i]
        val = float(parts[i+1])

        if op == '*':
            result *= val
        elif op == '/':
            if val == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            result /= val

        i += 2

    return result


def compute_expr(expr: str):
    """Compute an expression containing +, -, *, / without using eval."""
    s = expr.replace(' ', '')
    if not s:
        raise ValueError("Empty expression")

    i = 0
    tokens = []
    current = ''
    sign = 1

    # Convert into list of signed terms
    while i < len(s):
        ch = s[i]

        if ch in '+-':
            if current == '':
                sign *= -1 if ch == '-' else 1  # unary
            else:
                tokens.append((sign, current))
                current = ''
                sign = -1 if ch == '-' else 1
            i += 1
        else:
            current += ch
            i += 1

    if current == '':
        raise ValueError("Expression ends with an operator.")
    tokens.append((sign, current))

    total = 0.0

    # Evaluate each * / term
    for sign, term in tokens:
        total += sign * evaluate_term(term)

    if abs(total - int(total)) < 1e-12:
        return int(total)
    return total


def repl():
    print("Basic + / - / * / ÷ calculator. Type 'q' or 'quit' to exit.")
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
