import sys
from antlr4 import *
from pathlib import Path

from gen.privetonVisitorExtended import privetonVisitorExtended

ROOT_PATH = Path(__file__).parent

from gen.privatonListenerExtended import PrivetonListenerExtended
from gen.privetonLexer import privetonLexer
from gen.privetonParser import privetonParser


def main(argv):
    input_stream = FileStream("test.txt")
    # input_stream = InputStream('1/2*2;')
    lexer = privetonLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = privetonParser(stream)
    tree = parser.program()
    visitor = privetonVisitorExtended()
    result = visitor.visit(tree)

    # PLE = PrivetonListenerExtended()
    # parser.addParseListener(PLE)
    # parser.program()
    # print(PLE.environment.get_environment())


if __name__ == '__main__':
    main(sys.argv)
