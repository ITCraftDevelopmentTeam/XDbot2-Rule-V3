import re

KEYWORDS = [
    #    "use",
    #    "match",
    #    "rule",
    #    "on",
    "const",
    "var",
    "let",
    #    "del",
    "eval:",
    "lua",
    #    "config"
]

EXPRS = [
    r"\+\+",
    "<=",
    ">=",
    "==",
    ">",
    "<",
    "=",
    r"\+",
    "-",
    r"\*",
    r"\/"
]

TYPES = {
    "keyword": "|".join(KEYWORDS),
    "string": r"(\"(\\.|[^\"])*\")|('(\\.|[^'])*')",
    "end": "end|finish|fi",
    "at": "@",
    "dot": r"\.",
    "var": r"\$([\u4E00-\u9FA5AA-Za-z0-9_:]+)",
    "int": "-?([1-9][0-9]*|0x[0-9a-f]+|0b[0-1]+|0o[0-8]+)",
    "indent": "^( |\t)+",
    "space": "( |\t)+",
    "lpar": "\\(",
    "rpar": "\\)",
    "lsqb": "\\[",
    "rsqb": "\\]",
    "eol": ";",
    "op": ":",
    "expr": "|".join(EXPRS),
    "comment": r"(/\*(.*)\*/)|(//.*$)",
    "newline": "\n",
    "comma": ",",
    "name": r"[\u4E00-\u9FA5AA-Za-z0-9_:]+",  # r"[^'\"\\\(\) \n\t;:\.]+",
    "unknown": "(.+)"
}


def parse(src_code: str, ignore_token: bool = True) -> list:
    result: list = []
    token_regex = ""
    for key in list(TYPES.keys()):
        token_regex += "(?P<%s>%s)|" % (key, TYPES[key])
    callable_iterato = re.finditer(token_regex[:-1], src_code)
    for mo in callable_iterato:
        if mo.lastgroup == "unknown":
            print(f"WARN! Unknown token: {mo}")
            continue
        if mo.lastgroup in ["space", "null_char", "comment", "newline"]\
                and ignore_token:
            continue
        result.append((mo[0], mo.lastgroup))
    return result
