#### start the code generation
.text
__itod__:
lw $s0, 4($fp)
mtc1 $s0, $f0
cvt.s.w $f0, $f0
mfc1 $v0, $f0
jr $ra
.text
__itob__:
lw $s0, 4($fp)
li $v0 , 0
beqz $s0 , __itob__jump__li $v0 , 1
__itob__jump__:
jr $ra
.text
__dtoi__:
l.s $f0, 4($fp)
round.w.s $f0, $f0
mfc1 $v0, $f0
jr $ra
.text
__btoi__:
lw $v0, 4($fp)
jr $ra
.text
__str__cmp__1__:
lw $a0, 0($sp)
lw $a1, 8($sp)
addi $sp, $sp, 16
__str__cmp__:
lb $t0, 0($a0)
lb $t1, 0($a1)
bne $t0, $t1, __not__eq__str__
bne $t0, $zero, __stat__cont__
li $v0 , 1
jr $ra
__stat__cont__:
addi $a0, $a0, 1
addi $a1, $a1, 1
j __str__cmp__
__not__eq__str__:
li $v0 , 0
jr $ra
.text
__print__double__:
l.d $f12, 0($sp)
addi $sp, $sp, 8
cvt.s.d $f12 , $f12
li $v0 , 2
syscall
.text
__print__bool__:
j __print__bool__cont__
.data
.align 2
true:  .asciiz true
false:  .asciiz false
.text
__print__bool__cont__:
lw $a0, 0($sp)
addi $sp, $sp, 8
beqz $a0 , print bool cont 2li $v0 , 4
la $a0 , true
syscall
j __print__bool__end__
__print__bool__cont__2__:
li $v0 , 4
la $a0 , false
syscall
__print__bool__end__:
.text
__print__integer__:
lw $a0, 0($sp)
addi $sp, $sp, 8
li $v0 , 1
syscall
.text
__print__string__:
lw $a0, 0($sp)
addi $sp, $sp, 8
li $v0 , 4
syscall
.text
__print__new__line__:
j __new__line__
.data
.align 2
nw: 
 .asciiz \n
.text
__new__line__:
li $v0 , 4
la $a0 , nw
syscall
.text
__read__char__:
li $v0 , 12
syscall
sub $sp, $sp, 8
sw $v0, 0($sp)
.text
__read__integer__:
li $v0 , 5
syscall
sub $sp, $sp, 8
sw $v0, 0($sp)
.text
__read__line__:
li $v0 , 9
syscall
move $a0, $v0
sub $sp, $sp, 8
sw $a0, 0($sp)
li $a1 , 256
li $v0 , 8
syscall
.text
__end__:
li $v0 , 10
syscall
.text
main:
.data
.align 2
main_root_a: .space 4
.data
.align 2
main_root_b: .space 4
jal __end__
