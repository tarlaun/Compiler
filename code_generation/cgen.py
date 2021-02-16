import lark
from lark.visitors import Interpreter
from lark import Token
from parser_code import get_parse_tree
from symbol_table import SymbolTable, Scope, Symbol, Function, Class
from mips import *
from Error import *

# Typechecking... might move to a different file later.


class Type:
    def __init__(self, name, dimension=0):
        self.name = name
        self.dimension = dimension
    double = "double"
    int = "int"
    bool = "bool"
    string = "string"
    array = "array"
    null = "null"

    def is_primitive(self):
        return self.name in [Type.double, Type.string, Type.int, Type.bool]


def is_array(type):
    return not isinstance(type, str)


def convertible(type1, type2):  # type1 (Derived), type2 (Base)
    if type1.is_primitive() or type2.is_primitive():
        return type1 == type2

    if is_array(type1) or is_array(type2):
        return type1 == type2


class Cgen(Interpreter):
    label_counter = 0
    string_label = 0
    stmt_block_counter = 0
    varible_label_counter = 0
    loop_counter = 0
    array_last_type = None

    def new_variable_label(self):
        self.varible_label_counter += 1
        # fix this
        return 'var_'+str(self.varible_label_counter)

    def new_stmt_block_label(self):
        self.stmt_block_counter += 1
        return 'stmt_block_'+str(self.stmt_block_counter)

    def new_label(self):
        self.label_counter += 1
        return 'll_'+str(self.label_counter)

    def new_loop_label(self):
        self.loop_counter += 1
        return 'loop_label_' + str(self.loop_counter)

    def new_string_label(self):
        self.string_label += 1
        return 'str_'+str(self.string_label)

    def __init__(self):
        super().__init__()
        self.loop_labels = []
        self._types = []
        self.symbol_table = SymbolTable()
        self.data = DataSection()

    def start(self, tree):
        print('#### start the code generation')

        root = Scope('root')
        self.symbol_table.push_scope(root)

        code = ''.join(self.visit_children(tree))
        code += self.declare_global_static_funcs()
        return code

    def declaration(self, tree):
        code = ''
        for decl in tree.children:
            code += self.visit(decl)
        return code

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

        code += self.visit(formals)

        cur_scope = self.symbol_table.get_current_scope()
        function_scope = Scope(ident, cur_scope)
        self.symbol_table.push_scope(function_scope)

        function_data = Function(function_scope, ident, return_type)
        self.symbol_table.push_function(function_data)

        # set function label
        # function_data.set_label(label)

        if ident == 'main':  # ????
            code += ('main:\n')
        else:
            code += mips_create_label(str(function_scope))
        code += sub_stack(8)
        code += mips_store('$ra', '$sp')
        # code += self.visit(ident)
        code += self.visit(stmt_block)
        code += mips_load('$ra', '$sp', 0)
        code += add_stack(8)
        self.symbol_table.pop_scope()
        if ident == 'main':
            code += mips_jr('$ra')
        return code

    def variable_declaration(self, tree):
        code = ''
        code += ''.join(self.visit_children(tree))
        return code

    def variable(self, tree):
        print('### variable')
        code = ''
        variable_type = Type(self.visit(tree.children[0]), 0)
        variable_name = tree.children[1]
        label = self.new_variable_label()
        self.data.add_data(label + ':\n' + mips_align(2) + '.space 4\n')
        symbol = Symbol(variable_name, variable_type,
                        scope=self.symbol_table.get_current_scope(), label=label)
        self.symbol_table.push_symbol(symbol)
        # mips code to push to stack ==> probably not
        return code

    def formals(self, tree):
        code = ''
        parent_scope = self.symbol_table.get_current_scope()
        current_scope = Scope('formals', parent_scope)
        self.symbol_table.push_scope(current_scope)

        for variable in tree.children:
            formal_name = variable.children[1].value
            formal_type = Type(variable.children[0])
            code += '.data\n'
            code += '.align 2\n'
            if formal_type.name == Type.double and formal_type.dimension == 0:
                code += '{}: .space 8\n'.format(
                    (str(self.symbol_table.get_current_scope()) + "/" + formal_name).replace("/", "_"))
            else:
                code += '{}: .space 4\n'.format(
                    (str(self.symbol_table.get_current_scope()) + "/" + formal_name).replace("/", "_"))
        return code

    def type(self, tree):
        if type(tree.children[0]) == lark.lexer.Token:
            self.array_last_type = Type(tree.children[0])
        else:
            self.visit(tree.children[0])
            self.array_last_type.dimension += 1
        return tree.children[0].value

    def stmt_block(self, tree):
        parent_scope = self.symbol_table.get_current_scope()
        label = self.new_stmt_block_label()
        current_scope = Scope(label, parent_scope)
        self.stmt_block_counter += 1
        self.symbol_table.push_scope(current_scope)
        code = ''.join(self.visit_children(tree))
        self.symbol_table.pop_scope()
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

    def assignment(self, tree):  # todo - type checking - array
        code = ''.join(self.visit_children(tree))

        variable_type = self._types[-1]
        if variable_type.name == Type.double:  # and typ.dimension == 0:
            code += mips_load('$t0', '$sp', offset=8)  # label address
            code += mips_load_double('$f0', '$sp')  # value to be assigned
            code += mips_store_double('$f0', '$t0')  # save value in the label
            # save value in the top of stack
            code += mips_store_double('$f0', '$sp', offset=8)
            code += add_stack(8)
        else:  # int, bool
            code += mips_load('$t0', '$sp', offset=8)
            code += mips_load('$t1', '$sp')
            code += mips_store('$t1', '$t0')
            code += mips_store('$t1', '$sp', offset=8)
            code += add_stack(8)
        code += add_stack(8)
        self._types.pop()
        return code

    def class_inst(self, tree):  # todo
        return 'class_inst'

    def var_addr(self, tree):  # finds variable label and push it to stack
        code = ''
        var_name = tree.children[0].value
        symbol = self.symbol_table.lookup_symbol(var_name)
        print('### symbol', str(symbol.type.name))
        label = symbol.label
        code = ''
        code += mips_load_address('$t0', label=label)
        code += sub_stack(8)
        code += mips_store('$t0', '$sp')
        self._types.append(symbol.type)
        return code

    def var_access(self, tree):  # todo
        return 'var_access'

    def val(self, tree):  # todo = dimension
        print("#### val code gen")
        code = ''.join(self.visit_children(tree))
        operand_type = self._types[-1]
        if operand_type.name == Type.double:  # and typ.dimension == 0:
            code += mips_load('$t0', '$sp')
            code += mips_load_double('$f0', '$t0')
            code += mips_store_double('$f0', '$sp')
        else:  # bool, int
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$t0')
            code += mips_store('$t1', '$sp')
        return code

    def print_stmt(self, tree):  # todo - not sure about the type checking
        print('### print_stmt')
        code = ''
        for child in tree.children[0].children:
            code += self.visit(child)
            operand_type = self._types.pop()
            print('#type:', operand_type.name)
            if operand_type.name == Type.double:
                code += mips_jal(mips_get_label('print double'))
            elif operand_type.name == Type.int:
                code += mips_jal(mips_get_label('print integer'))
            elif operand_type.name == Type.string:
                code += mips_jal(mips_get_label('print string'))
            elif operand_type.name == Type.bool:  # and t.dimension == 0:
                code += mips_jal(mips_get_label('print bool'))
        code += mips_jal(mips_get_label('print new line'))
        return code

    def new_array(self, tree):  # todo - add the typechecking
        array_type = self.visit(tree.children[1])
        code = ''.join(self.visit(tree.children[0]))
        shamt = 2
        tp = self.array_last_type
        if tp.is_primitive and tp.dimension == 0:
            if tp.name == Type.double:
                shamt = 3
        length_type = self._types.pop()
        if length_type.name != 'int' or length_type.dimension != 0:
            raise(TypeError('Invalid length type for NewArray()'))

        code += sub_stack(8)
        code += mips_load_immidiate('$a0', shamt)
        code += mips_store('$a0', '$sp', 0)
        code += mips_jal(mips_get_label('new array'))
        self._types.append(Type(self.array_last_type.name,
                                self.array_last_type.dimension+1))
        return code

    def read_line(self, tree):
        code = ''.join(self.visit_children(tree))
        code += mips_jal(mips_get_label('read line'))
        self._types.append(Type(Type.string, 0))
        return code

    def read_integer(self, tree):
        code = ''.join(self.visit_children(tree))
        code += mips_jal(mips_get_label('read integer'))
        self._types.append(Type(Type.int, 0))
        return code

    def l_value(self, tree):
        return ''.join(self.visit_children(tree))

    def const_int(self, tree):
        print('#### const_int')
        code = ''
        const_val = tree.children[0].value.lower()
        code += mips_li('$t0', const_val)
        code += sub_stack(8)
        code += mips_store('$t0', '$sp')
        self._types.append(Type(Type.int, dimension=0))
        return code

    def const_double(self, tree):
        code = ''
        const_val = tree.children[0].value.lower()
        code += 'li.s $f0 , {}\n'.format(const_val)
        code += sub_stack(8)
        code += mips_store_double('$f0', '$sp')
        self._types.append(Type(Type.double, dimension=0))
        return code

    def const_bool(self, tree):
        code = ''
        const_val = tree.children[0].value.lower()
        numerical_val = 0
        if const_val == 'true':
            numerical_val = 1
        code += mips_li('$t0', numerical_val)
        code += sub_stack(8)
        code += mips_store('$t0', '$sp')
        self._types.append(Type(Type.bool))
        return code

    def const_string(self, tree):
        code = ''
        str_val = tree.children[0].value
        string_label = self.new_string_label()

        codeData = string_label + ':'
        codeData += mips_asciiz(str_val)
        self.data.add_data(codeData)
        code += mips_load_address('$t0', string_label)
        code += sub_stack(8)
        code += mips_store('$t0', '$sp')
        self._types.append(Type(Type.string))
        return code

    def null(self, tree):
        code = ''
        code += sub_stack(8)
        code += mips_store('$zero', '$sp')
        self._types.append(Type(Type.null))
        return code

    def mul(self, tree):
        code = ''.join(self.visit_children(tree))
        op1 = self._types.pop()
        op2 = self._types.pop()
        if not op1.is_primitive or not op2.is_primitive:
            raise TypeError('invalid Type for multiplication')
        if op1.name == Type.bool or op2.name == Type.bool:
            raise TypeError('invalid Type for multiplication')
        if op1.name == Type.string or op2.name == Type.string:
            raise TypeError('invalid Type for multiplication')
        if op1.name != op2.name:
            raise TypeError('invalid Type for multiplication')

        if op1.name == Type.int:
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            code += mips_mul('$t2', '$t1', '$t0')
            code += mips_store(src='$t2', dst='$sp', offset=8)
            code += add_stack(8)
            self._types.append(Type(Type.int))
        # double type --- use coprocessor. $f0-$f31 registers. Only use even numbered ones.
        elif op1 == Type.double:
            code += mips_load_double('$f0', '$sp')
            code += mips_load_double('$f2', '$sp', offset=8)
            code += mips_mul_double('$f4', '$f2', '$f0')
            code += mips_store_double('$f4', '$sp', offset=8)
            code += add_stack(8)
            self._types.append(Type(Type.int))
        return code

    def mod(self, tree):
        code = ''.join(self.visit_children(tree))
        op2 = self._types.pop()
        op1 = self._types.pop()
        if op2.type != Type.int or op1.Type != Type.int:
            raise TypeError('Invalid modulo')
        if op2 == Type.int:
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            code += mips_div('$t2', '$t1', '$t0')
            code += 'mfhi $t2\n'
            code += mips_store(src='$t2', dst='$sp', offset=8)
            code += add_stack(8)
            self._types.append(Type(Type.int))
        return code

    def div(self, tree):
        code = ''.join(self.visit_children(tree))
        op2 = self._types.pop()
        op1 = self._types.pop()
        if not op1.is_primitive or not op2.is_primitive:
            raise TypeError('invalid Type for multiplication')
        if op1.name == Type.bool or op2.name == Type.bool:
            raise TypeError('invalid Type for multiplication')
        if op1.name == Type.string or op2.name == Type.string:
            raise TypeError('invalid Type for multiplication')
        if op1.name != op2.name:
            raise TypeError('invalid Type for multiplication')
        if op1.name == Type.int:
            print('#########im in integer div')
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            code += mips_div('$t2', '$t1', '$t0')
            code += 'mflo $t2\n'
            code += mips_store(src='$t2', dst='$sp', offset=8)
            code += add_stack(8)
            self._types.append(Type(Type.int))
        # double type --- use coprocessor. $f0-$f31 registers. Only use even numbered ones.
        elif op1.name == Type.double:
            code += mips_load_double('$f0', '$sp')
            code += mips_load_double('$f2', '$sp', offset=8)
            code += mips_div_double('$f4', '$f2', '$f0')
            code += mips_store_double('$f4', '$sp', offset=8)
            code += add_stack(8)
            self._types.append(Type(Type.double))
        return code

    def add(self, tree):
        code = ''.join(self.visit_children(tree))
        op2 = self._types.pop()
        op1 = self._types.pop()
        if not op1.is_primitive or not op2.is_primitive:
            raise TypeError('invalid Type for add')
        if op1.name == Type.bool or op2.name == Type.bool:
            raise TypeError('invalid Type for add')
        if op1.name == Type.string or op2.name == Type.string:
            raise TypeError('invalid Type for add')
        if op1.name != op2.name:
            raise TypeError('invalid Type for add')

        if op1.name == Type.int:
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            code += mips_add('$t2', '$t0', '$t1')
            code += mips_store(src='$t2', dst='$sp', offset=8)
            self._types.append(Type(Type.int))
            code += add_stack(8)
        # double type --- use coprocessor. $f0-$f31 registers. Only use even numbered ones.
        elif op1.name == Type.double:
            code += mips_load_double('$f0', '$sp')
            code += mips_load_double('$f2', '$sp', offset=8)
            code += mips_add_double('$f4', '$f0', '$f2')
            code += mips_store_double('$f4', '$sp', offset=8)
            code += add_stack(8)
            self._types.append(Type(Type.double))
        return code

    def sub(self, tree):
        code = ''.join(self.visit_children(tree))
        op2 = self._types.pop()
        op1 = self._types.pop()
        if not op1.is_primitive or not op2.is_primitive:
            raise TypeError('invalid Type for sub')
        if op1.name == Type.bool or op2.name == Type.bool:
            raise TypeError('invalid Type for sub')
        if op1.name == Type.string or op2.name == Type.string:
            raise TypeError('invalid Type for sub')
        if op1.name != op2.name:
            raise TypeError('invalid Type for sub')

        if op1.name == Type.int:
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            code += mips_sub('$t2', '$t1', '$t0')
            code += mips_store(src='$t2', dst='$sp', offset=8)
            code += add_stack(8)
            self._types.append(Type(Type.int))
        # double type --- use coprocessor. $f0-$f31 registers. Only use even numbered ones.
        elif op1.name == Type.double:
            code += mips_load_double('$f0', '$sp')
            code += mips_load_double('$f2', '$sp', offset=8)
            code += mips_sub_double('$f4', '$f2', '$f0')
            code += mips_store_double('$f4', '$sp', offset=8)
            code += add_stack(8)
            self._types.append(Type(Type.double))
        return code

    def and_bool(self, tree):
        code = ''.join(self.visit_children(tree))
        op1 = self._types.pop()
        op2 = self._types.pop()
        if op1.name != Type.bool or op2.name != Type.bool:
            raise TypeError('Invalid Type for boolean action ')
        code += mips_load('$t0', '$sp')
        code += mips_load('$t0', '$sp', offset=8)
        code += mips_and('$t2', '$t0', '$t1')
        code += mips_store('$t2', '$sp', offset=8)
        code += add_stack(8)

        self._types.append(Type(Type.bool))
        return code

    def or_bool(self, tree):
        code = ''.join(self.visit_children(tree))
        op1 = self._types.pop()
        op2 = self._types.pop()
        if op1.name != Type.bool or op2.name != Type.bool:
            raise TypeError('Invalid Type for boolean action ')
        code += mips_load('$t0', '$sp')
        code += mips_load('$t0', '$sp', offset=8)
        code += mips_or('$t2', '$t0', '$t1')
        code += mips_store('$t2', '$sp', offset=8)
        code += add_stack(8)
        self._types.append(Type(Type.bool))
        return code

    def eq(self, tree):
        code = ''.join(self.visit_children(tree))
        op1 = self._types.pop()
        op2 = self._types.pop()
        if op1.name != Type.bool or op2.name != Type.bool:
            raise TypeError('Invalid Type for boolean action ')
        if op1.name == Type.double:  # and typ.dimension == 0: #todo - no clue what operand_type dimension is!!!
            label_number = self.new_label()
            label = '__d_eq__' + label_number
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
        elif op1.name == Type.string:  # and typ.dimension == 0:
            code += '.text\n'
            code += mips_jump(mips_get_label('str cmp 1'))
            code += mips_store('$v0', '$sp', 0)
        else:  # int, bool    #done i think
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            # special equality checking operation - will set t2 = 1 if t1 == t0
            code += 'seq $t2, $t1, $t0\n'
            code += add_stack(8)
            code += mips_store('$t2', '$sp')
        self._types.append(Type(Type.bool))
        return code

    def gt(self, tree):
        code = ''.join(self.visit_children(tree))
        operand_type = self._types.pop()
        if operand_type.name == Type.int:
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            code += 'sgt $t2, $t1, $t0\n'  # special data comparison instruction
            code += add_stack(8)
            code += mips_store('$t2', '$sp')
        if operand_type.name == Type.double:
            label_number = self.new_label()
            label = '__d_gt__' + label_number
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
        self._types.append(Type(Type.bool))
        return code

    def ge(self, tree):
        code = ''.join(self.visit_children(tree))
        operand_type = self._types.pop()
        if operand_type.name == Type.int:
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            code += 'sge $t2, $t1, $t0\n'  # special data comparison instruction
            code += add_stack(8)
            code += mips_store('$t2', '$sp')
        if operand_type.name == Type.double:
            label_number = self.new_label()
            label = '__d_ge__' + label_number
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
        self._types.append(Type(Type.bool))
        return code

    def lt(self, tree):
        code = ''.join(self.visit_children(tree))
        operand_type = self._types.pop()
        if operand_type.name == Type.int:
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            code += 'slt $t2, $t1, $t0\n'  # special data comparison instruction
            code += add_stack(8)
            code += mips_store('$t2', '$sp')
        if operand_type.name == Type.double:
            label_number = self.new_label()
            label = '__d_lt__' + label_number
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
        self._types.append(Type(Type.bool))
        return code

    def le(self, tree):
        code = ''.join(self.visit_children(tree))
        operand_type = self._types.pop()
        if operand_type.name == Type.int:
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            code += 'sle $t2, $t1, $t0\n'  # special data comparison instruction
            code += add_stack(8)
            code += mips_store('$t2', '$sp')
        if operand_type.name == Type.double:
            label_number = self.new_label()
            label = '__d_le__' + label_number
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
        self._types.append(Type(Type.bool))
        return code

    # operation for getting opposite of a bool value.
    def not_bool(self, tree):
        code = ''.join(self.visit_children(tree))
        op1 = self._types.pop()
        if op1.name != Type.bool:
            raise TypeError('Invalid Type for boolean Action')
        label_number = self.new_label()
        label = '__not__' + label_number
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
        self._types.append(Type(Type.bool))
        return code

    def neg(self, tree):
        code = ''.join(self.visit_children(tree))
        operand_type = self._types[-1]

        if operand_type.name == Type.int:
            code += mips_load('$t0', '$sp')
            code += mips_sub('$t0', '$zero', '$t0')
            code += mips_store('$t0', '$sp')
        elif operand_type.name == Type.double:
            code += mips_load_double('$f0', '$sp')
            code += 'ng.d $f0, $f0\n'  # special FP instruction for negating double
            code += mips_store('$f0', '$sp')
        else:
            raise TypeError('Invalid Type for negating')
        return code

    def actuals(self, tree):
        return 'actuals'

    def method(self, tree):
        return 'METH'

    def call(self, tree):
        return 'CALL'

    def subscript(self, tree):
        return 'subs_ '

    def stmt(self, tree):
        code = ''
        print('#### start stmt')
        child = tree.children[0]
        stmt_label = self.new_label()
        child._meta = stmt_label
        code += self.visit(child)
        return code

    def if_stmt(self, tree):
        print('### start if_stmt')
        condition = self.visit(tree.children[0])
        then_code = self.visit(tree.children[1])
        hasElse = len(tree.children) != 2

        else_label = self.new_label()
        then_label = self.new_label()
        end_label = self.new_label()

        code = mips_load('$a0', '$sp', 0)
        code += add_stack(8)
        code += mips_beq('$a0', 0, end_label)
        code += mips_jump(then_label)

        code += '{}:\n'.format(then_label)
        code += then_code
        code += mips_jump(end_label)
        if hasElse:
            else_code = self.visit(tree.children[2])
            code += '{}:\n'.format(else_label)
            code += else_code

        return code

    def for_stmt(self, tree):  # todo - i have no clue
        print('### start for_stmt')
        if len(tree.children == 2):
            check_code = self.visit(tree.children[0])
            stmt_code = self.visit(tree.children[1])
        if len(tree.children == 3):
            pass
        # generate for(expr;expr;expr){stmt;} code
        self.loop_labels.pop()
        return None

    def while_stmt(self, tree):
        print('### start while_stmt')
        check_label = self.new_loop_label()
        continue_label = '_cont_'+check_label
        end_label = '_end_'+check_label

        parent_scope = self.symbol_table.get_current_scope()
        current_scope = Scope(parent_scope, check_label)
        self.symbol_table.push_scope(current_scope)
        symbol = Symbol('loop', 'loop', value=None,
                        scope=current_scope, label=check_label)
        self.symbol_table.push_symbol(symbol)
        self.loop_labels.append(check_label)

        check_code = self.visit(tree.children[0])
        stmt_code = self.visit(tree.children[1])

        self.symbol_table.pop_scope()
        self.loop_labels.pop()

        code = ''
        code += '{}:\n'.format(check_label)
        code += check_code

        code += mips_load('$a0', '$sp', 0)
        code += add_stack(8)
        code += mips_beqz('$a0', end_label)
        code += mips_jump(continue_label)

        code += '{}:\n'.format(continue_label)
        code += stmt_code
        code += '{}:\n'.format(end_label)
        return code

    def break_stmt(self, tree):
        code = ''
        code += mips_jump('_end_' + self.loop_labels[-1])
        return code

    def return_stmt(self, tree):
        code = ''
        if len(tree.children) == 1:
            self.visit(tree.children[0])
            code += mips_load('$v0', '$sp', 0)
            code += add_stack(8)
        code += mips_jump('$ra')
        return code

    def converters(self, tree):
        return ''.join(self.visit_children(tree))

    def itob(self, tree):
        code = ''
        code = self.visit_children(tree)[0]
        tp = self._types.pop()
        if tp.name != Type.int:
            raise TypeError('invalid Type for itob')
        code += mips_jal(mips_get_label('itob'))
        code += sub_stack(8)
        code += mips_store('$v0', '$sp')
        self._types.append(Type(Type.bool))
        return code

    def btoi(self, tree):
        code = ''
        code = self.visit_children(tree)[0]
        tp = self._types.pop()
        if tp.name != Type.bool:
            raise TypeError('Invalid Type for btoi')
        code += mips_jal(mips_get_label('btoi'))
        code += sub_stack(8)
        code += mips_store('$v0', '$sp')
        self._types.append(Type(Type.int))
        return code

    def itod(self, tree):
        code = self.visit_children(tree)[0]
        tp = self._types.pop()
        if tp.name != Type.int:
            raise TypeError('Invalid Type for itod')
        code += mips_jal(mips_get_label('itod'))
        code += sub_stack(8)
        code += mips_store('$v0', '$sp')
        self._types.append(Type(Type.double))
        return code

    def dtoi(self, tree):
        code = ''
        code = self.visit_children(tree)[0]
        tp = self._types.pop()
        if tp.name != Type.double:
            raise TypeError('Invalid Type for dtoi')
        code += mips_jal(mips_get_label('dtoi'))
        code += sub_stack(8)
        code += mips_store('$v0', '$sp')
        self._types.append(Type(Type.int))
        return code

    def declare_global_static_funcs(self):
        code = ''
        code += mips_new_array()
        code += mips_itod()
        code += mips_itob()
        code += mips_dtoi()
        code += mips_btoi()
        code += mips_str_cmp()
        code += print_double()
        code += print_bool(self.data)
        code += print_integer()
        code += print_string()
        code += print_newline(self.data)
        code += read_char()
        code += read_integer()
        code += read_line()
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

