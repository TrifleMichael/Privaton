grammar priveton;

program : statement+;

statement : (let | show | if_block | while_block | fun_def | expr) ';';

let    :  NAME '=' expr;
show     : 'print(' expr ')';
expr   : expr bin_opr expr | '('expr (bin_opr expr)?')' | var | '(' un_opr expr ')';

if_block: 'if' condition ':' code_block (else_block)? ;
else_block: 'else' code_block;
//for_block: 'for' NAME 'in' array ':' (code_block | statement);
while_block: 'while' condition ':' code_block;


condition: expr ;
code_block : '{' statement* '}';
un_opr : neg_opr ;
neg_opr : LOG_NEG_OPR | SUB_OPR;
bin_opr : logic_opr | arthm_opr;
logic_opr : AND_OPR | OR_OPR | '>' | '<' | '>=' | '<=' | '==' | '!=';
arthm_opr : ADD_OPR | SUB_OPR | DIV_OPR | MUL_OPR ;
var : NAME | INT | FLOAT | STRING | LOGIC | array;
array : '[' (expr',')* expr ']' | '['']';

fun_def : 'def' NAME'(' (var',')* var')' ':' code_block | 'def' NAME'('')' ':' code_block;

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
