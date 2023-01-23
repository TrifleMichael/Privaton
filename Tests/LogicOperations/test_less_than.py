import sys
import unittest

from antlr4 import InputStream, CommonTokenStream
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_PATH) + "/gen")
from gen.privatonListenerExtended import PrivetonListenerExtended
from gen.privetonLexer import privetonLexer
from gen.privetonParser import privetonParser


class TestLess(unittest.TestCase):
    def my_set_up(self, stream):
        input_stream = InputStream(stream)
        lexer = privetonLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = privetonParser(stream)
        self.PLE = PrivetonListenerExtended()
        parser.addParseListener(self.PLE)
        parser.program()

    def testGreaterThanWithTwoInts1(self):
        self.my_set_up("2<3;")
        self.assertEqual(self.PLE.environment.evaluations[0], True)

    def testGreaterThanWithTwoInts2(self):
        self.my_set_up("2<2;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testGreaterThanWithTwoInts3(self):
        self.my_set_up("0<2;")
        self.assertEqual(self.PLE.environment.evaluations[0], True)

    def testGreaterThanWithTwoInts4(self):
        self.my_set_up("0<0;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testVariableGreaterThanIntTrue(self):
        self.my_set_up("a=2;a<2;")
        self.assertEqual(self.PLE.environment.evaluations[1], False)

    def testVariableGreaterThanIntFalse(self):
        self.my_set_up("a=2;a<3;")
        self.assertEqual(self.PLE.environment.evaluations[1], True)

    def testVariableGreaterThan0(self):
        self.my_set_up("a=0;a<0;")
        self.assertEqual(self.PLE.environment.evaluations[1], False)

    def testGreaterThanTwoFloats1(self):
        self.my_set_up("1.0<1.0;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testGreaterThanTwoFloats2(self):
        self.my_set_up("1.0<2.0;")
        self.assertEqual(self.PLE.environment.evaluations[0], True)

    def testGreaterThanTwoFloats3(self):
        self.my_set_up("0.0<1.0;")
        self.assertEqual(self.PLE.environment.evaluations[0], True)

    def testGreaterThanTwoFloats4(self):
        self.my_set_up("0.0<0.0;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testGreaterThanTwoFloats5(self):
        self.my_set_up("1.2345<1.2345;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testGreaterThanTwoFloats6(self):
        self.my_set_up("1.234<1.2345;")
        self.assertEqual(self.PLE.environment.evaluations[0], True)

    def testGreaterThanFloatAndInt1(self):
        self.my_set_up("0<0.0;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testGreaterThanFloatAndInt2(self):
        self.my_set_up("1<0.0;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testGreaterThanFloatAndInt3(self):
        self.my_set_up("1.0<0;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testGreaterThanFloatAndInt4(self):
        self.my_set_up("1.0<1;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testGreaterThanFloatAndInt5(self):
        self.my_set_up("1<1.0;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testGreaterThanFloatAndInt6(self):
        self.my_set_up("1.000000000<1;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testGreaterThanFloatAndInt7(self):
        self.my_set_up("1.0000000001<1;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)
