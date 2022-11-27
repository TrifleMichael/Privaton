grammar simplerlang;

program : statement+;

statement : (let | show | if_block | while_block | fun_def) ';';

let    :  NAME '=' large_expr;
show     : 'print(' large_expr ')';
//large_expr   : small_expr (bin_opr small_expr)* | '('small_expr (bin_opr small_expr)*')';
//large_expr   : var (bin_opr large_expr)? | '('var (bin_opr large_expr)?')'; // need to add back unary operations
large_expr   : small_expr (bin_opr large_expr)? | '('small_expr (bin_opr large_expr)?')';
small_expr   : var (bin_opr small_expr)? | '('var (bin_opr small_expr)?')';

if_block: 'if' condition ':' code_block;
//for_block: 'for' NAME 'in' array ':' (code_block | statement);
while_block: 'while' condition ':' code_block;


condition: large_expr ;
code_block : '{' statement* '}';
un_opr : neg_opr ;
neg_opr : NEG_OPR large_expr; // indirect leftside recursion
bin_opr : logic_opr | arthm_opr;
logic_opr : AND_OPR | OR_OPR | '>' | '<' | '>=' | '<=' | '==' | '!=';
arthm_opr : ADD_OPR | SUB_OPR | DIV_OPR | MUL_OPR ;
var : NAME | INT | FLOAT | STRING | LOGIC | array;
array : '[' (large_expr',')* large_expr ']' | '['']';

fun_def : 'def' NAME'(' (var',')* var')' ':' code_block | 'def' NAME'('')' ':' code_block;

AND_OPR: 'and';
OR_OPR: 'or';
//MORE_OPR: '>';

LOGIC : 'True' | 'False' ;
NEG_OPR : '!';
ADD_OPR : '+';
SUB_OPR : '-';
DIV_OPR : '/';
MUL_OPR : '*';
NAME     : [a-zA-Z] ([a-zA-Z0-9] | '_')*;
INT : '-'*[1-9]+[0-9]* | [0] ;
FLOAT : INT'.'[0-9]+ ;
STRING : '"'(.)*?'"';
WS     : [ \r\n\t]+ -> skip;
