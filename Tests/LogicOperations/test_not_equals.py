import sys
import unittest

from antlr4 import InputStream, CommonTokenStream
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_PATH) + "/gen")
from gen.privatonListenerExtended import PrivetonListenerExtended
from gen.privetonLexer import privetonLexer
from gen.privetonParser import privetonParser


class TestNotEquals(unittest.TestCase):
    def my_set_up(self, stream):
        input_stream = InputStream(stream)
        lexer = privetonLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = privetonParser(stream)
        self.PLE = PrivetonListenerExtended()
        parser.addParseListener(self.PLE)
        parser.program()

    def testNotEqualsWithTwoInts1(self):
        self.my_set_up("2!=3;")
        self.assertEqual(self.PLE.environment.evaluations[0], True)

    def testNotEqualsWithTwoInts2(self):
        self.my_set_up("2!=2;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testNotEqualsWithTwoInts3(self):
        self.my_set_up("0!=2;")
        self.assertEqual(self.PLE.environment.evaluations[0], True)

    def testNotEqualsWithTwoInts4(self):
        self.my_set_up("0!=0;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testVariableNotEqualsIntTrue(self):
        self.my_set_up("a=2;a!=2;")
        self.assertEqual(self.PLE.environment.evaluations[1], False)

    def testVariableNotEqualsIntFalse(self):
        self.my_set_up("a=2;a!=3;")
        self.assertEqual(self.PLE.environment.evaluations[1], True)

    def testVariableNotEquals0(self):
        self.my_set_up("a=0;a!=0;")
        self.assertEqual(self.PLE.environment.evaluations[1], False)

    def testNotEqualsTwoFloats1(self):
        self.my_set_up("1.0!=1.0;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testNotEqualsTwoFloats2(self):
        self.my_set_up("1.0!=2.0;")
        self.assertEqual(self.PLE.environment.evaluations[0], True)

    def testNotEqualsTwoFloats3(self):
        self.my_set_up("0.0!=1.0;")
        self.assertEqual(self.PLE.environment.evaluations[0], True)

    def testNotEqualsTwoFloats4(self):
        self.my_set_up("0.0!=0.0;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testNotEqualsTwoFloats5(self):
        self.my_set_up("1.2345!=1.2345;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testNotEqualsTwoFloats6(self):
        self.my_set_up("1.234!=1.2345;")
        self.assertEqual(self.PLE.environment.evaluations[0], True)

    def testNotEqualsFloatAndInt1(self):
        self.my_set_up("0!=0.0;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testNotEqualsFloatAndInt2(self):
        self.my_set_up("1!=0.0;")
        self.assertEqual(self.PLE.environment.evaluations[0], True)

    def testNotEqualsFloatAndInt3(self):
        self.my_set_up("1.0==0;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testNotEqualsFloatAndInt4(self):
        self.my_set_up("1.0!=1;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testNotEqualsFloatAndInt5(self):
        self.my_set_up("1.0!=1;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testNotEqualsFloatAndInt6(self):
        self.my_set_up("1.000000000!=1;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testNotEqualsFloatAndInt7(self):
        self.my_set_up("1.0000000001!=1;")
        self.assertEqual(self.PLE.environment.evaluations[0], True)
