label_number = 0
fp_dis = - 4  # sp = fp + fp_dis


# mips code producers for certain instructions:
def align_stack(top):
    global fp_dis
    if top != fp_dis:
        tmp = top - fp_dis
        fp_dis = top
        return ("addi $sp, $sp, " + str(tmp)+'\n')


def mips_add(v1, v2, v3):
    return ("add " + v1 + ", " + v2 + ", " + v3+'\n')


def mips_addi(v1, v2, v3):
    return ("addi " + v1 + ", " + v2 + ", " + v3+'\n')


def mips_move(dst, src):
    return ("move " + dst + ", " + src+'\n')


def mips_jump(label):
    return ("j " + label+'\n')


def mips_jal(label):
    return ("jal " + label+'\n')


def mips_jalr(reg):
    return ("jalr " + reg+'\n')


def mips_label(label):
    return (label + " :"+'\n')


def mips_load_address(dst, label):
    return ('la ' + dst + ' ' + label+'\n')


def mips_load(dst, src, offset=0):
    return ("lw " + dst + ", " + str(offset) + "(" + src + ")"+'\n')


def mips_load_double(dst, src, offset=0):
    return ("l.s " + dst + ", " + str(offset) + "(" + src + ")"+'\n')


def mips_li(dst, val):
    return ("li " + dst + ", " + str(val)+'\n')


def mips_load_byte(dst, src, offset=0):
    return ("lb " + dst + ", " + str(offset) + "(" + src + ")"+'\n')


def mips_syscall():
    return ("syscall"+'\n')


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


def emit_data(label, input):
    global data_section
    data_section += label + ':\n' + '    ' + input + '\n'


def print_data_section():
    global data_section
    print(data_section)


def label_gen():  # generates labels for MIPS code. Works well until 26*26
    global label_number
    num = label_number
    arr = []
    if num == 0:
        arr.append('A')
    count = 0
    while num != 0:
        s = num % 26
        num //= 26
        charcode = 65 + s - count
        arr.append(chr(charcode))
        count += 1
    arr.append("_")
    label_number += 1
    return "".join(arr[::-1])

def emit_array_length():
    code = ""
    code+=('___array_length:'+'\n')
    code+=mips_load('$s0', '$fp', 4+'\n')
    code+=mips_load('$v0', '$s0'+'\n')
    code+=('jr $ra'+'\n')
    return code


def mips_btoi():
    code = ""
    code+=('___btoi:\n')
    code+=('lw $v0, 4($fp)\n')
    code+=('jr $ra\n')
    return code


def mips_itob():
    code = ""
    code+=('___itob:\n')
    code+=('lw $s0, 4($fp)\n')
    code+=('li $v0, 0\n')
    code+=('beqz $s0, ___itob_jump\n')
    code+=('li $v0, 1\n')
    code+=('___itob_jump: jr $ra\n')
    return code


def mips_dtoi():
    code = ""
    code+=('___dtoi:\n')
    code+=('l.s $f0, 4($fp)\n')
    code+=('round.w.s $f0, $f0\n')
    code+=('mfc1 $v0, $f0\n')
    code+=('jr $ra\n')
    return code


def mips_itod():
    code=""
    code +=('___itod:\n')
    code+=('lw $s0, 4($fp)\n')
    code+=('mtc1 $s0, $f0\n')
    code+=('cvt.s.w $f0, $f0\n')
    code+=('mfc1 $v0, $f0\n')
    code+=('jr $ra\n')
    return code

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



text = ""
text += mips_add("$t1", "$t1", "$t2")
text+= mips_btoi()
print(text)
