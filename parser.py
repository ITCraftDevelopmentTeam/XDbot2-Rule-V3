import json
import lexer

class Parser:
    def __init__(self, tokens, is_splited = False) -> None:
        self.tokens = tokens
        self.now_token = -1
        if not is_splited:
            self.spliter()

    def token(self) -> tuple | None:
        if self.now_token >= self.tokens.__len__():
            return None
        return self.tokens[self.now_token] #if self.tokens[self.now_token] else self.next()
    
    def next(self) -> tuple | None:
        self.now_token += 1
        return self.token()

    def token_type(self) -> str:
        return self.token()[1]

    def parse(self) -> list | None:
        self.ast = []
        ast = {"type":None, "args": []}
        while self.next():
            if self.token_type() == "op":
                ast["args"].append(Parser(self.next(), True).parse())
            elif self.token_type() == "eol":
                self.ast.append(ast.copy())
                ast = {"type":None, "args": []}
            elif self.token_type() == "name" and ast["type"] == None:
                ast["type"] = "call"
                ast["func"] = self.token_value()
            elif self.token_type() == "keyword":
                ast["type"] = self.token_value()
            elif self.token_type() in ["string", "int"]:
                ast["args"].append(json.loads(self.token_value()))
        if ast["type"] != None:
            self.ast.append(ast)
        return self.ast

    def token_value(self) -> str:
        return self.token()[0]

    def spliter(self, ret: bool = False) -> list | None:
        tokens = []
        while self.next():
            tokens.append(self.token())
            if self.token_type() == "op":
                tokens.append(self.spliter(True))
            elif self.token_type() == "end" and ret:
                break
        if not ret:
            self.now_token = -1
            self.tokens = tokens
        else:
            return tokens




