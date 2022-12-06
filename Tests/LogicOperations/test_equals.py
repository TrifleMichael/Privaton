import sys
import unittest

from antlr4 import InputStream, CommonTokenStream
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_PATH) + "/gen")
from gen.privatonListenerExtended import PrivetonListenerExtended
from gen.privetonLexer import privetonLexer
from gen.privetonParser import privetonParser


class TestEquals(unittest.TestCase):
    def my_set_up(self, stream):
        input_stream = InputStream(stream)
        lexer = privetonLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = privetonParser(stream)
        self.PLE = PrivetonListenerExtended()
        parser.addParseListener(self.PLE)
        parser.program()

    def testEqualsWithTwoInts1(self):
        self.my_set_up("2==3;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testEqualsWithTwoInts2(self):
        self.my_set_up("2==2;")
        self.assertEqual(self.PLE.environment.evaluations[0], True)

    def testEqualsWithTwoInts3(self):
        self.my_set_up("0==2;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testEqualsWithTwoInts4(self):
        self.my_set_up("0==0;")
        self.assertEqual(self.PLE.environment.evaluations[0], True)

    def testVariableEqualsIntTrue(self):
        self.my_set_up("a=2;a==2;")
        self.assertEqual(self.PLE.environment.evaluations[1], True)

    def testVariableEqualsIntFalse(self):
        self.my_set_up("a=2;a==3;")
        self.assertEqual(self.PLE.environment.evaluations[1], False)

    def testVariableEquals0(self):
        self.my_set_up("a=0;a==0;")
        self.assertEqual(self.PLE.environment.evaluations[1], True)

    def testEqualsTwoFloats1(self):
        self.my_set_up("1.0==1.0;")
        self.assertEqual(self.PLE.environment.evaluations[0], True)

    def testEqualsTwoFloats2(self):
        self.my_set_up("1.0==2.0;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testEqualsTwoFloats3(self):
        self.my_set_up("0.0==1.0;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testEqualsTwoFloats4(self):
        self.my_set_up("0.0==0.0;")
        self.assertEqual(self.PLE.environment.evaluations[0], True)

    def testEqualsTwoFloats5(self):
        self.my_set_up("1.2345==1.2345;")
        self.assertEqual(self.PLE.environment.evaluations[0], True)

    def testEqualsTwoFloats6(self):
        self.my_set_up("1.234==1.2345;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testEqualsFloatAndInt1(self):
        self.my_set_up("0==0.0;")
        self.assertEqual(self.PLE.environment.evaluations[0], True)

    def testEqualsFloatAndInt2(self):
        self.my_set_up("1==0.0;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testEqualsFloatAndInt3(self):
        self.my_set_up("1.0==0;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)

    def testEqualsFloatAndInt4(self):
        self.my_set_up("1==1.0;")
        self.assertEqual(self.PLE.environment.evaluations[0], True)

    def testEqualsFloatAndInt5(self):
        self.my_set_up("1.0==1;")
        self.assertEqual(self.PLE.environment.evaluations[0], True)

    def testEqualsFloatAndInt6(self):
        self.my_set_up("1.000000000==1;")
        self.assertEqual(self.PLE.environment.evaluations[0], True)

    def testEqualsFloatAndInt7(self):
        self.my_set_up("1.0000000001==1;")
        self.assertEqual(self.PLE.environment.evaluations[0], False)
