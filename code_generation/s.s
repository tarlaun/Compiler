.text
.globl main
__pq__formals____class__A__root__:
sub $sp, $sp, 8
sw $ra, 0($sp)
la $t0 , str_1
sub $sp, $sp, 8
sw $t0, 0($sp)
jal __print__string__
la $t0 , var_3
sub $sp, $sp, 8
sw $t0, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
jal __print__integer__
jal __print__new__line__
la $t0 , str_2
sub $sp, $sp, 8
sw $t0, 0($sp)
jal __print__string__
la $t0 , var_1
sub $sp, $sp, 8
sw $t0, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
jal __print__integer__
jal __print__new__line__
la $t0 , var_1
sub $sp, $sp, 8
sw $t0, 0($sp)
la $t0 , var_3
sub $sp, $sp, 8
sw $t0, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
lw $t0, 8($sp)
lw $t1, 0($sp)
sw $t1, 0($t0)
sw $t1, 8($sp)
addi $sp, $sp, 8
addi $sp, $sp, 8
la $t0 , str_3
sub $sp, $sp, 8
sw $t0, 0($sp)
jal __print__string__
la $t0 , var_1
sub $sp, $sp, 8
sw $t0, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
jal __print__integer__
jal __print__new__line__
__pq__formals____class__A__root____end__:
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
li $v0 , 9
li $a0 , 8
syscall
la $t0 , __class__1
sw $v0, 0($t0)
lw $t0, 0($v0)
la $t1 , __pq__formals____class__A__root__
sw $t1, 0($t0)
__pp__formals____class__B____class__A__root__:
sub $sp, $sp, 8
sw $ra, 0($sp)
la $t0 , str_4
sub $sp, $sp, 8
sw $t0, 0($sp)
jal __print__string__
la $t0 , var_5
sub $sp, $sp, 8
sw $t0, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
jal __print__integer__
jal __print__new__line__
la $t0 , var_4
sub $sp, $sp, 8
sw $t0, 0($sp)
la $t0 , var_5
sub $sp, $sp, 8
sw $t0, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
lw $t0, 8($sp)
lw $t1, 0($sp)
sw $t1, 0($t0)
sw $t1, 8($sp)
addi $sp, $sp, 8
addi $sp, $sp, 8
__pp__formals____class__B____class__A__root____end__:
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
li $v0 , 9
li $a0 , 8
syscall
la $t0 , __class__2
sw $v0, 0($t0)
lw $t0, 0($v0)
la $t1 , __pp__formals____class__B____class__A__root__
sw $t1, 0($t0)
main:
sub $sp, $sp, 8
sw $ra, 0($sp)
la $t0 , var_6
sub $sp, $sp, 8
sw $t0, 0($sp)
la $t0 , __class__1
la $t1 , object_1
li $a0 , 32
li $v0 , 9
syscall
sw $v0, 0($t1)
sw $t0, 0($v0)
sub $sp, $sp, 8
sw $t1, 0($sp)
lw $t0, 8($sp)
lw $t1, 0($sp)
sw $t1, 0($t0)
sw $t1, 8($sp)
addi $sp, $sp, 8
addi $sp, $sp, 8
la $t0 , var_7
sub $sp, $sp, 8
sw $t0, 0($sp)
la $t0 , var_6
sub $sp, $sp, 8
sw $t0, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
lw $t0, 8($sp)
lw $t1, 0($sp)
sw $t1, 0($t0)
sw $t1, 8($sp)
addi $sp, $sp, 8
addi $sp, $sp, 8
la $t0 , var_7
sub $sp, $sp, 8
sw $t0, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
la $t0 , var_6
sub $sp, $sp, 8
sw $t0, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
lw $t0, 0($sp)
lw $t1, 8($sp)
seq $t2, $t1, $t0
addi $sp, $sp, 8
sw $t2, 0($sp)
lw $a0, 0($sp)
addi $sp, $sp, 8
beq $a0, 0, ll_13
la $t0 , str_5
sub $sp, $sp, 8
sw $t0, 0($sp)
jal __print__string__
jal __print__new__line__
ll_13:
la $t0 , var_6
sub $sp, $sp, 8
sw $t0, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
lw $t0, 0($sp)
addi $t1, $t0, 8
sw $t1, 0($sp)
li $t0, 2
sub $sp, $sp, 8
sw $t0, 0($sp)
lw $t0, 8($sp)
lw $t1, 0($sp)
sw $t1, 0($t0)
sw $t1, 8($sp)
addi $sp, $sp, 8
addi $sp, $sp, 8
la $t0 , var_6
sub $sp, $sp, 8
sw $t0, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
lw $t0, 0($sp)
addi $t1, $t0, 16
sw $t1, 0($sp)
la $t0 , __class__2
la $t1 , object_2
li $a0 , 24
li $v0 , 9
syscall
sw $v0, 0($t1)
sw $t0, 0($v0)
sub $sp, $sp, 8
sw $t1, 0($sp)
lw $t0, 8($sp)
lw $t1, 0($sp)
sw $t1, 0($t0)
sw $t1, 8($sp)
addi $sp, $sp, 8
addi $sp, $sp, 8
la $t0 , var_6
sub $sp, $sp, 8
sw $t0, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
lw $t0, 0($sp)
addi $t1, $t0, 16
sw $t1, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
lw $t0, 0($sp)
addi $t1, $t0, 8
sw $t1, 0($sp)
li $t0, 4
sub $sp, $sp, 8
sw $t0, 0($sp)
lw $t0, 8($sp)
lw $t1, 0($sp)
sw $t1, 0($t0)
sw $t1, 8($sp)
addi $sp, $sp, 8
addi $sp, $sp, 8
la $t0 , var_6
sub $sp, $sp, 8
sw $t0, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
lw $t0, 0($sp)
move $t3, $t0
addi $sp, $sp, 8
li $t0, 18
sub $sp, $sp, 8
sw $t0, 0($sp)
lw $t1, 8($t3)
la $t2 , var_1
sw $t1, 0($t2)
lw $t1, 16($t3)
la $t2 , var_2
sw $t1, 0($t2)
lw $t1, 24($t3)
la $t2 , var_3
sw $t1, 0($t2)
la $t0 , var_3
lw $t1, 0($sp)
lw $t2, 0($t0)
sw $t2, 0($sp)
sw $t1, 0($t0)
jal __pq__formals____class__A__root__
la $t0 , var_3
lw $t1, 0($sp)
addi $sp, $sp, 8
sw $t1, 0($t0)
la $t1 , var_1
lw $t2, 0($t1)
sw $t2, 8($t3)
la $t1 , var_2
lw $t2, 0($t1)
sw $t2, 16($t3)
la $t1 , var_3
lw $t2, 0($t1)
sw $t2, 24($t3)
la $t0 , var_6
sub $sp, $sp, 8
sw $t0, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
lw $t0, 0($sp)
addi $t1, $t0, 16
sw $t1, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
lw $t0, 0($sp)
move $t3, $t0
addi $sp, $sp, 8
li $t0, 21
sub $sp, $sp, 8
sw $t0, 0($sp)
lw $t1, 8($t3)
la $t2 , var_4
sw $t1, 0($t2)
lw $t1, 16($t3)
la $t2 , var_5
sw $t1, 0($t2)
la $t0 , var_5
lw $t1, 0($sp)
lw $t2, 0($t0)
sw $t2, 0($sp)
sw $t1, 0($t0)
jal __pp__formals____class__B____class__A__root__
la $t0 , var_5
lw $t1, 0($sp)
addi $sp, $sp, 8
sw $t1, 0($t0)
la $t1 , var_4
lw $t2, 0($t1)
sw $t2, 8($t3)
la $t1 , var_5
lw $t2, 0($t1)
sw $t2, 16($t3)
la $t0 , var_6
sub $sp, $sp, 8
sw $t0, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
lw $t0, 0($sp)
addi $t1, $t0, 8
sw $t1, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
la $t0 , var_6
sub $sp, $sp, 8
sw $t0, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
lw $t0, 0($sp)
addi $t1, $t0, 16
sw $t1, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
lw $t0, 0($sp)
addi $t1, $t0, 8
sw $t1, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
lw $t0, 0($sp)
lw $t1, 8($sp)
add $t2, $t0, $t1
sw $t2, 8($sp)
addi $sp, $sp, 8
jal __print__integer__
jal __print__new__line__
la $t0 , var_6
sub $sp, $sp, 8
sw $t0, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
lw $t0, 0($sp)
addi $t1, $t0, 8
sw $t1, 0($sp)
la $t0 , var_6
sub $sp, $sp, 8
sw $t0, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
lw $t0, 0($sp)
addi $t1, $t0, 8
sw $t1, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
la $t0 , var_6
sub $sp, $sp, 8
sw $t0, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
lw $t0, 0($sp)
addi $t1, $t0, 16
sw $t1, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
lw $t0, 0($sp)
addi $t1, $t0, 8
sw $t1, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
li $t0, 2
sub $sp, $sp, 8
sw $t0, 0($sp)
lw $t0, 0($sp)
lw $t1, 8($sp)
mul $t2, $t1, $t0
sw $t2, 8($sp)
addi $sp, $sp, 8
lw $t0, 0($sp)
lw $t1, 8($sp)
add $t2, $t0, $t1
sw $t2, 8($sp)
addi $sp, $sp, 8
lw $t0, 8($sp)
lw $t1, 0($sp)
sw $t1, 0($t0)
sw $t1, 8($sp)
addi $sp, $sp, 8
addi $sp, $sp, 8
la $t0 , var_6
sub $sp, $sp, 8
sw $t0, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
lw $t0, 0($sp)
addi $t1, $t0, 8
sw $t1, 0($sp)
lw $t0, 0($sp)
lw $t1, 0($t0)
sw $t1, 0($sp)
jal __print__integer__
jal __print__new__line__
__main__formals____class__B____class__A__root____end__:
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
__join__arrays__:
lw $t0, 8($sp)
lw $t1, 0($sp)
addi $sp, $sp, 16
lw $a0, 0($t0)
lw $a1, 0($t1)
add $a0, $a0, $a1
move $t2, $a0
addi $a0, $a0, 1
sllv $a0 , $a0 , 3
li $v0 , 9
syscall
move $a0, $v0
sub $sp, $sp, 8
sw $a0, 0($sp)
sub $sp, $sp, 8
sw $ra, 0($sp)
sw $t2, 0($a0)
addi $a0, $a0, 8
lw $t3, 0($t0)
addi $a1, $t0, 8
jal __copy__array__
lw $t3, 0($t1)
addi $a1, $t1, 8
jal __copy__array__
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
__copy__array__:
lw $t4, 0($a1)
sw $t4, 0($a0)
addi $a0, $a0, 8
addi $a1, $a1, 8
addi $t3, $t3, -1
bne $t3, $zero, __copy__array__
jr $ra
__new__array__:
lw $a0, 8($sp)
lw $a1, 0($sp)
addi $sp, $sp, 16
addi $t6, $a0, 0
sllv $a0 , $a0 , $a1
addi $a0, $a0, 8
li $v0, 9
syscall
sw $t6, 0($v0)
sub $sp, $sp, 8
sw $v0, 0($sp)
jr $ra
__itod__:
lw $s0, 0($sp)
mtc1 $s0, $f0
cvt.s.w $f0, $f0
mfc1 $v0, $f0
addi $sp, $sp, 8
jr $ra
__itob__:
lw $s0, 0($sp)
li $v0 , 0
beqz $s0 , __itob__jump__
li $v0 , 1
__itob__jump__:
addi $sp, $sp, 8
jr $ra
__dtoi__:
l.s $f0, 0($sp)
cvt.w.s $f0, $f0
mfc1 $v0, $f0
addi $sp, $sp, 8
jr $ra
__btoi__:
lw $v0, 0($sp)
addi $sp, $sp, 8
jr $ra
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
__print__double__:
l.s $f12, 0($sp)
addi $sp, $sp, 8
li $v0 , 2
syscall
jr $ra
__print__bool__:
lw $a0, 0($sp)
addi $sp, $sp, 8
beqz $a0 , __print__bool__cont__2__
li $v0 , 4
la $a0 , true
syscall
j __print__bool__end__
__print__bool__cont__2__:
li $v0 , 4
la $a0 , false
syscall
__print__bool__end__:
jr $ra
__print__integer__:
lw $a0, 0($sp)
addi $sp, $sp, 8
li $v0 , 1
syscall
jr $ra
__print__string__:
lw $a0, 0($sp)
addi $sp, $sp, 8
li $v0 , 4
syscall
jr $ra
__print__new__line__:
li $v0 , 4
la $a0 , nw
syscall
jr $ra
__read__char__:
li $v0 , 12
syscall
sub $sp, $sp, 8
sw $v0, 0($sp)
jr $ra
__read__integer__:
li $v0 , 5
syscall
sub $sp, $sp, 8
sw $v0, 0($sp)
jr $ra
__read__line__:
li $a0 , 256
li $v0 , 9
syscall
move $a0, $v0
sub $sp, $sp, 8
sw $a0, 0($sp)
li $a1 , 256
li $v0 , 8
syscall
jr $ra
__str__concat__:
lw $t0, 8($sp)
lw $t1, 0($sp)
addi $sp, $sp, 16
li $a0 , 256
li $v0 , 9
syscall
sub $sp, $sp, 8
sw $v0, 0($sp)
sub $sp, $sp, 8
sw $ra, 0($sp)
move $a0, $v0
move $a1, $t0
jal __str__copy__
move $a1, $t1
jal __str__copy__
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
__str__copy__:
lb $t4, 0($a1)
sb $t4, 0($a0)
beq $t4, $zero, __str__copy__end__
addi $a0, $a0, 1
addi $a1, $a1, 1
j __str__copy__
__str__copy__end__:
jr $ra

.data
var_1:
.align 2
.space 4
var_2:
.align 2
.space 4
var_3:
.align 2
.space 4
str_1: .asciiz "in A "
str_2: .asciiz "masht1 "
str_3: .asciiz "masht2 "
__class__1:
.align 2
.space 4
var_4:
.align 2
.space 4
var_5:
.align 2
.space 4
str_4: .asciiz "in B "
__class__2:
.align 2
.space 4
var_6:
.align 2
.space 4
var_7:
.align 2
.space 4
object_1:
.align 2
.space 4
str_5: .asciiz "joon baba"
object_2:
.align 2
.space 4
true: 
.align 2
 .asciiz "true"
false: 
.align 2
 .asciiz "false"
nw: 
.align 2
 .asciiz "\n"
