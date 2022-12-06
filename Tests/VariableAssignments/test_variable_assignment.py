import sys
import unittest

from antlr4 import InputStream, CommonTokenStream
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_PATH) + "/gen")
from gen.privatonListenerExtended import PrivetonListenerExtended
from gen.privetonLexer import privetonLexer
from gen.privetonParser import privetonParser


class TestVariableAssignment(unittest.TestCase):
    def my_set_up(self, stream):
        input_stream = InputStream(stream)
        lexer = privetonLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = privetonParser(stream)
        self.PLE = PrivetonListenerExtended()
        parser.addParseListener(self.PLE)
        parser.program()

    def testVariableAssignment1(self):
        self.my_set_up("a=2;")
        self.assertEqual(self.PLE.environment.evaluations[0], 2)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)

    def testVariableAssignment2(self):
        self.my_set_up("a=231978782931;")
        self.assertEqual(self.PLE.environment.evaluations[0], 231978782931)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)

    def testVariableAssignment3(self):
        self.my_set_up("a=0;")
        self.assertEqual(self.PLE.environment.evaluations[0], 0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)

    def testVariableAssignment4(self):
        self.my_set_up("a=1.01;")
        self.assertEqual(self.PLE.environment.evaluations[0], 1.01)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)

    def testVariableAssignment5_1(self):
        self.my_set_up('a="abc";')
        self.assertEqual(self.PLE.environment.evaluations[0], "abc")
        self.assertIsInstance(self.PLE.environment.evaluations[0], str)

    def testVariableAssignment5_2(self):
        self.my_set_up('a="abc;;";')
        self.assertEqual(self.PLE.environment.evaluations[0], "abc;;")
        self.assertIsInstance(self.PLE.environment.evaluations[0], str)

    def testVariableAssignment5_3(self):
        self.my_set_up('a=";abc;;";')
        self.assertEqual(self.PLE.environment.evaluations[0], ";abc;;")
        self.assertIsInstance(self.PLE.environment.evaluations[0], str)

    def testVariableAssignment5_4(self):
        self.my_set_up('a=";a_b.c;;";')
        self.assertEqual(self.PLE.environment.evaluations[0], ";a_b.c;;")
        self.assertIsInstance(self.PLE.environment.evaluations[0], str)

    def testVariableAssignment6(self):
        self.my_set_up('a="";')
        self.assertEqual(self.PLE.environment.evaluations[0], "")
        self.assertIsInstance(self.PLE.environment.evaluations[0], str)

    def testVariableAssignment7(self):
        self.my_set_up('a=True;')
        self.assertEqual(self.PLE.environment.evaluations[0], True)
        self.assertIsInstance(self.PLE.environment.evaluations[0], bool)

    def testVariableAssignment8(self):
        self.my_set_up('a=False;')
        self.assertEqual(self.PLE.environment.evaluations[0], False)
        self.assertIsInstance(self.PLE.environment.evaluations[0], bool)

    def testMultipleVariablesAssignment1(self):
        self.my_set_up('a=1;b=2.0;')
        self.assertEqual(self.PLE.environment.evaluations[0], 1)
        self.assertEqual(self.PLE.environment.evaluations[1], 2.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)
        self.assertIsInstance(self.PLE.environment.evaluations[1], float)

    def testMultipleVariablesAssignment2(self):
        self.my_set_up('a=1.001;b=2.0')
        self.assertEqual(self.PLE.environment.evaluations[0], 1.001)
        self.assertEqual(self.PLE.environment.evaluations[1], 2.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)
        self.assertIsInstance(self.PLE.environment.evaluations[1], float)

    def testMultipleVariablesAssignment3(self):
        self.my_set_up('a=1.001;b=2.0')
        self.assertEqual(self.PLE.environment.evaluations[0], 1.001)
        self.assertEqual(self.PLE.environment.evaluations[1], 2.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)
        self.assertIsInstance(self.PLE.environment.evaluations[1], float)

    def testMultipleVariablesAssignment4(self):
        self.my_set_up('a=1.001;b=2.0;c=a;')
        self.assertEqual(self.PLE.environment.evaluations[0], 1.001)
        self.assertEqual(self.PLE.environment.evaluations[1], 2.0)
        self.assertEqual(self.PLE.environment.evaluations[2], 1.001)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)
        self.assertIsInstance(self.PLE.environment.evaluations[1], float)
        self.assertIsInstance(self.PLE.environment.evaluations[2], float)

    def testMultipleVariablesAssignment5(self):
        self.my_set_up('a=1.001;b=2.0;c=a;d=11')
        self.assertEqual(self.PLE.environment.evaluations[0], 1.001)
        self.assertEqual(self.PLE.environment.evaluations[1], 2.0)
        self.assertEqual(self.PLE.environment.evaluations[2], 1.001)
        self.assertEqual(self.PLE.environment.evaluations[0], 11)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)
        self.assertIsInstance(self.PLE.environment.evaluations[1], float)
        self.assertIsInstance(self.PLE.environment.evaluations[2], float)
        self.assertIsInstance(self.PLE.environment.evaluations[3], int)

    def testAssignmentWithVariousOperations1(self):
        self.my_set_up('a=1+1;')
        self.assertEqual(self.PLE.environment.evaluations[0], 2)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)

    def testAssignmentWithVariousOperations2(self):
        self.my_set_up('a=1.0+1;')
        self.assertEqual(self.PLE.environment.evaluations[0], 2.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)

    def testAssignmentWithVariousOperations3(self):
        self.my_set_up('a=1.0*1;')
        self.assertEqual(self.PLE.environment.evaluations[0], 1.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)

    def testAssignmentWithVariousOperations4(self):
        self.my_set_up('a=1.0*1*2 + 2;')
        self.assertEqual(self.PLE.environment.evaluations[0], 4.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)

    def testAssignmentWithVariousOperations5(self):
        self.my_set_up('a=1.0*1*2 + 2*2;')
        self.assertEqual(self.PLE.environment.evaluations[0], 6.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], float)

    def testAssignmentWithVariousOperations6(self):
        self.my_set_up('a=1*1*2-1+2;')
        self.assertEqual(self.PLE.environment.evaluations[0], 3)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)

    def testAssignmentWithVariousOperations7(self):
        self.my_set_up('a=2+2*2;')
        self.assertEqual(self.PLE.environment.evaluations[0], 6)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)

    def testAssignmentWithVariousOperations8(self):
        self.my_set_up('a=2*2+2;')
        self.assertEqual(self.PLE.environment.evaluations[0], 6)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)

    def testAssignmentWithVariousOperations9(self):
        self.my_set_up('a=2;b=3;c=a*b+2*1.0;')
        self.assertEqual(self.PLE.environment.evaluations[0], 2)
        self.assertEqual(self.PLE.environment.evaluations[0], 3)
        self.assertEqual(self.PLE.environment.evaluations[0], 8.0)
        self.assertIsInstance(self.PLE.environment.evaluations[0], int)
        self.assertIsInstance(self.PLE.environment.evaluations[1], int)
        self.assertIsInstance(self.PLE.environment.evaluations[2], float)
