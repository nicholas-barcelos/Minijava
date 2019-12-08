.data
newline: .asciiz "\n"
aexp_compute_num_aux: .word 0
.text
exe_main:
  #sout
exe_aexp_compute1:
sw $fp, 0($sp)
addiu $sp, $sp, -4
li $a0, 3
sw $a0, 0($sp)
addiu $sp, $sp, -4
li $a0, 2
sw $a0, 0($sp)
addiu $sp, $sp, -4
li $a0, 1

neg $a0 $a0
sw $a0, 0($sp)
addiu $sp, $sp, -4
jal def_aexp_compute
li $v0, 1 # especifica o servico de print int
syscall # printa o $a0
li $v0, 4 # especifica o servico de print string
la $a0, newline
syscall # printa o newline
# eo_sout
  b end_program

class_aexp:
def_aexp_compute:
move $fp, $sp
sw $ra, 0($sp)
addiu $sp, $sp, -4
# cmds do metodo
lw $a0, 4($fp) # Pega arg do metodo

sw $a0, 0($sp)
addiu $sp, $sp, -4
li $a0, 0

lw $t1, 4($sp)
slt $a0, $t1, $a0
addiu $sp, $sp, 4

sw $a0, 0($sp)
addiu $sp, $sp, -4
bne $a0, $zero, true0
lw $a0, 4($fp) # Pega arg do metodo
sw $a0, 0($sp)
addiu $sp, $sp, -4
lw $a0, 12($fp) # Pega arg do metodo
lw $t1, 4($sp)
mul $a0, $t1, $a0
addiu $sp, $sp, 4
sw $a0, 0($sp)
addiu $sp, $sp, -4
lw $a0, 8($fp) # Pega arg do metodo
lw $t1, 4($sp)
add $a0, $t1, $a0
addiu $sp, $sp, 4
# Computou a expressao
la $t1, aexp_compute_num_aux
sw $a0, 0($t1) #Atribuiu a variavel

b eo_true0
true0:
lw $a0, 4($fp) # Pega arg do metodo
sw $a0, 0($sp)
addiu $sp, $sp, -4
lw $a0, 8($fp) # Pega arg do metodo
sw $a0, 0($sp)
addiu $sp, $sp, -4
li $a0, 1
lw $t1, 4($sp)
sub $a0, $t1, $a0
addiu $sp, $sp, 4
lw $t1, 4($sp)
mul $a0, $t1, $a0
addiu $sp, $sp, 4
sw $a0, 0($sp)
addiu $sp, $sp, -4
lw $a0, 12($fp) # Pega arg do metodo
lw $t1, 4($sp)
mul $a0, $t1, $a0
addiu $sp, $sp, 4
# Computou a expressao
la $t1, aexp_compute_num_aux
sw $a0, 0($t1) #Atribuiu a variavel

eo_true0:
addiu $sp, $sp, 4
# retorno
la $t1, aexp_compute_num_aux
lw $a0, 0($t1) # Acessa variavel
# prepara saida
lw $ra, 4($sp)
addiu $sp, $sp, 20
lw $fp, 0($sp)
jr $ra

def_aexp_negate:
move $fp, $sp
sw $ra, 0($sp)
addiu $sp, $sp, -4
# cmds do metodo
#sout
lw $a0, 4($fp) # Pega arg do metodo
li $v0, 1 # especifica o servico de print int
syscall # printa o $a0
li $v0, 4 # especifica o servico de print string
la $a0, newline
syscall # printa o newline
# eo_sout
# retorno
lw $a0, 4($fp) # Pega arg do metodo

beq $a0 $zero zerocheck_1
li $a0 0
b eo_zerocheck_1
zerocheck_1:
li $a0 1
eo_zerocheck_1:
# prepara saida
lw $ra, 4($sp)
addiu $sp, $sp, 12
lw $fp, 0($sp)
jr $ra

end_program: