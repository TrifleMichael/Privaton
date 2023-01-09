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


    # Enter a parse tree produced by privetonParser#expr.
    def enterExpr(self, ctx:privetonParser.ExprContext):
        pass

    # Exit a parse tree produced by privetonParser#expr.
    def exitExpr(self, ctx:privetonParser.ExprContext):
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


    # Enter a parse tree produced by privetonParser#priority_opr.
    def enterPriority_opr(self, ctx:privetonParser.Priority_oprContext):
        pass

    # Exit a parse tree produced by privetonParser#priority_opr.
    def exitPriority_opr(self, ctx:privetonParser.Priority_oprContext):
        pass


    # Enter a parse tree produced by privetonParser#non_priority_opr.
    def enterNon_priority_opr(self, ctx:privetonParser.Non_priority_oprContext):
        pass

    # Exit a parse tree produced by privetonParser#non_priority_opr.
    def exitNon_priority_opr(self, ctx:privetonParser.Non_priority_oprContext):
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


    # Enter a parse tree produced by privetonParser#logic_opr.
    def enterLogic_opr(self, ctx:privetonParser.Logic_oprContext):
        pass

    # Exit a parse tree produced by privetonParser#logic_opr.
    def exitLogic_opr(self, ctx:privetonParser.Logic_oprContext):
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


    # Enter a parse tree produced by privetonParser#func_call.
    def enterFunc_call(self, ctx:privetonParser.Func_callContext):
        pass

    # Exit a parse tree produced by privetonParser#func_call.
    def exitFunc_call(self, ctx:privetonParser.Func_callContext):
        pass


    # Enter a parse tree produced by privetonParser#outer_name.
    def enterOuter_name(self, ctx:privetonParser.Outer_nameContext):
        pass

    # Exit a parse tree produced by privetonParser#outer_name.
    def exitOuter_name(self, ctx:privetonParser.Outer_nameContext):
        pass


    # Enter a parse tree produced by privetonParser#return_call.
    def enterReturn_call(self, ctx:privetonParser.Return_callContext):
        pass

    # Exit a parse tree produced by privetonParser#return_call.
    def exitReturn_call(self, ctx:privetonParser.Return_callContext):
        pass


