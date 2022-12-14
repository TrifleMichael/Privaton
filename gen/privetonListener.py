# Generated from priveton.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .privetonParser import privetonParser
else:
    from privetonParser import privetonParser

# This class defines a complete listener for a parse tree produced by privetonParser.
class privetonListener(ParseTreeListener):

    # Enter a parse tree produced by privetonParser#program.
    def enterProgram(self, ctx:privetonParser.ProgramContext):
        pass

    # Exit a parse tree produced by privetonParser#program.
    def exitProgram(self, ctx:privetonParser.ProgramContext):
        pass


    # Enter a parse tree produced by privetonParser#statement.
    def enterStatement(self, ctx:privetonParser.StatementContext):
        pass

    # Exit a parse tree produced by privetonParser#statement.
    def exitStatement(self, ctx:privetonParser.StatementContext):
        pass


    # Enter a parse tree produced by privetonParser#let.
    def enterLet(self, ctx:privetonParser.LetContext):
        pass

    # Exit a parse tree produced by privetonParser#let.
    def exitLet(self, ctx:privetonParser.LetContext):
        pass


    # Enter a parse tree produced by privetonParser#show.
    def enterShow(self, ctx:privetonParser.ShowContext):
        pass

    # Exit a parse tree produced by privetonParser#show.
    def exitShow(self, ctx:privetonParser.ShowContext):
        pass


    # Enter a parse tree produced by privetonParser#large_expr.
    def enterLarge_expr(self, ctx:privetonParser.Large_exprContext):
        pass

    # Exit a parse tree produced by privetonParser#large_expr.
    def exitLarge_expr(self, ctx:privetonParser.Large_exprContext):
        pass


    # Enter a parse tree produced by privetonParser#small_expr.
    def enterSmall_expr(self, ctx:privetonParser.Small_exprContext):
        pass

    # Exit a parse tree produced by privetonParser#small_expr.
    def exitSmall_expr(self, ctx:privetonParser.Small_exprContext):
        pass


    # Enter a parse tree produced by privetonParser#if_block.
    def enterIf_block(self, ctx:privetonParser.If_blockContext):
        pass

    # Exit a parse tree produced by privetonParser#if_block.
    def exitIf_block(self, ctx:privetonParser.If_blockContext):
        pass


    # Enter a parse tree produced by privetonParser#else_block.
    def enterElse_block(self, ctx:privetonParser.Else_blockContext):
        pass

    # Exit a parse tree produced by privetonParser#else_block.
    def exitElse_block(self, ctx:privetonParser.Else_blockContext):
        pass


    # Enter a parse tree produced by privetonParser#while_block.
    def enterWhile_block(self, ctx:privetonParser.While_blockContext):
        pass

    # Exit a parse tree produced by privetonParser#while_block.
    def exitWhile_block(self, ctx:privetonParser.While_blockContext):
        pass


    # Enter a parse tree produced by privetonParser#condition.
    def enterCondition(self, ctx:privetonParser.ConditionContext):
        pass

    # Exit a parse tree produced by privetonParser#condition.
    def exitCondition(self, ctx:privetonParser.ConditionContext):
        pass


    # Enter a parse tree produced by privetonParser#code_block.
    def enterCode_block(self, ctx:privetonParser.Code_blockContext):
        pass

    # Exit a parse tree produced by privetonParser#code_block.
    def exitCode_block(self, ctx:privetonParser.Code_blockContext):
        pass


    # Enter a parse tree produced by privetonParser#un_opr.
    def enterUn_opr(self, ctx:privetonParser.Un_oprContext):
        pass

    # Exit a parse tree produced by privetonParser#un_opr.
    def exitUn_opr(self, ctx:privetonParser.Un_oprContext):
        pass


    # Enter a parse tree produced by privetonParser#neg_opr.
    def enterNeg_opr(self, ctx:privetonParser.Neg_oprContext):
        pass

    # Exit a parse tree produced by privetonParser#neg_opr.
    def exitNeg_opr(self, ctx:privetonParser.Neg_oprContext):
        pass


    # Enter a parse tree produced by privetonParser#bin_opr.
    def enterBin_opr(self, ctx:privetonParser.Bin_oprContext):
        pass

    # Exit a parse tree produced by privetonParser#bin_opr.
    def exitBin_opr(self, ctx:privetonParser.Bin_oprContext):
        pass


    # Enter a parse tree produced by privetonParser#logic_opr.
    def enterLogic_opr(self, ctx:privetonParser.Logic_oprContext):
        pass

    # Exit a parse tree produced by privetonParser#logic_opr.
    def exitLogic_opr(self, ctx:privetonParser.Logic_oprContext):
        pass


    # Enter a parse tree produced by privetonParser#arthm_opr.
    def enterArthm_opr(self, ctx:privetonParser.Arthm_oprContext):
        pass

    # Exit a parse tree produced by privetonParser#arthm_opr.
    def exitArthm_opr(self, ctx:privetonParser.Arthm_oprContext):
        pass


    # Enter a parse tree produced by privetonParser#var.
    def enterVar(self, ctx:privetonParser.VarContext):
        pass

    # Exit a parse tree produced by privetonParser#var.
    def exitVar(self, ctx:privetonParser.VarContext):
        pass


    # Enter a parse tree produced by privetonParser#array.
    def enterArray(self, ctx:privetonParser.ArrayContext):
        pass

    # Exit a parse tree produced by privetonParser#array.
    def exitArray(self, ctx:privetonParser.ArrayContext):
        pass


    # Enter a parse tree produced by privetonParser#fun_def.
    def enterFun_def(self, ctx:privetonParser.Fun_defContext):
        pass

    # Exit a parse tree produced by privetonParser#fun_def.
    def exitFun_def(self, ctx:privetonParser.Fun_defContext):
        pass


