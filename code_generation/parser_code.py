from lark import Lark


def remove_white_space(code):
    # not sure if we want it
    return code


def get_parse_tree(code):
    code_without_whitespace = remove_white_space(code)
    return decaf_parser.parse(code_without_whitespace)


decaf_grammar = r"""
start: (declaration)+
declaration: variable_declaration
    | function_declaration
    | class_declaration
    | interface_declaration
variable_declaration: variable ";"
variable: type IDENTIFIER
type : TYPE | IDENTIFIER | type "[]"
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
    expr : l_value "=" expr -> assignment 
    | expr0
    expr0 : expr0 "||" expr1 -> or_bool 
    | expr1
    expr1 : expr1 "&&" expr2 -> and_bool 
    | expr2
    expr2 : expr2 "==" expr3 -> eq 
    | expr2 "!=" expr3 -> ne 
    | expr3
    expr3 : expr3 "<" expr4 -> lt 
    | expr3 "<=" expr4 -> le 
    | expr3 ">" expr4 -> gt 
    | expr3 ">=" expr4 -> ge 
    | expr4
    expr4 : expr4 "+" expr5 -> add 
    | expr4 "-" expr5 -> sub 
    | expr5
    expr5 : expr5 "*" expr6 -> mul 
    | expr5 "/" expr6 -> div 
    | expr5 "%" expr6 -> mod 
    | expr6
    expr6 : "-" expr6 -> neg 
    | "!" expr6 -> not_expr 
    | expr7
    expr7 : constant 
    | "ReadInteger" "(" ")" -> read_integer 
    | "ReadLine" "(" ")" -> read_line 
    | "new" IDENTIFIER -> class_inst 
    | "NewArray" "(" expr "," type ")" -> new_array 
    | "(" expr ")" 
    | l_value -> val 
    | call
    l_value : IDENTIFIER -> var_addr 
    |  expr7 "." IDENTIFIER -> var_access 
    | expr7 "[" expr "]" -> subscript
    call : IDENTIFIER  "(" actuals ")" 
    |  expr7  "."  IDENTIFIER "(" actuals ")" -> method
    actuals :  expr (","expr)* |  
    constant : INTEGER -> const_int 
    | DOUBLE -> const_double  
    | BOOL -> const_bool 
    | STRING -> const_str
    | "null" -> null

TYPE : "int" | "double" | "bool" | "string"

BOOL: "true" | "false"
INTEGER: /([-\+])?[0-9]+/
DOUBLE: /([-\+])?([0-9])+\.([0-9])*((E|e)(\+|\-)?([0-9])+)?/
IDENTIFIER: /(?!void|int|double|bool|string|true|false|class|interface|null|this|extends|implements|for|while|if|else|return|break|continue|new|NewArray|Print|ReadInteger|ReadLine|dtoi|itod|btoi|itob|private|protected|public)[a-zA-Z][_a-zA-Z0-9]*/
STRING : /"([^"\r\n]*)"/
INLINE_COMMENT : /\/\/.*/
COMMENT_END : /\*\/ / 
MULTILINE_COMMENT : /\/\* ([^{COMMENT_END}]*) \*\//
%ignore INLINE_COMMENT
%ignore MULTILINE_COMMENT
%import common.WS
%ignore WS
"""
decaf_parser = Lark(decaf_grammar, start="start", parser="lalr")
