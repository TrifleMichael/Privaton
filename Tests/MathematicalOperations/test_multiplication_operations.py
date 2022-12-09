import sys
import unittest

from antlr4 import InputStream, CommonTokenStream
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_PATH) + "/gen")
from gen.privatonListenerExtended import PrivetonListenerExtended
from gen.privetonLexer import privetonLexer
from gen.privetonParser import privetonParser


class TestMultiplication(unittest.TestCase):
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

    def testMultiplicationOperation1(self):
        self.my_set_up("1*1;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 1)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)

    def testMultiplicationOperation2(self):
        self.my_set_up("1.0*1;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 1.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)

    def testMultiplicationOperation3(self):
        self.my_set_up("1.0*0;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 0.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)

    def testMultiplicationOperation4(self):
        self.my_set_up("1*0;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)

    def testMultiplicationOperation5(self):
        self.my_set_up("1.0*0;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 0.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)

    def testMultiplicationOperation6(self):
        self.my_set_up("0*0;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)

    def testMultiplicationOperation7(self):
        self.my_set_up("0.0*0;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 0.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)

    def testMultiplicationOperation8(self):
        self.my_set_up("(-1.0)*0;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 0.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)

    def testMultiplicationOperation9(self):
        self.my_set_up("1.0*(-1);")
        self.assertEqual(self.PLE.environment.evaluations[-1], -1.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)

    def testMultiplicationOperation10(self):
        self.my_set_up("(-1.0)*(-1);")
        self.assertEqual(self.PLE.environment.evaluations[-1], 1.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)

    def testMultiplicationOperation11(self):
        self.my_set_up("1*(-1);")
        self.assertEqual(self.PLE.environment.evaluations[-1], -1)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)

    def testMultiplicationOperation12(self):
        self.my_set_up("(-1)*(-1);")
        self.assertEqual(self.PLE.environment.evaluations[-1], 1)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)

    def testMultiplicationOperation13(self):
        self.my_set_up("2*(1/2);")
        self.assertEqual(self.PLE.environment.evaluations[-1], 1.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)

    def testMultiplicationOperation14(self):
        self.my_set_up("(-2)*(1/2);")
        self.assertEqual(self.PLE.environment.evaluations[-1], -1.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)

    def testMultiplicationOperation15(self):
        self.assertRaises(ZeroDivisionError, self.my_set_up, "(-2)*(1/0);")

