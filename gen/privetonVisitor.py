# Generated from priveton.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .privetonParser import privetonParser
else:
    from privetonParser import privetonParser

# This class defines a complete generic visitor for a parse tree produced by privetonParser.

class privetonVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by privetonParser#program.
    def visitProgram(self, ctx:privetonParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by privetonParser#statement.
    def visitStatement(self, ctx:privetonParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by privetonParser#let_object.
    def visitLet_object(self, ctx:privetonParser.Let_objectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by privetonParser#let.
    def visitLet(self, ctx:privetonParser.LetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by privetonParser#show.
    def visitShow(self, ctx:privetonParser.ShowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by privetonParser#expr.
    def visitExpr(self, ctx:privetonParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by privetonParser#if_block.
    def visitIf_block(self, ctx:privetonParser.If_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by privetonParser#else_block.
    def visitElse_block(self, ctx:privetonParser.Else_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by privetonParser#while_block.
    def visitWhile_block(self, ctx:privetonParser.While_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by privetonParser#priority_opr.
    def visitPriority_opr(self, ctx:privetonParser.Priority_oprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by privetonParser#non_priority_opr.
    def visitNon_priority_opr(self, ctx:privetonParser.Non_priority_oprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by privetonParser#condition.
    def visitCondition(self, ctx:privetonParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by privetonParser#code_block.
    def visitCode_block(self, ctx:privetonParser.Code_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by privetonParser#un_opr.
    def visitUn_opr(self, ctx:privetonParser.Un_oprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by privetonParser#neg_opr.
    def visitNeg_opr(self, ctx:privetonParser.Neg_oprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by privetonParser#logic_opr.
    def visitLogic_opr(self, ctx:privetonParser.Logic_oprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by privetonParser#var.
    def visitVar(self, ctx:privetonParser.VarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by privetonParser#fun_def.
    def visitFun_def(self, ctx:privetonParser.Fun_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by privetonParser#func_call.
    def visitFunc_call(self, ctx:privetonParser.Func_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by privetonParser#class_def.
    def visitClass_def(self, ctx:privetonParser.Class_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by privetonParser#object_declaration.
    def visitObject_declaration(self, ctx:privetonParser.Object_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by privetonParser#outer_name.
    def visitOuter_name(self, ctx:privetonParser.Outer_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by privetonParser#return_call.
    def visitReturn_call(self, ctx:privetonParser.Return_callContext):
        return self.visitChildren(ctx)



del privetonParser