import lark
from lark.visitors import Interpreter
from lark import Token
from parser_code import get_parse_tree
from symbol_table import SymbolTable, Scope, Symbol, Function, Class
from mips import *

# Typechecking... might move to a different file later.


class Type:
    double = "double"
    int = "int"
    bool = "bool"
    string = "string"
    array = "array"
    null = "null"


def is_primitive(type):
    return type in [Type.double, Type.string, Type.int, Type.bool]


def is_array(type):
    return not isinstance(type, str)


def convertible(type1, type2):  # type1 (Derived), type2 (Base)
    if is_primitive(type1) or is_primitive(type2):
        return type1 == type2

    if is_array(type1) or is_array(type2):
        return type1 == type2


class Cgen(Interpreter):
    label_counter = 0
    string_label = 0

    def new_label(self):
        self.label_counter += 1
        return str(self.label_counter)

    def new_string_label(self):
        self.string_label += 1
        return str(self.string_label)

    def __init__(self):
        super().__init__()
        self.current_scope = None
        self.loop_labels = []
        self._types = []
        self.symbol_table = SymbolTable()

    def start(self, tree):
        print('#### start the code generation')

        root = Scope('root')
        self.symbol_table.push_scope(root)

        return ''.join(self.visit_children(tree))

    def declaration(self, tree):
        code = ''
        for decl in tree.children:
            code += self.visit(decl)
        return code

    def class_declaration(self, tree):
        print('### class_declaration')
        ident = tree.children[0]  # its an IDENTIFIEER

        cur_scope = self.symbol_table.get_current_scope()
        class_scope = Scope(ident, [cur_scope])
        self.symbol_table.push_scope(class_scope)

        class_obj = Class(class_scope, ident)
        self.symbol_table.push_class(class_obj)

        self.visit_children(tree)

        self.symbol_table.pop_scope()

        return 'class'

    def extend(self, tree):
        print('### extend')
        cur_scope = self.symbol_table.get_current_scope()

        base_scope_name = tree.children[0].value
        base_scope = self.symbol_table.lookup_class(base_scope_name).scope

        cur_scope.add_parent_scope(base_scope)
        return None

    def implement(self, tree):
        print('### implement')  # for now we do not support interface
        interfaces = []
        for child in tree.children:
            interfaces.append(child.value)

    # todo - is incomplete (chera commentesh zard shod? cool!)
    def function_declaration(self, tree):
        code = ''
        if len(tree.children) == 4:
            return_type = self.visit(tree.children[0])
            ident = tree.children[1]
            formals = tree.children[2]
            stmt_block = tree.children[3]
        else:
            return_type = None  # function is void
            ident = tree.children[0]
            formals = tree.children[1]
            stmt_block = tree.children[2]

        cur_scope = self.symbol_table.get_current_scope()
        function_scope = Scope(ident, cur_scope)
        self.symbol_table.push_scope(function_scope)

        function_label = 'function_' + self.new_label()

        function_obj = Function(
            function_label, function_scope, ident, return_type)
        self.symbol_table.push_function(function_obj)

        if ident == 'main':  # ????
            code += self.declare_global_static_funcs()
            code += mips_label('main')
        else:
            code += mips_label(function_label)  # just for testing... its BS

        # code += self.visit(tree.children[0])
        code += self.visit(formals)
        code += self.visit(stmt_block)

        self.symbol_table.pop_scope()
        return code

    def variable_declaration(self, tree):  # todo - is incomplete
        code = ''
        code += ''.join(self.visit_children(tree))
        return code

    def variable(self, tree):
        print('### variable')
        code = ''
        variable_type = self.visit(tree.children[0])
        variable_name = tree.children[1]
        symbol = Symbol(variable_name, variable_type)
        self.symbol_table.push_symbol(symbol)
        # mips code to push to stack
        return code

    def formals(self, tree):
        code = ''
        if tree.children:
            # formals will be pushed to stack
            code += self.visit_children(tree)
        return code

    def type(self, tree):
        return tree.children[0].value

    def stmt_block(self, tree):  # todo - is incomplete
        code = ''
        # print('#### start stmt')
        if(len(tree.children) != 0):
            child = tree.children[0]
            stmt_label = self.new_label()
            child._meta = stmt_label
            code += self.visit(tree.children[0])
            code += self.visit(tree.children[1])
        return code

    def expr(self, tree):
        print("#### EXPR")
        return ''.join(self.visit_children(tree))

    def expr0(self, tree):
        return ''.join(self.visit_children(tree))

    def expr1(self, tree):
        return ''.join(self.visit_children(tree))

    def expr2(self, tree):
        return ''.join(self.visit_children(tree))

    def expr3(self, tree):
        return ''.join(self.visit_children(tree))

    def expr4(self, tree):
        return ''.join(self.visit_children(tree))

    def expr5(self, tree):
        return ''.join(self.visit_children(tree))

    def expr6(self, tree):
        return ''.join(self.visit_children(tree))

    def expr7(self, tree):
        code = ''
        more_code = self.visit_children(tree)
        if len(more_code) == 0:
            return code
        return ''.join(more_code)

    def assignment(self, tree):  # todo - figure out how to do the type checking(WHAT is dimension?)
        print("#### ASS")
        code = ''.join(self.visit_children(tree))
        operand_type = self._types[-1]
        if operand_type == Type.double:  # and typ.dimension == 0:
            code += mips_text()
            # sp+8 is stored in t0 -- why?
            code += mips_load('$t0', '$sp', offset=8)
            code += mips_load_double('$f0', '$sp')
            # f0 is stored in where t0 is pointing to -- why??
            code += mips_store_double('$f0', '$t0')
            code += mips_store_double('$f0', '$sp', offset=8)
            code += add_stack(8)
        else:  # int, bool
            code += mips_text()
            code += mips_load('$t0', '$sp', offset=8)
            code += mips_load('$t1', '$sp')
            code += mips_store('$t1', '$t0')
            code += mips_store('$t1', '$sp', offset=8)
            code += add_stack(8)
        self._types.pop()
        return code

    def class_inst(self, tree):  # todo
        return 'class_inst'

    def var_addr(self, tree):
        code = ''
        var_name = tree.children[0].value
        var_value = self.symbol_table.lookup_symbol(var_name)
        # mips code to assign
        return code

    def var_access(self, tree):  # todo
        return 'var_access'

    def val(self, tree):  # todo - dimension chie namoosan
        print("#### val code gen")
        print(len(tree.children))
        code = ''.join(self.visit_children(tree))
        operand_type = self._types[-1]
        if operand_type == Type.double:  # and typ.dimension == 0:
            code += mips_text()
            code += mips_load('$t0', '$sp')
            code += mips_load_double('$f0', '$t0')
            code += mips_store_double('$f0', '$sp')
        else:  # bool, int
            code += mips_text()
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$t0')
            code += mips_store('$t1', '$sp')
        return code

    def print_stmt(self, tree):  # todo - not sure about the type checking
        code = mips_text()
        for child in tree.children[0].children:
            code += self.visit(child)
            operand_type = self._types.pop()
            if operand_type == Type.double:
                code += print_double()
            elif operand_type == Type.int:
                code += print_int()
            elif operand_type == Type.string:
                code += print_string()
            elif operand_type == Type.bool:  # and t.dimension == 0:
                label_num = self.new_label()
                code += print_bool(label_num)
        code += print_newline()
        return code

    def new_array(self, tree):  # todo - add the typechecking
        code = ''.join(self.visit_children(tree))
        # TYPECHECKING: NEEDS TO BE CHANGED.
        shamt = 2  # shift amount?!
        tp = tree.children[1].children[0]
        if type(tp) == lark.lexer.Token:
            if tp.value == Type.double:
                shamt = 3
        code += mips_new_array(shamt)
        # add to self._types?
        return code

    def l_value(self, tree):
        return ''.join(self.visit_children(tree))

    def const_int(self, tree):
        code = ''
        code += mips_text()
        const_val = tree.children[0].value.lower()
        code += mips_li('$t0', const_val)
        code += sub_stack(8)
        code += mips_store('$t0', '$sp')
        self._types.append(Type.int)
        return code

    def const_bool(self, tree):
        code = mips_text()
        const_val = tree.children[0].value.lower()
        numerical_val = 0
        if const_val == 'true':
            numerical_val = 1
        code += mips_li('$t0', numerical_val)
        code += sub_stack(8)
        code += mips_store('$t0', '$sp')
        self._types.append(Type.bool)
        return code

    def const_string(self, tree):
        code = ''
        code += mips_data()
        code += mips_align(2)
        str_val = tree.children[0].value
        string_num = self.new_string_label()
        string_name = '__string__' + string_num
        code += string_name + ':'
        code += mips_asciiz(str_val)
        code += mips_text()
        code += mips_load_address('$t0', string_name)
        code += sub_stack(8)
        code += mips_store('$t0', '$sp')
        self._types.append(Type.string)
        return code

    def null(self, tree):
        code = mips_text()
        code += sub_stack(8)
        code += mips_store('$zero', '$sp')
        code += mips_store('$zero', '$sp')
        self._types.append(Type.null)
        return code

    def mul(self, tree):
        code = ''.join(self.visit_children(tree))
        operand_type = self._types.pop()
        if operand_type == Type.int:
            code += mips_text()
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            code += mips_mul('$t2', '$t1', '$t0')
            code += mips_store(src='$t2', dst='$sp', offset=8)
            code += add_stack(8)
        # double type --- use coprocessor. $f0-$f31 registers. Only use even numbered ones.
        elif operand_type == Type.double:
            code += mips_text()
            code += mips_load_double('$f0', '$sp')
            code += mips_load_double('$f2', '$sp', offset=8)
            code += mips_mul_double('$f4', '$f2', '$f0')
            code += mips_store_double('$f4', '$sp', offset=8)
            code += add_stack(8)
        return code

    def mod(self, tree):
        code = ''.join(self.visit_children(tree))
        operand_type = self._types.pop()
        if operand_type == Type.int:
            code += mips_text()
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            code += mips_div('$t2', '$t1', '$t0')
            code += 'mfhi $t2\n'
            code += mips_store(src='$t2', dst='$sp', offset=8)
            code += add_stack(8)

        return code

    def div(self, tree):
        code = ''.join(self.visit_children(tree))
        operand_type = self._types.pop()
        if operand_type == Type.int:
            code += mips_text()
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            code += mips_div('$t2', '$t1', '$t0')
            code += 'mflo $t2\n'
            code += mips_store(src='$t2', dst='$sp', offset=8)
            code += add_stack(8)
        # double type --- use coprocessor. $f0-$f31 registers. Only use even numbered ones.
        elif operand_type == Type.double:
            code += mips_text()
            code += mips_load_double('$f0', '$sp')
            code += mips_load_double('$f2', '$sp', offset=8)
            code += mips_div_double('$f4', '$f2', '$f0')
            code += mips_store_double('$f4', '$sp', offset=8)
            code += add_stack(8)
        return code

    def add(self, tree):
        code = ''.join(self.visit_children(tree))
        operand_type = self._types.pop()
        if operand_type == Type.int:
            code += mips_text()
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            code += mips_add('$t2', '$t0', '$t1')
            code += mips_store(src='$t2', dst='$sp', offset=8)
            code += add_stack(8)
        # double type --- use coprocessor. $f0-$f31 registers. Only use even numbered ones.
        elif operand_type == Type.double:
            code += mips_text()
            code += mips_load_double('$f0', '$sp')
            code += mips_load_double('$f2', '$sp', offset=8)
            code += mips_add_double('$f4', '$f0', '$f2')
            code += mips_store_double('$f4', '$sp', offset=8)
            code += add_stack(8)
        return code

    def sub(self, tree):
        code = ''.join(self.visit_children(tree))
        operand_type = self._types.pop()
        if operand_type == Type.int:
            code += mips_text()
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            code += mips_sub('$t2', '$t1', '$t0')
            code += mips_store(src='$t2', dst='$sp', offset=8)
            code += add_stack(8)
        # double type --- use coprocessor. $f0-$f31 registers. Only use even numbered ones.
        elif operand_type == Type.double:
            code += mips_text()
            code += mips_load_double('$f0', '$sp')
            code += mips_load_double('$f2', '$sp', offset=8)
            code += mips_sub_double('$f4', '$f2', '$f0')
            code += mips_store_double('$f4', '$sp', offset=8)
            code += add_stack(8)
        return code

    def and_bool(self, tree):
        code = ''.join(self.visit_children(tree))
        code += mips_text()
        code += mips_load('$t0', '$sp')
        code += mips_load('$t0', '$sp', offset=8)
        code += mips_and('$t2', '$t0', '$t1')
        code += mips_store('$t2', '$sp', offset=8)
        code += add_stack(8)
        self._types.pop()
        self._types.pop()
        self._types.append(Type.bool)
        return code

    def or_bool(self, tree):
        code = ''.join(self.visit_children(tree))
        code += mips_text()
        code += mips_load('$t0', '$sp')
        code += mips_load('$t0', '$sp', offset=8)
        code += mips_or('$t2', '$t0', '$t1')
        code += mips_store('$t2', '$sp', offset=8)
        code += add_stack(8)
        self._types.pop()
        self._types.pop()
        self._types.append(Type.bool)
        return code

    def eq(self, tree):
        code = ''.join(self.visit_children(tree))
        type = self._types.pop()
        if type == Type.double:  # and typ.dimension == 0: #todo - no clue what type dimension is!!!
            label_number = self.new_label()
            label = '__d_eq__' + label_number
            code += mips_text()
            code += mips_load_double('$f0', '$sp')
            code += mips_load_double('$f2', '$sp', offset=8)
            code += mips_li('$t0', 0)
            # special floating point coprocessor instruction, checks equality
            code += 'c.eq.d $f0, $f2\n'
            code += 'bc1f ' + label + '\n'
            # bc1f is a flag that stores equality operation result. if eq is false it jumps to label.
            code += mips_li('$t0', 1)
            code += label + ':\n'
            code += add_stack(8)
            code += mips_store('$t0', '$sp')
        elif type == Type.string:  # and typ.dimension == 0: todo - we need to implement STRCMP
            code += '.text\n'
            code += '\tsw $t0, -8($sp)\n'
            code += '\tsw $t1, -8($sp)\n'
            code += '\tsw $a0, -12($sp)\n'
            code += '\tsw $a1, -16($sp)\n'
            code += '\tsw $v0, -20($sp)\n'
            code += '\tsw $ra, -24($sp)\n'
            code += '\tlw $a0, 0($sp)\n'
            code += '\tlw $a1, 8($sp)\n'
            code += '\tjal __strcmp__\n'
            code += '\tsw $v0, 8($sp)\n'
            code += '\tlw $t0, -4($sp)\n'
            code += '\tlw $t1, -8($sp)\n'
            code += '\tlw $a0, -12($sp)\n'
            code += '\tlw $a1, -16($sp)\n'
            code += '\tlw $v0, -20($sp)\n'
            code += '\tlw $ra, -24($sp)\n'
            code += '\taddi $sp, $sp, 8\n\n'
        else:  # int, bool    #done i think
            code += mips_text()
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            # special equality checking operation - will set t2 = 1 if t1 == t0
            code += 'seq $t2, $t1, $t0\n'
            code += add_stack(8)
            code += mips_store('$t2', '$sp')
        self._types.pop()
        self._types.append(Type.bool)
        return code

    def gt(self, tree):
        code = ''.join(self.visit_children(tree))
        operand_type = self._types.pop()
        if operand_type == Type.int:
            code += mips_text()
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            code += 'sgt $t2, $t1, $t0\n'  # special data comparison instruction
            code += add_stack(8)
            code += mips_store('$t2', '$sp')
        if operand_type == Type.double:
            label_number = self.new_label()
            label = '__d_gt__' + label_number
            code += mips_text()
            code += mips_load_double('$f0', '$sp')
            code += mips_load_double('$f2', '$sp', offset=8)
            code += mips_li('$t0', 0)
            code += 'c.gt.d $f2, $f0\n'  # if gt is false, will jump to label
            code += 'bc1f ' + label
            code += mips_li('$t0', 1)  # will reach this code if gt is true
            code += label + ':\n'
            code += add_stack(8)
            code += mips_store('$t0', '$sp')
        self._types.pop()
        self._types.append(Type.bool)
        return code

    def ge(self, tree):
        code = ''.join(self.visit_children(tree))
        operand_type = self._types.pop()
        if operand_type == Type.int:
            code += mips_text()
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            code += 'sge $t2, $t1, $t0\n'  # special data comparison instruction
            code += add_stack(8)
            code += mips_store('$t2', '$sp')
        if operand_type == Type.double:
            label_number = self.new_label()
            label = '__d_ge__' + label_number
            code += mips_text()
            code += mips_load_double('$f0', '$sp')
            code += mips_load_double('$f2', '$sp', offset=8)
            code += mips_li('$t0', 0)
            code += 'c.ge.d $f2, $f0\n'  # if ge is false, will jump to label
            code += 'bc1f ' + label
            code += mips_li('$t0', 1)  # will reach this code if ge is true
            code += label + ':\n'
            code += add_stack(8)
            code += mips_store('$t0', '$sp')
        self._types.pop()
        self._types.append(Type.bool)
        return code

    def lt(self, tree):
        code = ''.join(self.visit_children(tree))
        operand_type = self._types.pop()
        if operand_type == Type.int:
            code += mips_text()
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            code += 'slt $t2, $t1, $t0\n'  # special data comparison instruction
            code += add_stack(8)
            code += mips_store('$t2', '$sp')
        if operand_type == Type.double:
            label_number = self.new_label()
            label = '__d_lt__' + label_number
            code += mips_text()
            code += mips_load_double('$f0', '$sp')
            code += mips_load_double('$f2', '$sp', offset=8)
            code += mips_li('$t0', 0)
            code += 'c.lt.d $f2, $f0\n'  # if lt is false, will jump to label
            code += 'bc1f ' + label
            code += mips_li('$t0', 1)  # will reach this code if lt is true
            code += label + ':\n'
            code += add_stack(8)
            code += mips_store('$t0', '$sp')
        self._types.pop()
        self._types.append(Type.bool)
        return code

    def le(self, tree):
        code = ''.join(self.visit_children(tree))
        operand_type = self._types.pop()
        if operand_type == Type.int:
            code += mips_text()
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            code += 'sle $t2, $t1, $t0\n'  # special data comparison instruction
            code += add_stack(8)
            code += mips_store('$t2', '$sp')
        if operand_type == Type.double:
            label_number = self.new_label()
            label = '__d_le__' + label_number
            code += mips_text()
            code += mips_load_double('$f0', '$sp')
            code += mips_load_double('$f2', '$sp', offset=8)
            code += mips_li('$t0', 0)
            code += 'c.le.d $f2, $f0\n'  # if le is false, will jump to label
            code += 'bc1f ' + label
            code += mips_li('$t0', 1)  # will reach this code if le is true
            code += label + ':\n'
            code += add_stack(8)
            code += mips_store('$t0', '$sp')
        self._types.pop()
        self._types.append(Type.bool)
        return code

    # operation for getting opposite of a bool value.
    def not_bool(self, tree):
        code = ''.join(self.visit_children(tree))
        label_number = self.new_label()
        label = '__not__' + label_number
        code += mips_text()
        code += mips_load('$t0', '$sp')
        code += add_stack(8)
        code += mips_li('$t1', 1)
        # if t0 is 0, t0not is 1 so jumps to label.
        code += mips_beq('$t0', '$zero', label)
        # reaches this code if t0 is 1 ---> t0not set to 0
        code += mips_li('$t1', 0)
        code += label + ':\n'
        code += sub_stack(8)
        code += mips_store('$t1', '$sp')
        self._types.pop()
        self._types.append(Type.bool)
        return code

    def neg(self, tree):
        code = ''.join(self.visit_children(tree))
        operand_type = self._types[-1]
        if operand_type == Type.int:
            code += mips_text()
            code += mips_load('$t0', '$sp')
            code += mips_sub('$t0', '$zero', '$t0')
            code += mips_store('$t0', '$sp')
        elif operand_type == Type.double:
            code += mips_load_double('$f0', '$sp')
            code += 'ng.d $f0, $f0\n'  # special FP instruction for negating double
            code += mips_store('$f0', '$sp')
        return code

    def actuals(self, tree):
        return 'actuals'

    def method(self, tree):
        return 'METH'

    def call(self, tree):
        return 'CALL'

    def subscript(self, tree):
        return 'subs_ '

    def stmt(self, tree):  # todo - very incomplete
        code = ''
        print('#### start stmt')
        child = tree.children[0]
        stmt_label = self.new_label()
        child._meta = stmt_label
        code += self.visit(child)
        return code

    def if_stmt(self, tree):  # todo - i have no clue
        print('### start if_stmt')
        expr = tree.children[0]
        self.visit(expr)
        stmt = tree.children[1]
        self.visit(stmt)
        hasElse = len(tree.children) != 2
        if not hasElse:
            # generate if(expr){stmt;} code
            None
        else:
            else_stmt = tree.children[2]
            self.visit(else_stmt)
            # generate if(expr){stmt;}else{stmt;} code
            None
        return None

    def for_stmt(self, tree):  # todo - i have no clue
        print('### start for_stmt')
        for_label = tree._meta
        self.loop_labels.append(for_label)
        expr1 = tree.children[0]
        self.visit(expr1)
        expr2 = tree.children[1]
        self.visit(expr2)
        expr3 = tree.children[2]
        self.visit(expr3)
        # generate for(expr;expr;expr){stmt;} code
        self.loop_labels.pop()
        return None

    def while_stmt(self, tree):  # todo - i have no clue
        print('### start while_stmt')
        while_label = tree._meta
        print(while_label)
        self.loop_labels.append(while_label)
        expr = tree.children[0]
        self.visit(expr)
        stmt = tree.children[1]
        self.visit(stmt)
        # generate for(expr;expr;expr){stmt;} code
        self.loop_labels.pop()
        return None

    def declare_global_static_funcs(self):
        code = ''
        code += mips_itod()
        code += mips_itob()
        code += mips_dtoi()
        code += mips_btoi()
        code += mips_str_cmp()
        return code


if_test_code = """
int main() {
    int a;
    a = 1;
    if(true){
        int a;
        a = 1;
    }
}
"""
for_test_code = """
int main() {
    int i;
    for(i = 0; i < 10; i = i+1){
        Print(i);
   }
}
"""

while_test_code = """
int main() {
    int i;
    i = 0;
    while (i < 5) {
        Print(i);
        i = i + 1;
    }
}
"""

function_test_code = '''
int func(int a, int b){
    return a;
}
'''

class_test_code = '''
class test_extends{

}
class test_class extends test_extends implements test_implement, test_implement2{
    private int a;
    protected int b;
    public int c;

    private int function1(bool a){

    }
    protected int function2(bool a){

    }
    public int function3(bool a){

    }
}
'''

shit_test_code = '''
bool main(){
int fuck;
fuck = 5 + 5;
}

int add(){

}
'''

if __name__ == '__main__':
    tree = get_parse_tree(shit_test_code)
    print(tree.pretty())
    code = ''
    code += str(Cgen().visit(tree))
    print("CODE:")
    print(code)

'''  def expr(self, tree):
        print('#### start expr')
        self.visit_children(tree)
        print(tree.children)
        return 'expression' '''
