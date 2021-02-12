def mips(stmt):
    return stmt + '\n'


fp_dis = - 4  # sp = fp + fp_dis


# mips code producers for certain instructions:
def mips_data():
    return '.data\n'


def mips_text():
    return '.text\n'


def mips_asciiz(str):
    ret = ' .asciiz ' + str + '\n'
    return ret


def mips_align(n):
    ret = '.align ' + str(n) + '\n'
    return ret


def align_stack(top):
    global fp_dis
    if top != fp_dis:
        tmp = top - fp_dis
        fp_dis = top
        return ("addi $sp, $sp, " + str(tmp) + '\n')


def sub_stack(disp):
    return ("sub $sp, $sp, " + str(disp) + '\n')


def add_stack(disp):
    return ("addi $sp, $sp, " + str(disp) + '\n')


def mips_add(v1, v2, v3):
    return ("add " + v1 + ", " + v2 + ", " + v3 + '\n')


def mips_addi(v1, v2, v3):
    return ("addi " + v1 + ", " + v2 + ", " + str(v3) + '\n')


def mips_add_double(v1, v2, v3):
    return ("add.d " + v1 + ", " + v2 + ", " + v3 + '\n')


def mips_sub(v1, v2, v3):
    return ("sub " + v1 + ", " + v2 + ", " + v3 + '\n')


def mips_sub_double(v1, v2, v3):
    return ("sub.d " + v1 + ", " + v2 + ", " + v3 + '\n')


def mips_mul(v1, v2, v3):
    return ("mul " + v1 + ", " + v2 + ", " + v3 + '\n')


def mips_mul_double(v1, v2, v3):
    return ("mul.d " + v1 + ", " + v2 + ", " + v3 + '\n')


def mips_div(v1, v2, v3):
    return ("div " + v1 + ", " + v2 + ", " + v3 + '\n')


def mips_div_double(v1, v2, v3):
    return ("div.d " + v1 + ", " + v2 + ", " + v3 + '\n')


def mips_or(v1, v2, v3):
    return ("or " + v1 + ", " + v2 + ", " + v3 + '\n')


def mips_and(v1, v2, v3):
    return ("and " + v1 + ", " + v2 + ", " + v3 + '\n')


def mips_move(dst, src):
    return ("move " + dst + ", " + src + '\n')


def mips_jump(label):
    return ("j " + label + '\n')

def mips_jr(register):
    return ("jr "+ register + "\n")

def mips_jal(label):
    return ("jal " + label + '\n')


def mips_jalr(reg):
    return ("jalr " + reg + '\n')


def mips_label(label):
    return (label + " :" + '\n')


def mips_load_address(dst, label):
    return ('la ' + dst + ' , ' + label + '\n')

def mips_load_immidiate(dst , value):
    return ('li ' + dst + ' , ' + str(value) + '\n')

def mips_load(dst, src, offset=0):
    return ("lw " + dst + ", " + str(offset) + "(" + src + ")" + '\n')


def mips_store(src, dst, offset=0):
    return ("sw " + src + ", " + str(offset) + "(" + dst + ")" + '\n')


def mips_store_double(src, dst, offset=0):
    return ("s.d" + src + ", " + str(offset) + "(" + dst + ")" + '\n')


def mips_load_double(dst, src, offset=0):
    return ("l.d " + dst + ", " + str(offset) + "(" + src + ")" + '\n')


def mips_li(dst, val):
    return ("li " + dst + ", " + str(val) + '\n')


def mips_load_byte(dst, src, offset=0):
    return ("lb " + dst + ", " + str(offset) + "(" + src + ")" + '\n')


def mips_beq(v1, v2, v3):
    return ("beq " + v1 + ", " + v2 + ", " + v3 + '\n')

def mips_beqz(register, label):
    return ("beqz "+register + " , " + label)

def mips_bne(v1 , v2 , v3):
    return ("bne " + v1 + ", " + v2 + ", " + v3 + '\n')

def mips_syscall():
    return ("syscall" + '\n')


def print_bool(label_num):
    return """
            lw $a0, 0($sp)
            addi $sp, $sp, 8
            beq $a0, 0, _false_print_{label}
            li $v0, 4
            la $a0, true
            syscall
            j _printbool_end_{label}
            _false_print_{label}:
            li $v0, 4
            la $a0, false
            syscall 
            _printbool_end_{label}:
                        """.format(label=label_num)


def print_newline():
    return """
                li $v0, 4
                la $a0, __newLine
                syscall
            """


