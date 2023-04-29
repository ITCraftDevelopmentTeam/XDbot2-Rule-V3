import json5
# import lexer

ENDS = {
    "op": "end",
    "lpar": "rpar",
    "lsqd": "rsqd"
}
IGNORE_TOKENS = [
    "at"
]


class Parser:
    def __init__(self, tokens, is_splited=False) -> None:
        self.tokens = tokens
        self.now_token = -1
        if not is_splited:
            self.spliter()
            # print(self.tokens)

    def token(self) -> tuple | None:
        if self.now_token >= self.tokens.__len__():
            return None
        return self.tokens[self.now_token]

    def next(self) -> tuple | None:
        self.now_token += 1
        return self.token()

    def token_type(self) -> str:
        # print(self.token())
        return self.token()[1]

    def parse(self) -> list | None:
        self.ast = []
        ast = {"type": None, "args": []}
        while self.next():
            if isinstance(self.token(), list):
                ast["args"].append(Parser(self.token(), True).parse())
            elif self.token_type() == "op":
                ast["args"].append(Parser(self.next(), True).parse())
            elif self.token_type() == "eol":
                if ast["type"] is not None:
                    self.ast.append(ast.copy())
                ast = {"type": None, "args": []}
            elif self.token_type() == "name" and ast["type"] is None\
                    or self.token_type() == "expr":
                ast["type"] = "call"
                ast["func"] = self.token_value()
            elif self.token_type() == "keyword":
                ast.update(self.parse_keyword())
            elif self.token_type() == "var":
                ast["args"].append([{
                    "type": "call",
                    "func": "*get_value",
                    "args": [self.token_value()]
                }])
            elif self.token_type() == "dot":
                ast["func"] = [{
                    "type": "call",
                    "func": "*get",
                    "args": [self.next()[0], ast["func"]]
                }]
            else:
                if self.token_type() in ["int", "string"]:
                    ast["args"].append(json5.loads(self.token_value()))
                else:
                    ast["args"].append({
                        "type": "call",
                        "func": "*get",
                        "args": [self.token_value()]
                    })
        if ast["type"] is not None:
            self.ast.append(ast)
        elif self.ast == [] and ast["args"] != []:
            return ast["args"]
        return self.ast

    def token_value(self) -> str:
        return self.token()[0]

    def parse_keyword(self) -> dict:
        ast = {}
        ast["type"] = self.token_value().replace(":", "")
        if self.token_value() in ["let", "var", "const"]:
            ast["type"] = "var"
            ast["var_type"] = self.token_value()
            ast["name"] = self.next()[0]
            try:
                ast["value"] = [
                    Parser(self.tokens[self.now_token + 1:], True).parse()[0]]
                while self.next()[1] != "eol":
                    pass
                self.now_token -= 1
            except BaseException:
                pass
        elif self.token_value() == "del":
            ast["var"] = []
            while self.next() == "eol":
                if self.token_type() == "name":
                    ast["var"].append(self.token_value())

            self.now_token -= 1
        return ast

    def spliter(self, ret: bool = False, end: str = "") -> list | None:
        tokens = []
        while self.next():
            if self.token_type() not in IGNORE_TOKENS:
                tokens.append(self.token())
            if self.token_type() in ENDS.keys():
                if tokens[-1][1] != "op":
                    tokens.pop(-1)
                tokens.append(self.spliter(True, ENDS[self.token_type()]))
            elif self.token_type() == end and ret:
                break
        if not ret:
            self.now_token = -1
            self.tokens = tokens
        else:
            return tokens[:-1]
