import lark 
from lark.visitors import Interpreter
from lark import Token , Lark
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
        return type1.name == type2.name

    if is_array(type1) or is_array(type2):
        return type1.name == type2.name and type1.dimension == type2.dimension


class Cgen(Interpreter):
    label_counter = 0
    string_label = 0
    class_label = 0
    stmt_block_counter = 0
    varible_label_counter = 0
    loop_counter = 0
    object_label_counter = 0
    array_last_type = None

    def new_object_label(self):
        self.object_label_counter += 1
        return 'object_'+str(self.object_label_counter)

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
    
    def new_class_label(self):
        self.class_label += 1
        return '__class__'+str(self.class_label)

    def __init__(self):
        super().__init__()
        self.loop_labels = []
        self._types = []
        self.func_formals = []
        self.symbol_table = SymbolTable()
        self.data = DataSection()
        self.current_function = None
        self.class_var_counter = 0
        self.class_func_counter = 0
        self.class_functions = []
        self.class_variables = []
        self.in_formal = False

    def filter_lists(self, object1):
        if isinstance(object1, list):
            code = ''
            for x in object1:
                code += x
            return code
        return object

    def start(self, tree):

        root = Scope('root')
        self.symbol_table.push_scope(root)

        code = ''.join(self.visit_children(tree))
        code += self.declare_global_static_funcs()
        return code

    def declaration(self, tree):
        declarations = []
        code = ''
        for decl in tree.children:
            declarations.append(decl)
        index = 0
        cannot_be_generated = False
        while(len(declarations) != 0):
            if cannot_be_generated:
                raise ClassError('code cannont be generated')
            try:
                code += self.visit(declarations[index])
                declarations.pop(index)
                index = 0
            except:
                index += 1
                if index == len(declarations):
                    cannot_be_generated = True
        return code
    
    def class_declaration(self, tree):
        return ''.join(self.visit(tree))

    def class1(self , tree):
        class_name = tree.children[0]
        try:
            self.symbol_table.lookup_class(class_name)
            raise Exception('Class already defined')
        except ClassError:
            self.class_var_counter = 0
            self.class_func_counter = 0
            self.class_functions = []
            self.class_variables = []
            class_label = self.new_class_label()
            parent_scope = self.symbol_table.get_current_scope()
            current_scope = Scope('__class__'+class_name , parent_scope)
            self.symbol_table.push_scope(current_scope)
            class_object = Class(parent_scope , class_name , class_label)
            self.symbol_table.push_class(class_object)  
            code = ''
            if len(tree.children) > 1:
                for field in tree.children[1:]:
                    code += self.visit(field)
            class_object.functions = self.class_functions.copy()
            class_object.variables = self.class_variables.copy()
            self.data.add_data(class_label+':\n' + mips_align(2) + '.space 4\n')
            code += mips_load_immidiate('$v0' , 9)
            code += mips_load_immidiate('$a0' , self.class_func_counter * 8)
            code += mips_syscall()
            code += mips_load_address('$t0' , class_label)
            code += mips_store('$v0' , '$t0' , 0)
            code += mips_load('$t0' , '$v0' , 0)
            offset = 0
            for func in self.class_functions:
                code += mips_load_address('$t1' , func.label)
                code += mips_store('$t1' , '$t0' , offset = offset)
                offset += 8
            return code          

    def field(self , tree):
        code = ''
        
        for child in tree.children:
            if child.data == 'function_declaration':
                code += self.visit(child)
                self.class_func_counter += 1
            elif child.data == 'variable_declaration':
                code += self.visit(child)
                self.class_var_counter += 1
        return code


    def function_declaration(self, tree):
        code = ''
        if len(tree.children) == 4:
            self.visit(tree.children[0])
            return_type = self.array_last_type
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

        function_data = Function(scope=function_scope,
                                 name=ident, label='', return_type=return_type , func_formals= self.func_formals)
        function_data.label = '__' + function_data.scope.get_id() + '__'
        self.class_functions.append(function_data)
        self.symbol_table.push_function(function_data)
        self.current_function = function_data
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
        code += '{}:\n'.format(function_data.label+'__end__')
        code += mips_load('$ra', '$sp', 0)
        code += add_stack(8)
        self.symbol_table.pop_scope()
        self.symbol_table.pop_scope()
        # if ident == 'main':
        code += mips_jr('$ra')
        return code

    def variable_declaration(self, tree):
        code = ''
        code += ''.join(self.visit_children(tree))
        return code

    def variable(self, tree):
        code = ''
        self.visit(tree.children[0])
        
        variable_type =  self.array_last_type #Type(self.visit(tree.children[0]), 0)
        variable_name = tree.children[1]
        label = self.new_variable_label()
        size = 4
        if variable_type.name == Type.double and variable_type.dimension == 0:
            size = 8
        self.data.add_data(label + ':\n' + mips_align(2) + '.space {}\n'.format(size))
        symbol = Symbol(variable_name, variable_type,
                        scope=self.symbol_table.get_current_scope(), label=label)
        self.class_variables.append(symbol)
        self.symbol_table.push_symbol(symbol)
        if self.in_formal:
            self.func_formals.append(symbol)
        return code

    def formals(self, tree):
        self.in_formal = True
        self.func_formals = []
        parent_scope = self.symbol_table.get_current_scope()
        current_scope = Scope('formals', parent_scope)
        self.symbol_table.push_scope(current_scope)

        self.visit_children(tree)
        self.in_formal = False
        return ''

    def type(self, tree):
        if type(tree.children[0]) == lark.lexer.Token:
            self.array_last_type = Type(tree.children[0])
        else:
            self.visit(tree.children[0])
            self.array_last_type.dimension += 1
        return '' #hope it doesn't ruin anything

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
        return ''.join(self.visit_children(tree))

    def expr0(self, tree):
        return ''.join(self.visit_children(tree))

    def expr1(self, tree):
        return ''.join(self.filter_lists(self.visit_children(tree)))

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
        tp1 = self._types.pop()
        tp2 = self._types.pop()
        if not convertible(tp1, tp2):
            raise TypeError('Invalid assignment type')
        if tp2.name == Type.double and tp2.dimension == 0:
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
        self._types.append(tp2)
        return code

    def class_inst(self, tree):  
        class_name = tree.children[0].value
        class_object = self.symbol_table.lookup_class(class_name)
        data_length = 8 + 8 * (len(class_object.variables))
        object_label = self.new_object_label()
        self.data.add_data(object_label + ':\n' + mips_align(2)  + '.space 4\n')
        code = ''
        code += mips_load_address('$t0' , class_object.label)
        code += mips_load_address('$t1' , object_label)
        code += mips_load_immidiate('$a0' , data_length)
        code += mips_load_immidiate('$v0' , 9)
        code += mips_syscall()
        code += mips_store('$v0' , '$t1')
        code += mips_store('$t0' , '$v0')
        code += sub_stack(8)
        code += mips_store('$t1' , '$sp')
        symbol = Symbol(class_name , Type(class_name) , value = None , scope =self.symbol_table.get_current_scope() , label = object_label)
        self.symbol_table.push_symbol(symbol)
        self._types.append(symbol.type)
        return code

    def var_addr(self, tree):  # finds variable label and push it to stack
        code = ''
        var_name = tree.children[0].value
        symbol = self.symbol_table.lookup_symbol(var_name)
        label = symbol.label
        code = ''
        code += mips_load_address('$t0', label=label)
        code += sub_stack(8)
        code += mips_store('$t0', '$sp')
        self._types.append(symbol.type)
        return code

    def simple_call(self, tree):
        code = ''
        function_name = tree.children[0].value
        function = self.symbol_table.lookup_function(function_name)
        function_label = function.label
        if len(tree.children) > 1:
            code += self.visit(tree.children[1])
        offset = 0
        for x in reversed(function.func_formals):
            code += mips_load_address('$t0' , x.label)
            code += mips_load('$t1' , '$sp' , offset)
            code += mips_load('$t2' , '$t0' , 0)
            code += mips_store('$t2' , '$sp' , offset)
            code += mips_store('$t1' , '$t0' , 0)
            offset += 8
        code += mips_jal(function_label)
        for x in reversed(function.func_formals):
            code += mips_load_address('$t0' , x.label)
            code += mips_load('$t1' , '$sp' , 0)
            code += add_stack(8)
            code += mips_store('$t1' , '$t0' , 0)
        
        if function.return_type != None:
            self._types.append(function.return_type)
            code += sub_stack(8)
            code += mips_store('$v0' , '$sp' , 0)
        return code

    def class_call(self, tree):
        function_name = tree.children[1].value
        code = ''
        code += self.visit(tree.children[0])
        code += mips_load('$t0' , '$sp')
        code += mips_move('$t3' , '$t0')
        code += add_stack(8)
        tp = self._types.pop()
        if tp.dimension > 0:
            if function_name != 'length':
                raise FunctionError('Invalid function for array')
            code += sub_stack(8)
            code += mips_load('$t3' , '$t3' , 0)
            code += mips_store('$t3' , '$sp')
            self._types.append(Type(Type.int))
            return code
        class_object = self.symbol_table.lookup_class(tp.name)
        func_index = class_object.get_func_index(function_name)
        func = class_object.get_function(function_name)
        if len(tree.children) > 2:
            code += self.visit(tree.children[2])
        offset = 8
        for x in class_object.variables:
            code += mips_load('$t1' , '$t3' , offset)
            code += mips_load_address('$t2' , x.label)
            code += mips_store('$t1' , '$t2' , 0)
            offset += 8
        offset = 0
        for x in reversed(func.func_formals):
            code += mips_load_address('$t0' , x.label)
            code += mips_load('$t1' , '$sp' , offset)
            code += mips_load('$t2' , '$t0' , 0)
            code += mips_store('$t2' , '$sp' , offset)
            code += mips_store('$t1' , '$t0' , 0)
            offset += 8
        code += mips_jal(func.label)
        for x in reversed(func.func_formals):
            code += mips_load_address('$t0' , x.label)
            code += mips_load('$t1' , '$sp' , 0)
            code += add_stack(8)
            code += mips_store('$t1' , '$t0' , 0)
        offset = 8
        for x in class_object.variables:
            code += mips_load_address('$t1' , x.label)
            code += mips_load('$t2' , '$t1' , 0)
            code += mips_store('$t2' , '$t3' , offset)
            offset += 8
        if func.return_type != None:
            self._types.append(func.return_type)
            code += sub_stack(8)
            code += mips_store('$v0' , '$sp' , 0)
        return code

    def var_access(self, tree): 
        ident = tree.children[1].value
        code = ''
        code += self.visit(tree.children[0])
        code += mips_load('$t0' , '$sp' )
        tp = self._types.pop()
        if tp.dimension > 0:
            if ident != 'length':
                raise FunctionError('Invalid function for array')
            code += mips_store('$t0' , '$sp')
            self._types.append(Type(Type.int))
            return code
        class_object = self.symbol_table.lookup_class(tp.name)
        var_index = class_object.get_var_index(ident)
        var_type = class_object.get_variable(ident).type
        self._types.append(var_type)
        code += mips_addi('$t1' , '$t0' , 8 * ( 1 + var_index ))
        code += mips_store('$t1' , '$sp')
        return  code

    def val(self, tree):  
        code = ''.join(self.visit_children(tree))
        operand_type = self._types[-1]
        if operand_type.name == Type.double and operand_type.dimension == 0:
            code += mips_load('$t0', '$sp')
            code += mips_load_double('$f0', '$t0')
            code += mips_store_double('$f0', '$sp')
        else: 
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$t0')
            code += mips_store('$t1', '$sp')
        return code

    def print_stmt(self, tree): 
        code = ''
        for child in tree.children:
            code += self.visit(child)
            operand_type = self._types.pop()
            if(operand_type.dimension > 0):
                raise TypeError('Invalid dimension for Print')
            if operand_type.name == Type.double:
                code += mips_jal(mips_get_label('print double'))
            elif operand_type.name == Type.int:
                code += mips_jal(mips_get_label('print integer'))
            elif operand_type.name == Type.string:
                code += mips_jal(mips_get_label('print string'))
            elif operand_type.name == Type.bool:  
                code += mips_jal(mips_get_label('print bool'))
        code += mips_jal(mips_get_label('print new line'))
        return code

    def new_array(self, tree): 
        code = ''.join(self.visit(tree.children[0]))
        self.visit(tree.children[1])
        tp = self.array_last_type
        length_type = self._types.pop()
        if length_type.name != 'int' or length_type.dimension != 0:
            raise(TypeError('Invalid length type for NewArray()'))

        code += sub_stack(8)
        code += mips_load_immidiate('$a0', 3)
        code += mips_store('$a0', '$sp', 0)
        code += mips_jal(mips_get_label('new array'))
        self._types.append(Type(tp.name,
                                tp.dimension+1))
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
        elif op1.name == Type.double:
            code += mips_load_double('$f0', '$sp')
            code += mips_load_double('$f2', '$sp', offset=8)
            code += mips_mul_double('$f4', '$f2', '$f0')
            code += mips_store_double('$f4', '$sp', offset=8)
            code += add_stack(8)
            self._types.append(Type(Type.double))
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
        else:
            raise TypeError('Invalid Type for Division')
        return code

    def add(self, tree):
        code = ''.join(self.visit_children(tree))
        op2 = self._types.pop()
        op1 = self._types.pop()
        if op1.dimension == op2.dimension and op1.dimension == 1 and op1.name == op2.name:
            code += mips_jal(mips_get_label('join arrays'))
            self._types.append(Type(op1.name , op2.dimension))
            return code
        if not op1.is_primitive or not op2.is_primitive:
            raise TypeError('invalid Type for add')
        if op1.name == Type.bool or op2.name == Type.bool:
            raise TypeError('invalid Type for add')
        if op1.name != op2.name:
            raise TypeError('invalid Type for add')
        if op1.dimension > 1 or op2.dimension > 1:
            return TypeError('invalid dimension')
        
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

        elif op1.name == Type.string:
            code += mips_jal(mips_get_label('str concat'))
            self._types.append(Type(Type.string))
        else:
            raise TypeError('Invalid Type for addition')
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
        if op1.dimension != 0 or op2.dimension != 0:
            raise TypeError('Invalid dimension for subtraction')
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
        else:
            raise TypeError('Invalid Type for substraction')
        return code

    def and_bool(self, tree):
        code = ''.join(self.visit_children(tree))
        op1 = self._types.pop()
        op2 = self._types.pop()
        if op1.name != Type.bool or op2.name != Type.bool:
            raise TypeError('Invalid Type for boolean action ')
        if op1.dimension != 0 or op2.dimension != 0:
            raise TypeError('Invalid dimension for and action')
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
        if op1.dimension != 0 or op2.dimension != 0:
            raise TypeError('Invalid dimension for or action')
        code += mips_load('$t0', '$sp')
        code += mips_load('$t1', '$sp', offset=8)
        code += mips_or('$t2', '$t0', '$t1')
        code += mips_store('$t2', '$sp', offset=8)
        code += add_stack(8)
        self._types.append(Type(Type.bool))
        return code

    def eq(self, tree):
        code = ''.join(self.visit_children(tree))
        op1 = self._types.pop()
        op2 = self._types.pop()
        if op1.name != op2.name:
            raise TypeError('Invalid Type for equal action')
        if op1.dimension != 0 or op2.dimension != 0:
            raise TypeError('Invalid dimension for comparison')
        if op1.name == Type.double: 
            label_number = self.new_label()
            label = '__d_eq__' + label_number
            code += mips_load_double('$f0', '$sp')
            code += mips_load_double('$f2', '$sp', offset=8)
            code += mips_li('$t0', 0)
            # special floating point coprocessor instruction, checks equality
            code += 'c.eq.s $f0, $f2\n'
            code += 'bc1f ' + label + '\n'
            # bc1f is a flag that stores equality operation result. if eq is false it jumps to label.
            code += mips_li('$t0', 1)
            code += label + ':\n'
            code += add_stack(8)
            code += mips_store('$t0', '$sp')
        elif op1.name == Type.string:  
            code += '.text\n'
            code += mips_jump(mips_get_label('str cmp 1'))
            code += mips_store('$v0', '$sp', 0)
        else:  # int, bool , class
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            # special equality checking operation - will set t2 = 1 if t1 == t0
            code += 'seq $t2, $t1, $t0\n'
            code += add_stack(8)
            code += mips_store('$t2', '$sp')
        self._types.append(Type(Type.bool))
        return code

    def ne(self, tree):
        code = ''.join(self.visit_children(tree))
        op1 = self._types.pop()
        op2 = self._types.pop()
        if op1.name != op2.name:
            raise TypeError('Invalid Type for equal action')
        if op1.dimension != 0 or op2.dimension != 0:
            raise TypeError('Invalid dimension for comparison')
        if op1.name == Type.double: 
            label_number = self.new_label()
            label = '__d_eq__' + label_number
            code += mips_load_double('$f0', '$sp')
            code += mips_load_double('$f2', '$sp', offset=8)
            code += mips_li('$t0', 0)
            # special floating point coprocessor instruction, checks equality
            code += 'c.eq.s $f0, $f2\n'
            code += 'bc1f ' + label + '\n'
            # bc1f is a flag that stores equality operation result. if eq is false it jumps to label.
            code += mips_li('$t0', 1)
            code += label + ':\n'
            code += add_stack(8)
            code += mips_store('$t0', '$sp')
        elif op1.name == Type.string:  # and typ.dimension == 0:
            code += '.text\n'
            code += mips_jump(mips_get_label('str cmp 1'))
            code += mips_load_immidiate('$t0', 1)
            code += 'sne $v0 , $v0 , $t0\n'
            code += mips_store('$v0', '$sp', 0)
        else:  # int, bool    
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            # special equality checking operation - will set t2 = 1 if t1 == t0
            code += 'sne $t2, $t1, $t0\n'
            code += add_stack(8)
            code += mips_store('$t2', '$sp')
        self._types.append(Type(Type.bool))
        return code

    def gt(self, tree):
        code = ''.join(self.visit_children(tree))
        op1 = self._types.pop()
        op2 = self._types.pop()
        if op1.name != op2.name:
            raise TypeError('Invalid Type for equal action')
        if op1.dimension != 0 or op2.dimension != 0:
            raise TypeError('Invalid dimension for comparison')
        if op1.name == Type.int:
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            code += 'sgt $t2, $t1, $t0\n'  # special data comparison instruction
            code += add_stack(8)
            code += mips_store('$t2', '$sp')
        elif op1.name == Type.double:
            label_number = self.new_label()
            label = '__d_gt__' + label_number
            code += mips_load_double('$f0', '$sp')
            code += mips_load_double('$f2', '$sp', offset=8)
            code += mips_li('$t0', 0)
            code += 'c.gt.s $f2, $f0\n'  # if gt is false, will jump to label
            code += 'bc1f ' + label
            code += mips_li('$t0', 1)  # will reach this code if gt is true
            code += label + ':\n'
            code += add_stack(8)
            code += mips_store('$t0', '$sp')
        else:
            raise TypeError('Invalid Type for comparison')
        self._types.append(Type(Type.bool))
        return code

    def ge(self, tree):
        code = ''.join(self.visit_children(tree))
        op1 = self._types.pop()
        op2 = self._types.pop()
        if op1.name != op2.name:
            raise TypeError('Invalid Type for equal action')
        if op1.dimension != 0 or op2.dimension != 0:
            raise TypeError('Invalid dimension for comparison')
        if op1.name == Type.int:
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            code += 'sge $t2, $t1, $t0\n'  # special data comparison instruction
            code += add_stack(8)
            code += mips_store('$t2', '$sp')
        elif op1.name == Type.double:
            label_number = self.new_label()
            label = '__d_ge__' + label_number
            code += mips_load_double('$f0', '$sp')
            code += mips_load_double('$f2', '$sp', offset=8)
            code += mips_li('$t0', 0)
            code += 'c.ge.s $f2, $f0\n'  # if ge is false, will jump to label
            code += 'bc1f ' + label
            code += mips_li('$t0', 1)  # will reach this code if ge is true
            code += label + ':\n'
            code += add_stack(8)
            code += mips_store('$t0', '$sp')
        else:
            raise TypeError('Invalid Type for comparison')
        self._types.append(Type(Type.bool))
        return code

    def lt(self, tree):
        code = ''.join(self.visit_children(tree))
        op1 = self._types.pop()
        op2 = self._types.pop()
        if op1.name != op2.name:
            raise TypeError('Invalid Type for equal action')
        if op1.dimension != 0 or op2.dimension != 0:
            raise TypeError('Invalid dimension for comparison')
        if op1.name == Type.int:
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            code += 'slt $t2, $t1, $t0\n'  # special data comparison instruction
            code += add_stack(8)
            code += mips_store('$t2', '$sp')
        elif op1.name == Type.double:
            label_number = self.new_label()
            label = '__d_lt__' + label_number
            code += mips_load_double('$f0', '$sp')
            code += mips_load_double('$f2', '$sp', offset=8)
            code += mips_li('$t0', 0)
            code += 'c.lt.s $f2, $f0\n'  # if lt is false, will jump to label
            code += 'bc1f ' + label
            code += mips_li('$t0', 1)  # will reach this code if lt is true
            code += label + ':\n'
            code += add_stack(8)
            code += mips_store('$t0', '$sp')
        else:
            raise TypeError('Invalid Type for comparison')
        self._types.append(Type(Type.bool))
        return code

    def le(self, tree):
        code = ''.join(self.visit_children(tree))
        op1 = self._types.pop()
        op2 = self._types.pop()
        if op1.name != op2.name:
            raise TypeError('Invalid Type for equal action')
        if op1.dimension != 0 or op2.dimension != 0:
            raise TypeError('Invalid dimension for comparison')
        if op1.name == Type.int:
            code += mips_load('$t0', '$sp')
            code += mips_load('$t1', '$sp', offset=8)
            code += 'sle $t2, $t1, $t0\n'  # special data comparison instruction
            code += add_stack(8)
            code += mips_store('$t2', '$sp')
        elif op1.name == Type.double:
            label_number = self.new_label()
            label = '__d_le__' + label_number
            code += mips_load_double('$f0', '$sp')
            code += mips_load_double('$f2', '$sp', offset=8)
            code += mips_li('$t0', 0)
            code += 'c.le.s $f2, $f0\n'  # if le is false, will jump to label
            code += 'bc1f ' + label
            code += mips_li('$t0', 1)  # will reach this code if le is true
            code += label + ':\n'
            code += add_stack(8)
            code += mips_store('$t0', '$sp')
        else:
            raise TypeError('Invalid Type for comparison')
        self._types.append(Type(Type.bool))
        return code

    # operation for getting opposite of a bool value.
    def not_bool(self, tree):
        code = ''.join(self.visit_children(tree))
        op1 = self._types.pop()
        if op1.name != Type.bool or op1.dimension > 0:
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
        if operand_type.dimension > 0 :
            raise TypeError('Invalid dimension for negating')
        if operand_type.name == Type.int:
            code += mips_load('$t0', '$sp')
            code += mips_sub('$t0', '$zero', '$t0')
            code += mips_store('$t0', '$sp')
        elif operand_type.name == Type.double:
            code += mips_load_double('$f0', '$sp')
            code += 'ng.s $f0, $f0\n'  # special FP instruction for negating double
            code += mips_store('$f0', '$sp')
        else:
            raise TypeError('Invalid Type for negating')
        return code

    def actuals(self, tree):
        code = ''
        return ''.join(self.visit_children(tree))

    

    def call(self,tree):
        return ''.join(self.visit_children(tree.children))

    

    def subscript(self, tree):
        code = ''
        code += self.visit(tree.children[0])
        tp = self._types.pop()
        if tp.dimension == 0:
            raise TypeError("Invalid array access")
        code += self.visit(tree.children[1])
        tp2 = self._types.pop()
        if tp2.name != Type.int:
            raise TypeError("Invalid index")
        self._types.append(Type(tp.name , tp.dimension - 1))
        code += mips_load('$a0' , '$sp' , 0)
        code += mips_load('$v0' , '$sp' , 8)
        code += add_stack(16)
        code += mips_addi('$a0' , '$a0' , 1)
        code += mips_shift_left('$a0' , '$a0' , 3)
        code += mips_add('$v0' , '$v0' , '$a0')
        code += sub_stack(8)
        code += mips_store('$v0' , '$sp' , 0)
        return code

    def stmt(self, tree):
        code = ''
        child = tree.children[0]
        stmt_label = self.new_label()
        child._meta = stmt_label
        code += self.visit(child)
        return code

    def if_stmt(self, tree):
        condition = self.visit(tree.children[0])
        tp = self._types.pop()
        if tp.name != Type.bool:
            raise TypeError('Invalid type for if condition')
        then_code = self.visit(tree.children[1])
        hasElse = len(tree.children) != 2
        else_label = self.new_label()
        end_label = self.new_label()
        next_label = end_label
        if hasElse:
            next_label = else_label
        code = condition
        code += mips_load('$a0', '$sp', 0)
        code += add_stack(8)
        code += mips_beq('$a0', 0, next_label)
        code += then_code
        if hasElse:
            code += mips_jump(end_label)
            else_code = self.visit(tree.children[2])
            code += '{}:\n'.format(else_label)
            code += else_code
        code += '{}:\n'.format(end_label)
        return code

    def for_stmt(self, tree):  
        return ''.join(self.visit_children(tree))

    def for1(self, tree):
        check_label = self.new_loop_label()
        check_label2 = self.new_loop_label()
        end_label = '_end_' + check_label
        parent_scope = self.symbol_table.get_current_scope()
        current_scope = Scope(check_label, parent_scope)
        self.symbol_table.push_scope(current_scope)
        self.loop_labels.append(check_label)

        init_code = self.visit(tree.children[0])
        check_code = self.visit(tree.children[1])
        every_loop_code = self.visit(tree.children[2])
        stmt_code = self.visit(tree.children[3])
        self.symbol_table.pop_scope()
        self.loop_labels.pop()
        code = ''
        code += init_code
        code += mips_jump(check_label2)
        code += '{}:\n'.format(check_label)
        code += every_loop_code
        code += '{}:\n'.format(check_label2)
        code += check_code
        code += mips_load('$a0', '$sp', 0)
        code += add_stack(8)
        code += mips_beqz('$a0', end_label)
        code += stmt_code
        code += mips_jump(check_label)
        code += '{}:\n'.format(end_label)
        return code

    def for2(self, tree):
        check_label = self.new_loop_label()
        end_label = '_end_' + check_label
        parent_scope = self.symbol_table.get_current_scope()
        current_scope = Scope(check_label, parent_scope)
        self.symbol_table.push_scope(current_scope)
        self.loop_labels.append(check_label)
        init_code = self.visit(tree.children[0])
        check_code = self.visit(tree.children[1])
        stmt_code = self.visit(tree.children[2])
        self.symbol_table.pop_scope()
        self.loop_labels.pop()
        code = ''
        code += init_code
        code += '{}:\n'.format(check_label)
        code += check_code
        code += mips_load('$a0', '$sp', 0)
        code += add_stack(8)
        code += mips_beqz('$a0', end_label)
        code += stmt_code
        code += mips_jump(check_label)
        code += '{}:\n'.format(end_label)
        return code

    def for3(self, tree):
        check_label = self.new_loop_label()
        check_label2 = self.new_loop_label()
        end_label = '_end_' + check_label
        parent_scope = self.symbol_table.get_current_scope()
        current_scope = Scope(check_label, parent_scope)
        self.symbol_table.push_scope(current_scope)
        self.loop_labels.append(check_label)
        check_code = (self.visit(tree.children[0]))
        every_loop_code = (self.visit(tree.children[1]))
        stmt_code = (self.visit(tree.children[2]))
        self.symbol_table.pop_scope()
        self.loop_labels.pop()
        code = ''
        code += mips_jump(check_label2)
        code += '{}:\n'.format(check_label)
        code += every_loop_code
        code += '{}:\n'.format(check_label2)
        code += check_code
        code += mips_load('$a0', '$sp', 0)
        code += add_stack(8)
        code += mips_beqz('$a0', end_label)
        code += stmt_code
        code += mips_jump(check_label)
        code += '{}:\n'.format(end_label)
        return code

    def for4(self, tree):
        check_label = self.new_loop_label()
        end_label = '_end_' + check_label
        parent_scope = self.symbol_table.get_current_scope()
        current_scope = Scope(check_label, parent_scope)
        self.symbol_table.push_scope(current_scope)
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
        code += stmt_code
        code += mips_jump(check_label)
        code += '{}:\n'.format(end_label)
        return code

    def while_stmt(self, tree):
        check_label = self.new_loop_label()
        end_label = '_end_'+check_label
        parent_scope = self.symbol_table.get_current_scope()
        current_scope = Scope(check_label, parent_scope)
        self.symbol_table.push_scope(current_scope)
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
        code += stmt_code
        code += mips_jump(check_label)
        code += '{}:\n'.format(end_label)
        return code

    def break_stmt(self, tree):
        code = ''
        code += mips_jump('_end_' + self.loop_labels[-1])
        return code

    def return_stmt(self, tree):
        code = ''
        if self.current_function.return_type == None and len(tree.children) != 0:
            raise TypeError('Invalid return')
        if len(tree.children) == 1:
            code += self.visit(tree.children[0])
            if self.current_function.return_type.name != self._types.pop().name:
                raise TypeError('Invalid return Type')
            code += mips_load('$v0', '$sp', 0)
            code += add_stack(8)
        code += mips_jump(self.current_function.label+'__end__')
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
        code += join_arrays()
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
        code += concat_string()
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
  i = 0;
   for (i = 3; i <10;i = i + 1 ) {
     Print(i);
     i = i + 1;
  }
  Print("done");
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
void calc(int a) {
    Print("Im in the FUNCTION");
}

