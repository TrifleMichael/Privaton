grammar priveton;

program : statement+;

statement : (let | show | if_block | while_block | fun_def | expr | return_call | class_def | let_object | let_object_variable) ';';

let_object : NAME '=' object_declaration;
let_object_variable : NAME'.'NAME '=' expr;
let    :  (NAME | outer_name) '=' expr;
show     : 'print(' expr (',' expr)* ')';
expr   : '('expr')' | expr priority_opr expr | expr non_priority_opr expr | var | '(' un_opr expr ')';

if_block: 'if' condition ':' code_block (else_block)? ;
else_block: 'else' code_block;
while_block: 'while' condition ':' code_block;

priority_opr : MUL_OPR | DIV_OPR;
non_priority_opr : ADD_OPR | SUB_OPR | logic_opr;

condition: expr ;
code_block : '{' statement* '}';
un_opr : neg_opr ;
neg_opr : LOG_NEG_OPR | SUB_OPR;
logic_opr : AND_OPR | OR_OPR | '>' | '<' | '>=' | '<=' | '==' | '!=';
//arthm_opr : DIV_OPR | MUL_OPR |  ADD_OPR | SUB_OPR;
var : outer_name | NAME | INT | FLOAT | STRING | LOGIC | func_call | object_variable_call ;

fun_def : 'def' NAME'(' (var',')* var')' ':' code_block | 'def' NAME'():' code_block;
func_call : NAME'(' (var',')* var')' | NAME'()';

class_def : 'class' NAME ':' code_block;
object_declaration : 'class.' NAME;
object_variable_call : NAME'.'NAME;

outer_name : 'parent::'NAME;
return_call : 'return' expr;

AND_OPR: 'and';
OR_OPR: 'or';

LOGIC : 'True' | 'False' ;
LOG_NEG_OPR : '!';
ADD_OPR : '+';
SUB_OPR : '-';
DIV_OPR : '/';
MUL_OPR : '*';
NAME     : [a-zA-Z] ([a-zA-Z0-9] | '_')*;
INT : [1-9]+[0-9]* | [0] ;
FLOAT : INT'.'[0-9]+ ;
STRING : '"'(.)*?'"';
WS     : [ \r\n\t]+ -> skip;
