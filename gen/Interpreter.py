import sys
from antlr4 import *
from gen.privatonListenerExtended import PrivetonListenerExtended
from gen.privetonLexer import privetonLexer
from gen.privetonParser import privetonParser


def main(argv):
    input_stream = FileStream('test.txt')
    lexer = privetonLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = privetonParser(stream)
    PLE = PrivetonListenerExtended()
    parser.addParseListener(PLE)
    parser.program()


if __name__ == '__main__':
    main(sys.argv)