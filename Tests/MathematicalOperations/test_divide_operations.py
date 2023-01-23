import sys
import unittest

from antlr4 import InputStream, CommonTokenStream
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_PATH) + "/gen")
from gen.privatonListenerExtended import PrivetonListenerExtended
from gen.privetonLexer import privetonLexer
from gen.privetonParser import privetonParser


class TestDivide(unittest.TestCase):
    def my_set_up(self, stream):
        input_stream = InputStream(stream)
        lexer = privetonLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = privetonParser(stream)
        self.PLE = PrivetonListenerExtended()
        parser.addParseListener(self.PLE)
        try:
            parser.program()
        except ZeroDivisionError:
            raise ZeroDivisionError

    def testDivideOperation1(self):
        self.my_set_up("1/1;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 1.0)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], float)

    def testDivideOperation2(self):
        self.my_set_up("1/2;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 1 / 2)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], float)

    def testDivideOperation3(self):
        self.my_set_up("1/2/3;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 1 / 2 / 3)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], float)

    def testDivideOperation4(self):
        self.my_set_up("2/1;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 2.0)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], float)

    def testDivideOperation5(self):
        self.assertRaises(ZeroDivisionError, self.my_set_up, "1/0;")

    def testDivideOperation6(self):
        self.assertRaises(ZeroDivisionError, self.my_set_up, "0/0;")

    def testDivideOperation7(self):
        self.assertRaises(ZeroDivisionError, self.my_set_up, "1/2/0;")

    def testDivideOperation8(self):
        self.assertRaises(ZeroDivisionError, self.my_set_up, "1/2/3/4/5/6/7/8/9/0;")

    def testDivideOperation9(self):
        self.assertRaises(ZeroDivisionError, self.my_set_up, "0/1/2/3/4/0;")
