import os

# ---------------- TOKENIZER ---------------- #
def tokenize(expr):
    #Tokenize the input expression into a list of tokens, where each token is a tuple of (type, value).
    tokens = []
    i = 0

    while i < len(expr):
        c = expr[i]
        if c.isdigit() or c == '.': #Check for digits or decimal point to form a number token
            num = c
            i += 1
            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                num += expr[i]
                i += 1
            tokens.append(("NUM", num))
            continue
        elif c in "+-*/": #Check for operators and add them as tokens
            tokens.append(("OP", c))
        elif c == "(": #Check for left parenthesis and add as token
            tokens.append(("LPAREN", c)) 
        elif c == ")": #Check for right parenthesis and add as token
            tokens.append(("RPAREN", c))
        elif c.isspace(): #Skip whitespace characters
            i += 1
            continue
        else:
            raise ValueError("Invalid character")

        i += 1

    tokens.append(("END", ""))
    return tokens

# ---------------- PARSER STATE ---------------- #
# _tokens holds the current token list; _pos is the read cursor.
_tokens = []
_pos = 0
def _current():
    return _tokens[_pos]

def _eat(expected_type=None):
    global _pos
    tok = _current()
    if expected_type and tok[0] != expected_type:
        raise ValueError("Unexpected token")
    _pos += 1
    return tok

def _init_parser(tokens):
    global _tokens, _pos
    _tokens = tokens
    _pos = 0

# ---------------- PARSER FUNCTIONS ---------------- #
def _expression():
    #expression → term ((+ | -) term)*
    left_val, left_tree = _term() #Parse the first term and store its value and tree representation

    while _current()[0] == "OP" and _current()[1] in ("+", "-"): #Check for addition or subtraction operator
        op = _eat()[1]
        right_val, right_tree = _term()
        if op == "+":
            left_val += right_val
        else:
            left_val -= right_val
        left_tree = f"({op} {left_tree} {right_tree})"
    return left_val, left_tree


def _term():
    #term → factor ((* | / | implicit *) factor)*
    left_val, left_tree = _factor()

    while True:
        tok = _current()

        if tok[0] == "OP" and tok[1] in ("*", "/"): #Check for multiplication or division operator
            op = _eat()[1]
            right_val, right_tree = _factor()
            tmp_tree = f"({op} {left_tree} {right_tree})"

            if op == "*":
                left_val *= right_val
            else:
                if right_val == 0:
                    raise ZeroDivisionError(tmp_tree)
                left_val /= right_val

            left_tree = tmp_tree

        elif tok[0] in ("NUM", "LPAREN"): #Check for number or left parenthesis to handle implicit multiplication
            right_val, right_tree = _factor()
            left_val *= right_val
            left_tree = f"(* {left_tree} {right_tree})"

        else:
            break

    return left_val, left_tree


def _factor():
    #factor → NUMBER | (expression) | unary negation
    tok = _current()

    if tok == ("OP", "-"): #Check for unary negation operator
        _eat("OP")
        val, tree = _factor()
        return -val, f"(neg {tree})"

    if tok == ("OP", "+"): #Check for unary plus operator, which is not allowed in this implementation
        raise ValueError("Unary + not allowed")

    if tok[0] == "NUM": #Check for number token, consume it and return its value and string representation
        _eat("NUM")
        return float(tok[1]), tok[1]

    elif tok[0] == "LPAREN": #Check for left parenthesis, consume it, parse the enclosed expression, and consume the right parenthesis
        _eat("LPAREN")
        val, tree = _expression()
        _eat("RPAREN")
        return val, tree

    else:
        raise ValueError("Invalid factor")

# ---------------- FORMATTERS ---------------- #
def format_tokens(tokens):
    #Format the list of tokens into a string representation for output.
    result = []
    for t, v in tokens:
        if t == "END":
            result.append("[END]")
        else:
            result.append(f"[{t}:{v}]")
    return " ".join(result)

def format_result(value):
    #Format the evaluated result for output, rounding to 4 decimal places if necessary and removing trailing zeros.
    if value == int(value):
        return str(int(value))
    return f"{round(value, 4):.4f}".rstrip('0').rstrip('.')

# ---------------- MAIN FUNCTION ---------------- #
def evaluate_file(input_path: str) -> list[dict]:
    #Read expressions from the input file, evaluate them, and write the results to an output file. 
    #Return a list of dictionaries containing the input, tree representation, tokens, and result for each expression.
    results = []

    output_path = os.path.join(os.path.dirname(input_path), "output.txt")

    with open(input_path, "r") as infile, open(output_path, "w") as outfile:
        #Read all lines from the input file and process each expression
        lines = infile.readlines()

        for i, line in enumerate(lines):
            expr = line.rstrip("\n")

            # ---------- Step 1: Tokenization ----------
            try:
                tokens = tokenize(expr)
                token_str = format_tokens(tokens)
            except Exception:
                tokens = None
                token_str = "ERROR"

            # ---------- Step 2: Parsing & Evaluation ----------
            if tokens is not None:
                try:
                    _init_parser(tokens)
                    value, tree = _expression()

                    # Ensure full consumption
                    if _current() != ("END", ""):
                        raise ValueError("Unexpected token")

                    formatted_result = format_result(value)

                except (ValueError, ZeroDivisionError) as e:
                    value = "ERROR"
                    tree = e.args[0]
                    formatted_result = "ERROR"
            else:
                value = "ERROR"
                tree = "ERROR"
                formatted_result = "ERROR"

            # ---------- Write to output file ----------
            outfile.write(f"Input: {expr}\n")
            outfile.write(f"Tree: {tree}\n")
            outfile.write(f"Tokens: {token_str}\n")
            outfile.write(f"Result: {formatted_result}\n")

            if i != len(lines) - 1:
                outfile.write("\n")

            # ---------- Store return structure ----------
            results.append({
                "input": expr,
                "tree": tree,
                "tokens": token_str,
                "result": value
            })

    return results

if __name__ == "__main__":

    # update input_file variable below to test with different input files
    input_file = "sample_input.txt"
    evaluate_file(input_file)