from . import lexer
from . import preporcessor
from . import parser
from . import visitor
import json

def compile(file, out):
    with open(file, encoding="utf-8") as f:
        result = visitor.codegen(parser.Parser(lexer.parse(
            preporcessor.prepare(f.read()))).parse())
    json.dump(result, open(out, "w", encoding="utf-8"))

