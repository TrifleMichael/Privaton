import sys
import unittest

from antlr4 import InputStream, CommonTokenStream
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_PATH) + "/gen")
from gen.privatonListenerExtended import PrivetonListenerExtended
from gen.privetonLexer import privetonLexer
from gen.privetonParser import privetonParser


class TestSubtract(unittest.TestCase):
    def my_set_up(self, stream):
        input_stream = InputStream(stream)
        lexer = privetonLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = privetonParser(stream)
        self.PLE = PrivetonListenerExtended()
        parser.addParseListener(self.PLE)
        parser.program()

    def testSubtractOperation1(self):
        self.my_set_up("1-1;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 0)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], int)

    def testSubtractOperation2(self):
        self.my_set_up("1-2;")
        self.assertEqual(self.PLE.environment.evaluations[-1], -1)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], int)

    def testSubtractOperation3(self):
        self.my_set_up("3.0-2;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 1.0)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], float)

    def testSubtractOperation4(self):
        self.my_set_up("1.0-2;")
        self.assertEqual(self.PLE.environment.evaluations[-1], -1.0)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], float)

    def testSubtractOperation5(self):
        self.my_set_up("1-1.0;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 0.0)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], float)

    def testSubtractOperation6(self):
        self.my_set_up("0-0;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 0)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], int)

    def testSubtractOperation7(self):
        self.my_set_up("0-0.0;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 0.0)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], float)

    def testSubtractOperation8(self):
        self.my_set_up("0.0-0.0;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 0.0)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], float)