int main() {
    calc(5);
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
    a = 11.5;
    Print(a);
    b = 3.4;
    Print(b);
    c = a * b;
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
test_equal = '''
int main(){
    if( true == true ){
        Print("true is equal to true");
    }
    if( true != false ){
        Print("true is not equal to false");
    }
}
'''

test_function_with_formal = '''
    void calc(int a , int b){
        Print(a , " " , b);
        if(a == 3){
            calc(2,131);
        }
    }

    int main(){
        calc(5 , 4);
        calc(3, 6);
    }
'''

test_funciton_return = '''
    int calc(int a){
        return 2 * a + 3;
    }

    int main(){
        Print(calc(3));
    }
'''

test_function_recursive = '''
    int fib(int a ){
        int x;
        if (a == 0 || a == 1){
           return 1;
        }
        Print(a);
        x =  fib( a - 1) + fib( a - 2);
        Print("Ab " , a , " " , x);
        return x;
    }

    int main(){
        Print(fib(5));
    }
'''

func_test = '''
void calc2(){
    Print("im in CALC2 function");
}

void calc(){
    calc2();
}

int main(){
    calc();
}

'''

double_test = '''
int main(){
    double a;
    double b;
    double c;
    a = 1.5;
    b = 3.4;
    c = a + b;
    Print(c);
    c = a - b;
    Print(c);
    c = a * b;
    Print(c);
    c = a / b;
    Print(c);
}
'''

class_test = '''
    class A{
        int a;
        B y;
        void pq(int d){
            Print("in A " , d);
            Print("masht1 " , a);
            a = d;
            Print("masht2 " , a);
        }
    }
    class B{
        int b;
        void pp(int c){
            Print("in B " , c);
            b = c;
        }
    }

    

    int main(){
        A x ;
        A z;
        x = new A;
        z = x;
        if(z == x){
            Print("joon baba");
        }
        x.a = 2;
        x.y = new B;
        x.y.b = 4;
        x.pq(18);
        x.y.pp(21); 
        Print(x.a + x.y.b);
        x.a = x.a + x.y.b * 2;
        Print(x.a);
    }

'''

indent_test = '''
    int main(){
        int a;
        a = a + 1;
        a=a-2;
        Print(a);
    }

'''

string_test =  '''
    int main(){
        string s;
        string x;
        s = "salam";
        x = s;
        Print(s , " " , x);
    }


'''

test = '''

class Person {
    string name;
    int age;

    void setName(string new_name) {
        name = new_name;
    }

    void setAge(int new_age) {
        age = new_age;
    }

    void print() {
        Print("Name: ", name, " Age: ", age);
    }

}

int main() {
    Person p;

    string name;
    int age;

    name = ReadLine();
    age = ReadInteger();

    p = new Person;
    p.setName(name);
    p.setAge(age);

    p.print();
}


'''

string_concat_test = '''
    int main(){
        string s;
        s = "salam " + "chetori? ";
        Print(s);
    }

'''

array_test = '''
    int main(){
        int[] a;
        int i;
        a = NewArray(10 , int);
        Print(a.length);         
        
    }


'''

array_test2 = '''

void sort(int[] items) {

    /* implementation of bubble sort */
    int i;
    int j;

    int n;
    n = items.length;

    for (i = 0; i < n-1; i = i + 1)
        for (j = 0; j < n - i - 1; j = j + 1)
            if (items[j] > items[j + 1]) {
                int t;
                t = items[j];
                items[j] = items[j + 1];
                items[j + 1] = t;
            }
}

int main() {
    int i;
    int j;
    int[] rawitems;
    int[] items;

    Print("Please enter the numbers (max count: 100, enter -1 to end sooner): ");

    rawitems = NewArray(100, int);
    for (i = 0; i < 100; i = i + 1) {
        int x;
        x = ReadInteger();
        if (x == -1) break;

        rawitems[i] = x;
    }

    items = NewArray(i, int);

    // copy to a more convenient location
    for (j = 0; j < i; j = j + 1) {
        items[j] = rawitems[j];
    }

    sort(items);

    Print("After sort: ");

    for (i = 0; i < items.length(); i = i + 1) {
        Print(items[i]);
    }
}

'''

test_array3 = '''
    int main(){
        int[] a;
        int[] b;
        int[] c;
        int i;
        a = NewArray(10 , int);
        b = NewArray(5 , int);
        for(i = 0 ; i < a.length ; i = i + 1){
            a[i] = i+1;
        }
        for(i = 0; i < b.length() ; i =i+1){
            b[i] = i*i;
        }
        Print(a.length());
        Print(b.length());
        for(i = 0; i < b.length; i = i + 1){
            Print(a[i] , " ", b[i]);
        }
        c = a + b;
        Print(c.length);
        b = a;
        for( i = 0 ; i < c.length() ; i = i + 1){
            Print(c[i] , " " , b[i]);
        }
    }



'''

test2 = '''
class A {

}

int main(){
    A a;

    a = New A ;  
}

'''


if __name__ == '__main__':
    tree = get_parse_tree(class_test)
    print(tree.pretty())
    code = mips_text()
    code += '.globl main\n'
    cgen = Cgen()
    code += str(cgen.visit(tree))
    code += cgen.data.data
    print(code)
    f = open("s.s", "w")
    f.write(code)
    f.close()

'''  def expr(self, tree):
        print('#### start expr')
        self.visit_children(tree)
        print(tree.children)
        return 'expression' '''