test_in_out = '''
int main(){
    int a;
    a = ReadInteger();
    Print(a);
}
'''

test_print = '''
int main(){
    Print(5);
}
'''

test_read_line = '''
int main(){
    string s;
    s = ReadLine();
    Print(s);
}

'''

test_int_operation = '''
int main(){
    int a;
    int b;
    int c;
    a = 5;
    b = 10;
    c = a / b;
    Print(c);
}
'''

test_itob = '''
int main(){
    bool a;
    a = itob(5);
    Print(a);
}
'''

test_double_operation = '''
int main(){
    double a;
    double b;
    double c;
    a = 1.5;
    b = 3.4;
    c = a + b;
    Print(c);
}
'''

test_array = '''
int main(){
    NewArray(5, int);
}
'''

test_if = '''
int main(){
    int a;
    if (true){
        a = 5;
        Print(a);
    }
    else{
        a = 6;
        Print(a);
    }

    if (false){
        a = 5;
        Print(a);
    }
    else{
        a = 6;
        Print(a);
    }
}
'''


if __name__ == '__main__':
    tree = get_parse_tree(test_if)
    print(tree.pretty())
    code = mips_text()
    code += '.globl main\n'
    cgen = Cgen()
    code += str(cgen.visit(tree))
    code += cgen.data.data
    print("CODE:")
    print(code)
    f = open("s.s", "w")
    f.write(code)
    f.close()

'''  def expr(self, tree):
        print('#### start expr')
        self.visit_children(tree)
        print(tree.children)
        return 'expression' '''
