import lexer
from rich import print
import preporcessor
import parser

if __name__ == "__main__":
    with open("./helloworld.xr", encoding="utf-8") as f:
        result = parser.Parser(lexer.parse(preporcessor.prepare(f.read()))).parse()
    print(result)
