#### start the code generation
### variable
### variable
#### start stmt
#### var name a
### symbol int
#### EXPR
#### const_int
#### start stmt
#### var name b
### symbol string
#### EXPR
#### start stmt
### print_stmt
#### EXPR
#### val code gen
#### var name a
### symbol int
#### val code gen
#### var name b
### symbol string
.text
                .globl main
                main:
                la $t0 , error
                sub $sp, $sp, 8
                sw $t0, 0($sp)
                jal __print__string__
                li $v0 , 10
                syscall

                __print__string__:
                lw $a0, 0($sp)
                addi $sp, $sp, 8
                li $v0 , 4
                syscall
                jr $ra

                .data
                error:
                .align 2
                .asciiz "Semantic Error"