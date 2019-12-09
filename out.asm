.data
newline: .asciiz "\n"
fac_computefac_num_aux: .word 0
.text
exe_main:
  #sout
exe_fac_computefac1:
sw $fp, 0($sp)
addiu $sp, $sp, -4
li $a0, 10
sw $a0, 0($sp)
addiu $sp, $sp, -4
jal def_fac_computefac
li $v0, 1 # especifica o servico de print int
syscall # printa o $a0
li $v0, 4 # especifica o servico de print string
la $a0, newline
syscall # printa o newline
# eo_sout
  b end_program

class_fac:
def_fac_computefac:
move $fp, $sp
sw $ra, 0($sp)
addiu $sp, $sp, -4
# cmds do metodo
lw $a0, 4($fp) # Pega arg do metodo

sw $a0, 0($sp)
addiu $sp, $sp, -4
li $a0, 1

lw $t1, 4($sp)
slt $a0, $t1, $a0
addiu $sp, $sp, 4

sw $a0, 0($sp)
addiu $sp, $sp, -4
bne $a0, $zero, true0
lw $a0, 4($fp) # Pega arg do metodo
sw $a0, 0($sp)
addiu $sp, $sp, -4
exe_fac_computefac2:
sw $fp, 0($sp)
addiu $sp, $sp, -4
lw $a0, 4($fp) # Pega arg do metodo
sw $a0, 0($sp)
addiu $sp, $sp, -4
li $a0, 1
lw $t1, 4($sp)
sub $a0, $t1, $a0
addiu $sp, $sp, 4
sw $a0, 0($sp)
addiu $sp, $sp, -4
jal def_fac_computefac
lw $t1, 4($sp)
mul $a0, $t1, $a0
addiu $sp, $sp, 4
# Computou a expressao
la $t1, fac_computefac_num_aux
sw $a0, 0($t1) #Atribuiu a variavel

b eo_true0
true0:
li $a0, 1
# Computou a expressao
la $t1, fac_computefac_num_aux
sw $a0, 0($t1) #Atribuiu a variavel

eo_true0:
addiu $sp, $sp, 4
# retorno
la $t1, fac_computefac_num_aux
lw $a0, 0($t1) # Acessa variavel
# prepara saida
lw $ra, 4($sp)
addiu $sp, $sp, 12
lw $fp, 0($sp)
jr $ra

end_program: