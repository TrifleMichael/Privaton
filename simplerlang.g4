grammar simplerlang;

program : statement+;

statement : (let | show | if_block | for_block | fun_def) ';';

let    :  NAME '=' large_expr;
show     : 'print(' large_expr ')';
large_expr   : small_expr (bin_opr small_expr)* | '('small_expr (bin_opr small_expr)*')';
small_expr   : (var | un_opr) (bin_opr small_expr)* | '('(var | un_opr) (bin_opr small_expr)*')';

if_block: 'if' large_expr ':' (code_block | statement);
for_block: 'for' NAME 'in' array ':' (code_block | statement);

code_block : '{' statement* '}';
un_opr : neg_opr ;
neg_opr : NEG_OPR small_expr; // indirect leftside recursion
bin_opr : logic_opr | arthm_opr;
logic_opr : 'and' | 'or' | '>' | '<' | '>=' | '<=' | '==' | '!=';
arthm_opr : ADD_OPR | SUB_OPR | DIV_OPR | MUL_OPR ;
var : NAME | INT | FLOAT | STRING ;
array : '[' (var',')* var ']' | '['']';

fun_def : 'def' NAME'(' (var',')* var')' ':' code_block | 'def' NAME'('')' ':' code_block;

NEG_OPR : '!';
ADD_OPR : '+';
SUB_OPR : '-';
DIV_OPR : '/';
MUL_OPR : '*';
NAME     : [a-zA-Z] ([a-zA-Z0-9] | '_')*;
INT : '-'*[1-9]+[0-9]* | [0] ;
FLOAT : INT'.'[0-9]+ ;
STRING : '"'(.)*?'"';
WS     : [ \n\t]+ -> skip;
