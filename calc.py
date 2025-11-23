# simple_add_sub_calculator.py
import sys

def compute_add_sub(expr: str):
    """Compute an expression containing only + and - and numbers (ints or floats)."""
    s = expr.replace(' ', '')
    if not s:
        raise ValueError("Empty expression")

    total = 0.0
    i = 0
    sign = 1           # sign to apply to the next number
    num_str = ''       # collects digits and decimal point
    expect_number = True  # if True, unary + / - are allowed; otherwise + / - is a binary operator

    while i < len(s):
        ch = s[i]
        if ch in '+-':
            if expect_number:
                # treat as unary sign (allow chain of + / -)
                sign = sign * (-1 if ch == '-' else 1)
                i += 1
            else:
                # binary operator -> flush current number, then set sign for next number
                if num_str == '':
                    raise ValueError(f"Operator at unexpected place near index {i}: '{s}'")
                total += sign * float(num_str)
                num_str = ''
                sign = 1 if ch == '+' else -1
                expect_number = True
                i += 1
        elif ch.isdigit() or ch == '.':
            expect_number = False
            num_str += ch
            i += 1
        else:
            raise ValueError(f"Invalid character '{ch}' in expression. Only digits, '.' and '+'/'-' allowed.")

    # after loop, flush last number
    if num_str == '':
        raise ValueError("Expression ends with an operator or is malformed.")
    total += sign * float(num_str)

    # Return int when result is whole number, else float
    if abs(total - int(total)) < 1e-12:
        return int(total)
    return total

def repl():
    print("Basic + / - calculator. Type 'q' or 'quit' to exit.")
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
            result = compute_add_sub(expr)
            print("=", result)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # allow compute from command line: python simple_add_sub_calculator.py "5+3-2"
        expr = " ".join(sys.argv[1:])
        try:
            print(compute_add_sub(expr))
        except Exception as e:
            print("Error:", e)
    else:
        repl()
