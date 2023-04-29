from . import lexer


def tokens2code(tokens):
    buf = ""
    for token in tokens:
        buf += token[0]
    return buf


def prepare(src_code):
    tokens = lexer.parse(src_code, False)
    token_length = 0
    bracket_depth = 0
    line_tokens = 0
    starts_with_at = False
    for token in tokens.copy():
        if token[1] in ["lsqb", "lpar"]:
            bracket_depth += 1
        elif token[1] in ["rsqb", "rpar"]:
            bracket_depth -= 1
        elif token[1] == "at":
            starts_with_at = True
        if token[1] == "newline" and\
                bracket_depth == 0 and\
                line_tokens > 0 and\
                tokens[token_length - 1][1] not in ["op", "eol"]:
            tokens.insert(
                token_length,
                (";", "eol") if not starts_with_at else (":", "op"))
            starts_with_at = False
            token_length += 1
            line_tokens = 0
        elif token[1] in ["newline", "op", "eol"]:
            starts_with_at = False
            line_tokens = 0
        else:
            line_tokens += 1
        token_length += 1
    return tokens2code(tokens)
