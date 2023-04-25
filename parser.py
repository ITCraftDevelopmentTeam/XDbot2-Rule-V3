import lexer

class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.now_token = -1

    def token(self) -> tuple | None:
        if self.now_token >= self.tokens.__len__():
            return None
        return self.tokens[self.now_token]
    
    def next(self) -> tuple | None:
        self.now_token += 1
        return self.token()

    def parse(self) -> list | None:
        return self.spliter()

    def spliter(self) -> list:
        tokens = []
        while self.next():
            tokens.append(self.token())
            if self.token()[1] == "op":
                tokens.append(self.spliter())
        return tokens



