grammar priveton;

program : statement+;

statement : (let | show | if_block | while_block | fun_def | expr) ';';

let    :  (NAME | outer_name) '=' expr;
show     : 'print(' expr ')';
expr   : '('expr')' | expr priority_opr expr | expr non_priority_opr expr | var | '(' un_opr expr ')';

if_block: 'if' condition ':' code_block (else_block)? ;
else_block: 'else' code_block;
//for_block: 'for' NAME 'in' array ':' (code_block | statement);
while_block: 'while' condition ':' code_block;

priority_opr : MUL_OPR | DIV_OPR;
non_priority_opr : ADD_OPR | SUB_OPR | logic_opr;

condition: expr ;
code_block : '{' statement* '}';
un_opr : neg_opr ;
neg_opr : LOG_NEG_OPR | SUB_OPR;
logic_opr : AND_OPR | OR_OPR | '>' | '<' | '>=' | '<=' | '==' | '!=';
//arthm_opr : DIV_OPR | MUL_OPR |  ADD_OPR | SUB_OPR;
var : outer_name | NAME | INT | FLOAT | STRING | LOGIC | array;
array : '[' (expr',')* expr ']' | '['']';

fun_def : 'def' NAME'(' (var',')* var')' ':' code_block | 'def' NAME'('')' ':' code_block;
outer_name : 'parent::'NAME;

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
