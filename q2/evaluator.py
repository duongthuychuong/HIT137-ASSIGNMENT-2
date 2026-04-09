import os

def tokenize(expression):
    tokens = []
    i = 0
    while i < len(expression):
        char = expression[i]
        if char.isspace():
            i += 1
            continue
        if char.isdigit() or char == '.':
            num = ""
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                num += expression[i]
                i += 1
            tokens.append(("NUM", num))
            continue
        if char in "+-*/":
            tokens.append(("OP", char))
        elif char == '(':
            tokens.append(("LPAREN", "("))
        elif char == ')':
            tokens.append(("RPAREN", ")"))
        else:
            return None  # Invalid character error
        i += 1
    tokens.append(("END", "END"))
    return tokens

def format_result(val):
    if val == "ERROR": return "ERROR"
    if val == int(val):
        return str(int(val))
    return f"{round(float(val), 4):.4f}".rstrip('0').rstrip('.')

def evaluate_file(input_path):
    results = []
    
    with open(input_path, 'r') as f:
        lines = f.readlines()

    output_lines = []
    for line in lines:
        raw_input = line.strip()
        if not raw_input: continue
        
        tokens = tokenize(raw_input)
        
        # State management for recursive descent
        pos = 0
        error_flag = False

        def get_token():
            nonlocal pos
            return tokens[pos] if tokens and pos < len(tokens) else ("END", "END")

        def match(expected_type=None, expected_val=None):
            nonlocal pos, error_flag
            token = get_token()
            if error_flag: return False
            if (expected_type and token[0] == expected_type) or (expected_val and token[1] == expected_val):
                pos += 1
                return True
            return False

        def parse_expression():
            nonlocal error_flag
            tree_l, val_l = parse_term()
            while get_token()[1] in ('+', '-'):
                op = get_token()[1]
                match()
                tree_r, val_r = parse_term()
                if error_flag: break
                tree_l = f"({op} {tree_l} {tree_r})"
                val_l = (val_l + val_r) if op == '+' else (val_l - val_r)
            return tree_l, val_l

        def parse_term():
            nonlocal error_flag
            tree_l, val_l = parse_factor()
            # Handle standard *, / and implicit multiplication
            while True:
                token = get_token()
                if token[1] in ('*', '/'):
                    op = token[1]
                    match()
                    tree_r, val_r = parse_factor()
                    if error_flag: break
                    if op == '/' and val_r == 0: 
                        error_flag = True
                        break
                    tree_l = f"({op} {tree_l} {tree_r})"
                    val_l = (val_l * val_r) if op == '*' else (val_l / val_r)
                # Implicit multiplication: next is NUM or LPAREN
                elif token[0] in ('NUM', 'LPAREN'):
                    tree_r, val_r = parse_factor()
                    if error_flag: break
                    tree_l = f"(* {tree_l} {tree_r})"
                    val_l *= val_r
                else:
                    break
            return tree_l, val_l

        def parse_factor():
            nonlocal error_flag
            if match(expected_val='-'):
                tree, val = parse_factor()
                return f"(neg {tree})", -val
            elif get_token()[1] == '+':
                error_flag = True # Unary + not supported
                return "ERROR", 0
            return parse_primary()

        def parse_primary():
            nonlocal error_flag
            token = get_token()
            if match(expected_type='NUM'):
                return str(format_result(float(token[1]))), float(token[1])
            elif match(expected_type='LPAREN'):
                tree, val = parse_expression()
                if not match(expected_type='RPAREN'): error_flag = True
                return tree, val
            error_flag = True
            return "ERROR", 0

        # Run Parsing
        try:
            if tokens is None: raise Exception("Lexer Error")
            tree_final, result_final = parse_expression()
            if pos < len(tokens) - 1: error_flag = True # Leftover tokens
        except:
            error_flag = True

        # Formatting Output
        if error_flag:
            res_dict = {"input": raw_input, "tree": "ERROR", "tokens": "ERROR", "result": "ERROR"}
        else:
            token_str = " ".join([f"[{t[0]}:{t[1]}]" for t in tokens if t[0] != "END"]) + " [END]"
            res_dict = {
                "input": raw_input, 
                "tree": tree_final, 
                "tokens": token_str, 
                "result": float(result_final)
            }
        
        results.append(res_dict)
        
        # Build output.txt format
        output_lines.append(f"Input: {res_dict['input']}")
        output_lines.append(f"Tree: {res_dict['tree']}")
        output_lines.append(f"Tokens: {res_dict['tokens']}")
        output_lines.append(f"Result: {format_result(res_dict['result'])}")
        output_lines.append("")

    # Write to file
    output_path = os.path.join(os.path.dirname(input_path), "output.txt")
    with open(output_path, 'w') as f:
        f.write("\n".join(output_lines).strip() + "\n")
        
    return results