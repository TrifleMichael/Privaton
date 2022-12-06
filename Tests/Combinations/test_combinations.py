import sys
import unittest

from antlr4 import InputStream, CommonTokenStream
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_PATH) + "/gen")
from gen.privatonListenerExtended import PrivetonListenerExtended
from gen.privetonLexer import privetonLexer
from gen.privetonParser import privetonParser


class TestCombinations(unittest.TestCase):
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

    def testCombinations1(self):
        self.my_set_up("1/2*2;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 1 / 2 * 2)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], float)

    def testCombinations2(self):
        self.my_set_up("1/2/3*2;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 1 / 2 / 3 * 2)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], float)

    def testCombinations3(self):
        self.my_set_up("(1/2)/(3*2);")
        self.assertEqual(self.PLE.environment.evaluations[-1], (1 / 2) / (3 * 2))
        self.assertIsInstance(self.PLE.environment.evaluations[-1], float)

    def testCombinations4(self):
        self.my_set_up("(1+2)/(3-2);")
        self.assertEqual(self.PLE.environment.evaluations[-1], (1 + 2) / (3 - 2))
        self.assertIsInstance(self.PLE.environment.evaluations[-1], float)

    def testCombinations5(self):
        self.my_set_up("(1+2)*2/(3-2);")
        self.assertEqual(self.PLE.environment.evaluations[-1], (1 + 2) * 2 / (3 - 2))
        self.assertIsInstance(self.PLE.environment.evaluations[-1], float)

    def testCombinations6(self):
        self.my_set_up("(1+2)*2/(3-2)*2;")
        self.assertEqual(self.PLE.environment.evaluations[-1], (1 + 2) * 2 / (3 - 2) * 2)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], float)

    def testCombinations7(self):
        self.my_set_up("(1+2)*2/((3-2)*2);")
        self.assertEqual(self.PLE.environment.evaluations[-1], (1 + 2) * 2 / ((3 - 2) * 2))
        self.assertIsInstance(self.PLE.environment.evaluations[-1], float)

    def testCombinations8(self):
        self.my_set_up("((1+2)*2-1)/((3-2)*2);")
        self.assertEqual(self.PLE.environment.evaluations[-1], ((1 + 2) * 2 - 1) / ((3 - 2) * 2))
        self.assertIsInstance(self.PLE.environment.evaluations[-1], float)

    def testCombinations9(self):
        self.my_set_up("1+1+1+1+2-2;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 4)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], int)

    def testCombinations10(self):
        self.my_set_up("(1+1)+1+1+2-2;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 4)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], int)

    def testCombinations11(self):
        self.my_set_up("(1+1)+(1+1)+2-2;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 4)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], int)

    def testCombinations12(self):
        self.my_set_up("((1+1)+1+1)+2-2;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 4)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], int)

    def testCombinations13(self):
        self.my_set_up("((1+1)+(1+1))+2-2;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 4)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], int)

    def testCombinations14(self):
        self.my_set_up("((1+1)+(1+1))+(2-2);")
        self.assertEqual(self.PLE.environment.evaluations[-1], 4)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], int)

    def testCombinations15(self):
        self.my_set_up("(((1+1)+(1+1))+(2-2));")
        self.assertEqual(self.PLE.environment.evaluations[-1], 4)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], int)

    def testCombinations16(self):
        self.my_set_up("((((1)+1)+1)+1)+2-2;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 4)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], int)

    def testCombinations17(self):
        self.my_set_up("((((1)+(1))+(1))+(1))+(2)-(2);")
        self.assertEqual(self.PLE.environment.evaluations[-1], 4)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], int)

    def testCombinations18(self):
        self.my_set_up("((((1)+(1))+(1))+(1))+((2)-(2));")
        self.assertEqual(self.PLE.environment.evaluations[-1], 4)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], int)

    def testCombinations19(self):
        self.my_set_up("1*True;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 1)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], int)

    def testCombinations20(self):
        self.my_set_up("1*False;")
        self.assertEqual(self.PLE.environment.evaluations[-1], 0)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], int)

    def testCombinations21(self):
        self.my_set_up('1*"a";')
        self.assertEqual(self.PLE.environment.evaluations[-1], "a")
        self.assertIsInstance(self.PLE.environment.evaluations[-1], str)

    def testCombinations22(self):
        self.my_set_up('2*"a";')
        self.assertEqual(self.PLE.environment.evaluations[-1], "aa")
        self.assertIsInstance(self.PLE.environment.evaluations[-1], str)

    def testCombinations23(self):
        self.my_set_up('1*[1];')
        self.assertEqual(self.PLE.environment.evaluations[-1], [1])
        self.assertIsInstance(self.PLE.environment.evaluations[-1], list)

    def testCombinations24(self):
        self.my_set_up('2*[1];')
        self.assertEqual(self.PLE.environment.evaluations[-1], [1, 1])
        self.assertIsInstance(self.PLE.environment.evaluations[-1], list)

    def testCombinations25(self):
        self.assertRaises(ZeroDivisionError, self.my_set_up, "((((1)+(1))+(1))+(1))/((2)-(2));")

    def testCombinations26(self):
        self.my_set_up("((((1)+(1))+(1))+(1))*((2)-(2));")
        self.assertEqual(self.PLE.environment.evaluations[-1], 0)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], int)

    def testCombinations27(self):
        self.my_set_up("((((1)+(1))+(1))+(1))*((2)+(-2));")
        self.assertEqual(self.PLE.environment.evaluations[-1], 0)
        self.assertIsInstance(self.PLE.environment.evaluations[-1], int)