def print_int():
    return """
            li $v0, 1
            lw $a0, 0($sp)
            addi $sp, $sp, 8
            syscall   
        """


def print_string():
    return """
        li $v0, 4
        lw $a0, 0($sp)
        addi $sp, $sp, 8
        syscall
        """


def print_double():
    return """
            l.d $f12, 0($sp)
            addi $sp, $sp, 8
            cvt.s.d $f12, $f12
            li $v0, 2
            syscall
        """


data_section = '''.data
__read:
    .space 400
__newLine:
    .asciiz "\\n"
__space:
    .asciiz " "
 __true:
    .asciiz "true"
__false:
    .asciiz "false"
__null:
    .word 0
__chert:
    .word 0
'''


def add_data(label, input):
    global data_section
    data_section += label + ':\n' + '    ' + input + '\n'


def print_data_section():
    global data_section
    print(data_section)


label_number = 0


def label_gen():  # generates labels for MIPS code. Works well until 26*26
    global label_number
    num = label_number
    lab = ""
    if num == 0:
        lab += 'A'
    count = 0
    while num != 0:
        disp = num % 26
        num //= 26
        charcode = 65 + disp - count
        lab += chr(charcode)
        count += 1
    lab += "_"
    label_number += 1
    return lab[::-1]


def mips_array_decl():
    code = ""
    code += ('__array__decl__:' + '\n')
    code += mips_load('$s0', '$fp', 4)
    code += mips_load('$v0', '$s0')
    code += ('jr $ra' + '\n')
    return code


def mips_btoi():
    code = ""
    code += mips_text()
    code += mips_create_label('btoi')
    code += mips_load('$v0', '$fp', 4)
    code += mips_jr('$ra')
    return code


def mips_itob():
    code = ""
    code += mips_text()
    code += mips_create_label('itob')
    code += mips_load('$s0' , '$fp' , 4)
    code += mips_load_immidiate('$v0' , 0)
    code += mips_beqz('$s0' , mips_get_label('itob jump'))
    code += mips_load_immidiate('$v0' , 1)
    code += mips_create_label('itob jump')
    code += mips_jr('$ra')
    return code


def mips_dtoi():
    code = ""
    code += mips_text()
    code += mips_create_label('dtoi')
    code += ('l.s $f0, 4($fp)\n')
    code += ('round.w.s $f0, $f0\n')
    code += ('mfc1 $v0, $f0\n')
    code += mips_jr('$ra')
    return code


def mips_itod():
    code = ""
    code += mips_text()
    code += mips_create_label('itod')
    code += mips_load('$s0' , '$fp' , 4)
    code += ('mtc1 $s0, $f0\n')
    code += ('cvt.s.w $f0, $f0\n')
    code += ('mfc1 $v0, $f0\n')
    code += mips_jr('$ra')
    return code

def mips_str_cmp():
    code = ""
    code += mips_text()
    code += mips_create_label('str cmp')
    code += mips_load_byte('$t0' , '$a0' , 0)
    code += mips_load_byte("$t1" , "$a1" , 0)
    code += mips_bne('$t0' , '$t1' , mips_get_label('not eq str'))
    code += mips_bne('$t0' , '$zero',  mips_get_label('stat cont'))
    code += mips_load_immidiate('$v0' , 1)
    code += mips_jr("$ra")
    code += mips_create_label('stat cont')
    code += mips_addi('$a0' , '$a0' , 1)
    code += mips_addi('$a1' , '$a1' , 1)
    code += mips_jump(mips_get_label('str cmp'))
    code += mips_create_label('not eq str')
    code += mips_load_immidiate('$v0' , 0)
    return code

def mips_end_programm():
    code = ''
    code += mips_text()
    code += mips_create_label('end')
    code += mips_load_immidiate('$v0' , 10)
    code += 'syscall\n'
    return code




def mips_create_label(str):
    
    return(mips_get_label(str) +":\n")

def mips_get_label(str):
    code = ""
    strings = str.split(" ")
    for i in range(len(strings)):
        code += "__"
        code += strings[i]
    return(code + "__")

semantic_error = '''
.text
.globl main

main:
la $a0 , errorMsg
addi $v0 , $zero, 4
syscall
jr $ra

.data
errorMsg: .asciiz "Semantic Error"
'''


def mips_semantic_error():
    return semantic_error


'''
text = ""
text += mips_add("$t1", "$t1", "$t2")
text += mips_btoi()
print(text)
for i in range(100):
    print(label_gen())'''
# print(print_bool(56))
