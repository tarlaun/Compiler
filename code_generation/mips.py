label_number = 0
fp_dis = - 4  # sp = fp + fp_dis


# mips code producers for certain instructions:
def align_stack(top):
    global fp_dis
    if top != fp_dis:
        tmp = top - fp_dis
        fp_dis = top
        return ("addi $sp, $sp, " + str(tmp))


def mips_add(v1, v2, v3):
    return ("add " + v1 + ", " + v2 + ", " + v3)


def mips_addi(v1, v2, v3):
    return ("addi " + v1 + ", " + v2 + ", " + v3)


def mips_move(dst, src):
    return ("move " + dst + ", " + src)


def mips_jump(label):
    return ("j " + label)


def mips_jal(label):
    return ("jal " + label)


def mips_jalr(reg):
    return ("jalr " + reg)


def mips_label(label):
    return (label + " :")


def mips_load_address(dst, label):
    return ('la ' + dst + ' ' + label)


def mips_load(dst, src, offset=0):
    return ("lw " + dst + ", " + str(offset) + "(" + src + ")")


def mips_load_double(dst, src, offset=0):
    return ("l.s " + dst + ", " + str(offset) + "(" + src + ")")


def mips_li(dst, val):
    return ("li " + dst + ", " + str(val))


def mips_load_byte(dst, src, offset=0):
    return ("lb " + dst + ", " + str(offset) + "(" + src + ")")


def mips_syscall():
    return ("syscall")


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


text = ""
text += mips_add("$t1", "$t1", "$t2")
print(text)
