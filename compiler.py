import lexer
from rich import print
import preporcessor
import parser
import visitor
import json

def compile(file, out):
    with open(file, encoding="utf-8") as f:
        result = visitor.codegen(parser.Parser(lexer.parse(
            preporcessor.prepare(f.read()))).parse())
    print(result)
    json.dump(result, open(out, "w", encoding="utf-8"))

if __name__ == "__main__":
    import sys
    compile(sys.argv[1], sys.argv[2])
