from lark import Lark

decaf_grammar= r"""
start: (declaration)+
declaration: variable_declaration
    | function_declaration
    | class_declaration
    | interface_declaration
variable_declaration: variable ";"
variable: type IDENTIFIER
type: "int"
    | "double"
    | "bool"
    | "string"
    | IDENTIFIER
    | type "[]"
function_declaration: type IDENTIFIER "(" formals ")" stmt_block
    | "void" IDENTIFIER "(" formals ")" stmt_block
    | "static void" IDENTIFIER "(" formals ")" stmt_block
formals: variable ("," variable)*
    |
class_declaration: "class" IDENTIFIER ("extends" IDENTIFIER)? ("implements" IDENTIFIER ("," IDENTIFIER)*)? "{" (field)* "}"
field: access_mode variable_declaration
    |  access_mode function_declaration
access_mode: "private" 
    | "public"
    | "protected"
    |
interface_declaration: "interface" IDENTIFIER "{" (prototype)* "}"
prototype: type IDENTIFIER "(" formals ")" ";"
    | "void" IDENTIFIER "(" formals ")" ";"
    | "static void" IDENTIFIER "(" formals ")" ";"
stmt_block: "{" (variable_declaration)* (stmt)* "}"
stmt: (expr)? ";"
    | if_stmt
    | while_stmt
    | for_stmt
    | break_stmt
    | return_stmt
    | print_stmt
    | stmt_block
if_stmt: "if" "(" expr ")" stmt ("else" stmt)?
while_stmt: "while" "(" expr ")" stmt
for_stmt: "for" "(" (expr)? ";" expr ";" (expr)? ")" stmt
return_stmt: "return" (expr)? ";"
break_stmt: "break" ";"
print_stmt : "Print" "(" expr ("," expr)* ")" ";" 
expr : l_value "=" expr
    | constant
    | l_value
    | "this"
    | call
    | "(" expr ")"
    | expr "+" expr
    | expr "-" expr
    | expr "*" expr
    | expr "/" expr
    | expr "%" expr
    | "-" expr
    | expr "<" expr
    | expr "<=" expr
    | expr ">" expr
    | expr ">=" expr
    | expr "==" expr
    | expr "!=" expr
    | expr "&&" expr
    | expr "||" expr
    | "!" expr
    | "ReadInteger" "(" ")"
    | "ReadLine" "(" ")"
    | "new" IDENTIFIER
    | "NewArray" "(" expr "," type ")"
    | "itod" "(" expr ")"
    | "dtoi" "(" expr ")"
    | "itob" "(" expr ")"
    | "btoi" "(" expr ")"
l_value: IDENTIFIER
    | expr "." IDENTIFIER
    | expr "[" expr "]"
call: IDENTIFIER "(" actuals ")"
    | expr "." IDENTIFIER "(" actuals ")"
actuals:  expr ("," expr)*
    |
constant:  INTEGER
    | DOUBLE
    | BOOL
    | STRING
    | "null"
BOOL: "true"
    | "false"
INTEGER: /([-\+])?[0-9]+/
DOUBLE: /([-\+])?([0-9])+\.([0-9])*((E|e)(\+|\-)?([0-9])+)?/
IDENTIFIER: /[a-zA-Z][_a-zA-Z0-9]*/
STRING : /"([^"\r\n]*)"/
INLINE_COMMENT : /\/\/.*/
COMMENT_END : /\*\/ / 
MULTILINE_COMMENT : /\/\* ([^{COMMENT_END}]*) \*\//
%ignore INLINE_COMMENT
%ignore MULTILINE_COMMENT
%import common.WS
%ignore WS
"""
decaf_parser = Lark(decaf_grammar , start="start" , parser="lalr")