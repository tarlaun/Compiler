.text
jal main
jal end
jr $ra
.globl main
new__array:
lw $a0, 8($sp)
lw $a1, 0($sp)
addi $sp, $sp, 16
addi $t6, $a0, 0
sllv $a0 , $a0 , $a1
addi $a0, $a0, 8
li $v0, 9
syscall
sw $t6, 0($v0)
addi $v0, $v0, 8
sub $sp, $sp, 8
sw $v0, 0($sp)
jr $ra
itod:
lw $s0, 4($fp)
mtc1 $s0, $f0
cvt.s.w $f0, $f0
mfc1 $v0, $f0
jr $ra
itob:
lw $s0, 4($fp)
li $v0 , 0
beqz $s0 , itob__jump
li $v0 , 1
itob__jump:
jr $ra
dtoi:
l.s $f0, 4($fp)
round.w.s $f0, $f0
mfc1 $v0, $f0
jr $ra
btoi:
lw $v0, 4($fp)
jr $ra
str__cmp__1:
lw $a0, 0($sp)
lw $a1, 8($sp)
addi $sp, $sp, 16
str__cmp:
lb $t0, 0($a0)
lb $t1, 0($a1)
bne $t0, $t1, not__eq__str
bne $t0, $zero, stat__cont
li $v0 , 1
jr $ra
stat__cont:
addi $a0, $a0, 1
addi $a1, $a1, 1
j str__cmp
not__eq__str:
li $v0 , 0
jr $ra
print__double:
l.d $f12, 0($sp)
addi $sp, $sp, 8
cvt.s.d $f12 , $f12
li $v0 , 2
syscall
jr $ra
print__bool:
lw $a0, 0($sp)
addi $sp, $sp, 8
beqz $a0 , print__bool__cont__2
li $v0 , 4
la $a0 , true
syscall
j print__bool__end
print__bool__cont__2:
li $v0 , 4
la $a0 , false
syscall
print__bool__end:
jr $ra
print__integer:
lw $a0, 0($sp)
addi $sp, $sp, 8
li $v0 , 1
syscall
jr $ra
print__string:
lw $a0, 0($sp)
addi $sp, $sp, 8
li $v0 , 4
syscall
jr $ra
print__new__line:
li $v0 , 4
la $a0 , nw
syscall
jr $ra
read__char:
li $v0 , 12
syscall
sub $sp, $sp, 8
sw $v0, 0($sp)
jr $ra
read__integer:
li $v0 , 5
syscall
sub $sp, $sp, 8
sw $v0, 0($sp)
jr $ra
read__line:
li $v0 , 9
syscall
move $a0, $v0
sub $sp, $sp, 8
sw $a0, 0($sp)
li $a1 , 256
li $v0 , 8
syscall
jr $ra
end:
li $v0 , 10
syscall
jr $ra
main:
move $fp , $sp
sub $sp, $sp, 8
sw $ra, 0($sp)
li $t0, 5
sub $sp, $sp, 8
sw $t0, 0($sp)
jal print__integer
jal print__new__line
lw $ra, 0($sp)
addi $sp, $sp, 8
move $sp , $fp
jr $ra

.data
true:
.align 2
 .asciiz "true"
false:
.align 2
 .asciiz "false"
nw:
.align 2
 .asciiz "\n"