import sys
from antlr4 import *
from gen.simplerlangListenerExtended import SimplerlangListenerExtended

from simplerlangParser import simplerlangParser
from simplerlangLexer import simplerlangLexer


def main(argv):
    input_stream = FileStream('test.txt')
    lexer = simplerlangLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = simplerlangParser(stream)
    sle = SimplerlangListenerExtended()
    parser.addParseListener(sle)
    parser.program()


if __name__ == '__main__':
    main(sys.argv)