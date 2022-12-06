import sys
import unittest

from antlr4 import InputStream, CommonTokenStream
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_PATH) + "/gen")
from gen.privatonListenerExtended import PrivetonListenerExtended
from gen.privetonLexer import privetonLexer
from gen.privetonParser import privetonParser


class TestNegativeNumbers(unittest.TestCase):
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

    def testNegativeNumbers1(self):
        self.my_set_up("(-1)+1;")
        self.assertEqual(self.PLE.environment.evaluations[0], 0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)

    def testNegativeNumbers2(self):
        self.my_set_up("(-1)*1;")
        self.assertEqual(self.PLE.environment.evaluations[0], -1)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)

    def testNegativeNumbers3(self):
        self.my_set_up("(-1)*(-1);")
        self.assertEqual(self.PLE.environment.evaluations[0], 1)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)

    def testNegativeNumbers4(self):
        self.my_set_up("(-1)+(-1);")
        self.assertEqual(self.PLE.environment.evaluations[0], -2)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)

    def testNegativeNumbers5(self):
        self.my_set_up("(-1)-1;")
        self.assertEqual(self.PLE.environment.evaluations[0], -2)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)

    def testNegativeNumbers6(self):
        self.my_set_up("1+(-1);")
        self.assertEqual(self.PLE.environment.evaluations[0], 0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)

    def testNegativeNumbers7(self):
        self.my_set_up("1*(-1);")
        self.assertEqual(self.PLE.environment.evaluations[0], -1)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)

    def testNegativeNumbers8(self):
        self.my_set_up("1/(-1);")
        self.assertEqual(self.PLE.environment.evaluations[0], -1.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)

    def testNegativeNumbers9(self):
        self.my_set_up("(-1)/(-1);")
        self.assertEqual(self.PLE.environment.evaluations[0], 1.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)

    def testNegativeNumbers10(self):
        self.my_set_up("(-1)/1;")
        self.assertEqual(self.PLE.environment.evaluations[0], -1.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)

    def testNegativeNumbers11(self):
        self.my_set_up("(-1)-(-1);")
        self.assertEqual(self.PLE.environment.evaluations[0], 0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)

    def testNegativeNumbers12(self):
        self.assertRaises(ZeroDivisionError, self.my_set_up, "(-1)/(-0);")

    def testNegativeNumbers13(self):
        self.my_set_up("(-1.0)/1;")
        self.assertEqual(self.PLE.environment.evaluations[0], -1.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)

    def testNegativeNumbers14(self):
        self.my_set_up("(-1)/1.0;")
        self.assertEqual(self.PLE.environment.evaluations[0], -1.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)

    def testNegativeNumbers15(self):
        self.my_set_up("1.0/(-1.0);")
        self.assertEqual(self.PLE.environment.evaluations[0], -1.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)

    def testNegativeNumbers16(self):
        self.my_set_up("1/(-1.0);")
        self.assertEqual(self.PLE.environment.evaluations[0], -1.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)

    def testNegativeNumbers17(self):
        self.my_set_up("(-1.0)/(-1.0);")
        self.assertEqual(self.PLE.environment.evaluations[0], 1.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)

    def testNegativeNumbers18(self):
        self.my_set_up("(-1)/(-1.0);")
        self.assertEqual(self.PLE.environment.evaluations[0], 1.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)
