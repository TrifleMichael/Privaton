import sys
import unittest

from antlr4 import InputStream, CommonTokenStream
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_PATH) + "/gen")
from gen.privatonListenerExtended import PrivetonListenerExtended
from gen.privetonLexer import privetonLexer
from gen.privetonParser import privetonParser


class TestAdd(unittest.TestCase):
    def my_set_up(self, stream):
        input_stream = InputStream(stream)
        lexer = privetonLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = privetonParser(stream)
        self.PLE = PrivetonListenerExtended()
        parser.addParseListener(self.PLE)
        parser.program()

    def testAdditionOperation1(self):
        self.my_set_up("1+1;")
        self.assertEqual(self.PLE.environment.evaluations[0], 2)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)

    def testAdditionOperation2(self):
        self.my_set_up("1+11;")
        self.assertEqual(self.PLE.environment.evaluations[0], 12)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)

    def testAdditionOperation3(self):
        self.my_set_up("0+0;")
        self.assertEqual(self.PLE.environment.evaluations[0], 0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)

    def testAdditionOperation4(self):
        self.my_set_up("0.0+0;")
        self.assertEqual(self.PLE.environment.evaluations[0], 0.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)

    def testAdditionOperation5(self):
        self.my_set_up("1.0+1.0;")
        self.assertEqual(self.PLE.environment.evaluations[0], 2.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)

    def testAdditionOperation6(self):
        self.my_set_up("1+1.0;")
        self.assertEqual(self.PLE.environment.evaluations[0], 2.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)

    def testAdditionOperation7(self):
        self.my_set_up("0+(-2);")
        self.assertEqual(self.PLE.environment.evaluations[0], -2)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)

    def testAdditionOperation8(self):
        self.my_set_up("1.0+(-1);")
        self.assertEqual(self.PLE.environment.evaluations[0], 0.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)
