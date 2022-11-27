# Generated from simplerlang.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .simplerlangParser import simplerlangParser
else:
    from simplerlangParser import simplerlangParser

# This class defines a complete listener for a parse tree produced by simplerlangParser.
class simplerlangListener(ParseTreeListener):

    # Enter a parse tree produced by simplerlangParser#program.
    def enterProgram(self, ctx:simplerlangParser.ProgramContext):
        pass

    # Exit a parse tree produced by simplerlangParser#program.
    def exitProgram(self, ctx:simplerlangParser.ProgramContext):
        pass


    # Enter a parse tree produced by simplerlangParser#statement.
    def enterStatement(self, ctx:simplerlangParser.StatementContext):
        pass

    # Exit a parse tree produced by simplerlangParser#statement.
    def exitStatement(self, ctx:simplerlangParser.StatementContext):
        pass


    # Enter a parse tree produced by simplerlangParser#let.
    def enterLet(self, ctx:simplerlangParser.LetContext):
        pass

    # Exit a parse tree produced by simplerlangParser#let.
    def exitLet(self, ctx:simplerlangParser.LetContext):
        pass


    # Enter a parse tree produced by simplerlangParser#show.
    def enterShow(self, ctx:simplerlangParser.ShowContext):
        pass

    # Exit a parse tree produced by simplerlangParser#show.
    def exitShow(self, ctx:simplerlangParser.ShowContext):
        pass


    # Enter a parse tree produced by simplerlangParser#large_expr.
    def enterLarge_expr(self, ctx:simplerlangParser.Large_exprContext):
        pass

    # Exit a parse tree produced by simplerlangParser#large_expr.
    def exitLarge_expr(self, ctx:simplerlangParser.Large_exprContext):
        pass


    # Enter a parse tree produced by simplerlangParser#small_expr.
    def enterSmall_expr(self, ctx:simplerlangParser.Small_exprContext):
        pass

    # Exit a parse tree produced by simplerlangParser#small_expr.
    def exitSmall_expr(self, ctx:simplerlangParser.Small_exprContext):
        pass


    # Enter a parse tree produced by simplerlangParser#if_block.
    def enterIf_block(self, ctx:simplerlangParser.If_blockContext):
        pass

    # Exit a parse tree produced by simplerlangParser#if_block.
    def exitIf_block(self, ctx:simplerlangParser.If_blockContext):
        pass


    # Enter a parse tree produced by simplerlangParser#for_block.
    def enterFor_block(self, ctx:simplerlangParser.For_blockContext):
        pass

    # Exit a parse tree produced by simplerlangParser#for_block.
    def exitFor_block(self, ctx:simplerlangParser.For_blockContext):
        pass


    # Enter a parse tree produced by simplerlangParser#code_block.
    def enterCode_block(self, ctx:simplerlangParser.Code_blockContext):
        pass

    # Exit a parse tree produced by simplerlangParser#code_block.
    def exitCode_block(self, ctx:simplerlangParser.Code_blockContext):
        pass


    # Enter a parse tree produced by simplerlangParser#un_opr.
    def enterUn_opr(self, ctx:simplerlangParser.Un_oprContext):
        pass

    # Exit a parse tree produced by simplerlangParser#un_opr.
    def exitUn_opr(self, ctx:simplerlangParser.Un_oprContext):
        pass


    # Enter a parse tree produced by simplerlangParser#neg_opr.
    def enterNeg_opr(self, ctx:simplerlangParser.Neg_oprContext):
        pass

    # Exit a parse tree produced by simplerlangParser#neg_opr.
    def exitNeg_opr(self, ctx:simplerlangParser.Neg_oprContext):
        pass


    # Enter a parse tree produced by simplerlangParser#bin_opr.
    def enterBin_opr(self, ctx:simplerlangParser.Bin_oprContext):
        pass

    # Exit a parse tree produced by simplerlangParser#bin_opr.
    def exitBin_opr(self, ctx:simplerlangParser.Bin_oprContext):
        pass


    # Enter a parse tree produced by simplerlangParser#logic_opr.
    def enterLogic_opr(self, ctx:simplerlangParser.Logic_oprContext):
        pass

    # Exit a parse tree produced by simplerlangParser#logic_opr.
    def exitLogic_opr(self, ctx:simplerlangParser.Logic_oprContext):
        pass


    # Enter a parse tree produced by simplerlangParser#arthm_opr.
    def enterArthm_opr(self, ctx:simplerlangParser.Arthm_oprContext):
        pass

    # Exit a parse tree produced by simplerlangParser#arthm_opr.
    def exitArthm_opr(self, ctx:simplerlangParser.Arthm_oprContext):
        pass


    # Enter a parse tree produced by simplerlangParser#var.
    def enterVar(self, ctx:simplerlangParser.VarContext):
        pass

    # Exit a parse tree produced by simplerlangParser#var.
    def exitVar(self, ctx:simplerlangParser.VarContext):
        pass


    # Enter a parse tree produced by simplerlangParser#array.
    def enterArray(self, ctx:simplerlangParser.ArrayContext):
        pass

    # Exit a parse tree produced by simplerlangParser#array.
    def exitArray(self, ctx:simplerlangParser.ArrayContext):
        pass


    # Enter a parse tree produced by simplerlangParser#fun_def.
    def enterFun_def(self, ctx:simplerlangParser.Fun_defContext):
        pass

    # Exit a parse tree produced by simplerlangParser#fun_def.
    def exitFun_def(self, ctx:simplerlangParser.Fun_defContext):
        pass


