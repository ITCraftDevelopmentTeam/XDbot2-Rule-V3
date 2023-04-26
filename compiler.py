import lexer
from rich import print
import preporcessor
import parser
import visitor
import json

if __name__ == "__main__":
    with open("./helloworld.xr", encoding="utf-8") as f:
        result = visitor.codegen(parser.Parser(lexer.parse(
            preporcessor.prepare(f.read()))).parse())
    print(result)
    json.dump(result, open("./helloworld.xr.json", "w", encoding="utf-8"))

