import src.node as nd

class Code:
    def __init__(self,stab):
        self.stab = stab
        self.beq_counter = 0

    #passa arvore sintatica
    def gera_mips(self,tree): 
        with open('out.txt', 'w') as out:
            str1 = ""
            for key in self.stab.keys():
                str1 += f"{key} word 0\n"
            string = (
                f".data\n"
                f"{str1}"
                f".text\n"
            )
            string += self.cgen_prog_main(tree)
            out.write(string)

        #--------------PROG--------------#

    def cgen_prog_main(self,prog_main):
        if(prog_main.children[0] is not None):
            string_ch1 = self.cgen_main_class(prog_main.children[0])
        if(prog_main.children[1] is not None):
            string_ch2 = self.cgen_loopclasse_ini(prog_main.children[1])
        string = f"{string_ch1}\n{string_ch2}"
        return string

    #--------------MAIN--------------#

    def cgen_main_class(self,main_class):
        string_ch1 = "//MAINCLASS\n"
        if(main_class.children[0] is not None):
            string_ch1 += self.cgen_cmd(main_class.children[0])

        string = (
            f"main_entry:\n"
            f"  move $fp $sp\n"
            f"  sw $ra 0($sp)\n"
            f"  addiu $sp $sp -4\n"
            f"  {string_ch1}\n"
            f"  lw $ra 4($sp)\n"
            f"  addiu $sp $sp 12\n"
            f"  lw $fp 0($sp)\n"
            f"  jr $ra\n"
        )
        return string

    #--------------CLASSE--------------#

    def cgen_classe_id(self,classe_id):
        string = "//CLASSE_ID"
        string += self.cgen_loopvar_ini(classe_id.children[1])
        string += self.cgen_loopmetodo_ini(classe_id.children[2])
        string += "//EO_CLASSE_ID"
        return string

    #--------------VAR--------------#

    def cgen_var_tipo(self,var_tipo):
        return ""

    #--------------METODO--------------#

    def cgen_metodo_public(self,metodo_public):
        string = "//Metodo_public"
        string += self.cgen_loopvar_ini(classe_id.children[2])
        string += self.cgen_loopcmd_ini(loopcmd_ini.children[3])
        string += self.cgen_exp(loopcmd_ini.children[4])
        string += "//EO_Metodo_public"
        return string

    #--------------PARAMS--------------#

    def cgen_params_tipo(self,params_tipo):
        pass

    #--------------TIPO--------------#

    def cgen_tipo_inta(self,tipo_inta):
        pass

    def cgen_tipo_bool(self,tipo_bool):
        pass

    def cgen_tipo_int(self,tipo_int):
        pass

    def cgen_tipo_id(self,tipo_id):
        pass

    #--------------CMD--------------#

    def cgen_cmd(self,cmd):
        string_ch1 = ""
        if(cmd.leaf[0] == "{"):
            string_ch1 += self.cgen_cmd_chave(cmd)
            
        elif(cmd.leaf[0].lower() == "if" and len(cmd.leaf) < 4):
            string_ch1 += self.cgen_cmd_if(cmd)

        elif(len(cmd.leaf) > 3 and cmd.leaf[3].lower() == "else"):
            string_ch1 += self.cgen_cmd_ifelse(cmd)

        elif(cmd.leaf[0].lower() == "while"):
            string_ch1 += self.cgen_cmd_while(cmd)

        elif(cmd.leaf[0].lower() == "system.out.println"):
            string_ch1 += self.cgen_cmd_sout(cmd)

        elif(cmd.leaf[1].lower() == "="):
            string_ch1 += self.cgen_cmd_ideq(cmd)

        elif(cmd.leaf[1].lower() == "["):
            string_ch1 += self.cgen_cmd_id(cmd)
        return string_ch1

    def cgen_cmd_chave(self,cmd_chave):
        string = "//cmd_chave"
        string += self.cgen_loopcmd_ini(loopcmd_ini.children[0])
        string += "//EO_cmd_chave"
        return string

    def cgen_cmd_if(self,cmd_if):
        string = "//IF_ELSE"
        cond = self.cgen_exp(cmd_ifelse.children[0])
        str1 = self.cgen_exp(cmd_ifelse.children[1])
        string += (
            f"{cond}\n"
            f"sw $a0 0($sp)\n"
            f"addiu $sp $sp -4\n"
            f"beq $a0 $zero false{self.beq_counter}\n"
            f"{str1}\n"
            f"false{self.beq_counter}:\n"
            f"addiu $sp $sp 4\n"
            )
        self.beq_counter += 1
        string += "//EO_IF_ELSE"
        return string

    def cgen_cmd_ifelse(self,cmd_ifelse):
        string = "//IF_ELSE"
        cond = self.cgen_exp(cmd_ifelse.children[0])
        str1 = self.cgen_cmd(cmd_ifelse.children[1])
        str2 = self.cgen_cmd(cmd_ifelse.children[2])
        string += (
            f"{cond}\n"
            f"sw $a0 0($sp)\n"
            f"addiu $sp $sp -4\n"
            f"bne $a0 $zero true{self.beq_counter}\n"
            f"{str2}\n"
            f"b eo_true{self.beq_counter}\n"
            f"true{self.beq_counter}:\n"
            f"{str1}\n"
            f"eo_true{self.beq_counter}:\n"
            f"addiu $sp $sp 4\n"
            )
        self.beq_counter += 1
        string += "//EO_IF_ELSE"
        return string

    def cgen_cmd_while(self,cmd_while):
        string = "//IF_ELSE"
        cond = self.cgen_exp(cmd_ifelse.children[0])
        str1 = self.cgen_cmd(cmd_ifelse.children[1])
        string += (
            f"{cond}\n"
            f"sw $a0 0($sp)\n"
            f"addiu $sp $sp -4\n"
            f"start{self.beq_counter}:\n"
            f"beq $a0 $zero false{self.beq_counter}\n"
            f"{str1}\n"
            f"b start{self.beq_counter}\n"
            f"false{self.beq_counter}:\n"
            f"addiu $sp $sp 4\n"
            )
        self.beq_counter += 1
        string += "//EO_IF_ELSE"
        return string

    def cgen_cmd_sout(self,cmd_sout):
        return ""

    def cgen_cmd_ideq(self,cmd_ideq):
        string = "//cmd_ideq"
        var = cmd_ideq.leaf[0]
        str1 = self.cgen_exp(cmd_ideq.children[0])
        string += (
            f"{str1}\n"
            f"la $t1 {var}\n"
            f"sw $a0 0($t1)\n"
        )
        string += "//EO_cmd_ideq"
        return string

    def cgen_cmd_id(self,cmd_id):
        return ""

    #--------------EXP--------------#

    def cgen_exp(self,exp):
        string = "//EXP"
        if(len(exp.children) > 1):
            string += self.cgen_exp_exp(exp)
        else:
            string += self.cgen_exp_rexp(exp)
        string += "//EO_EXP"
        return string


    def cgen_exp_exp(self,exp_exp):
        string = "//EXP_EXP"
        str1 = cgen(exp_exp.children[0])
        str2 = cgen(exp_rexp.children[1])
        string += (
            f"{str1}\n"
            f"sw $a0 0($sp)\n"
            f"addiu $sp $sp -4\n"
            f"{str2}\n"
            f"lw $t1 4($sp)\n"
            f"and $a0 $t1 $a0\n"
            f"addiu $sp $sp 4\n"
        )
        string += "//EO_EXP_EXP"
        return string

    def cgen_exp_rexp(self,exp_rexp):
        string = "//EXP_REXP"
        string += self.cgen_rexp(exp_rexp.children[0])
        string += "//EO_EXP_REXP"
        return string

    #--------------REXP--------------#

    def cgen_rexp(self,rexp):
        string = "//Rexp"
        if(len(rexp.children) > 1):
            string += self.cgen_rexp_rexp(rexp)
        else:
            string += self.cgen_rexp_aexp(rexp)
        string += "//EO_Rexp"
        return string

    def cgen_rexp_rexp(self,rexp_rexp):
        string = "//Rexp_Rexp"
        str1 = self.cgen_rexp(rexp_rexp.children[0])
        str2 = self.cgen_aexp(rexp_rexp.children[1])
        if(rexp_rexp.leaf[0] == "<"):
            string += (
                f"{str1}\n"
                f"sw $a0 0($sp)\n"
                f"addiu $sp $sp -4\n"
                f"{str2}\n"
                f"lw $t1 4($sp)\n"
                f"slt $a0 $t1 $a0\n"
                f"addiu $sp $sp 4\n"
            )
        elif(rexp_rexp.leaf[0] == ">"):
            string += (
                f"{str1}\n"
                f"sw $a0 0($sp)\n"
                f"addiu $sp $sp -4\n"
                f"{str2}\n"
                f"lw $t1 4($sp)\n"
                f"slt $a0 $a0 $t1\n"
                f"addiu $sp $sp 4\n"
            )
        elif(rexp_rexp.leaf[0] == "=="):
            string += (
                f"{str1}\n"
                f"sw $a0 0($sp)\n"
                f"addiu $sp $sp -4\n"
                f"{str2}\n"
                f"lw $t1 4($sp)\n"
                f"beq $a0 $t1 true{self.beq_counter}\n"
                f"li $a0 0\n"
                f"b eo_true{self.beq_counter}\n"
                f"true{self.beq_counter}:\n"
                f"li $a0 1\n"
                f"eo_true{self.beq_counter}:\n"
                f"addiu $sp $sp 4\n"
            )
            self.beq_counter += 1
        elif(rexp_rexp.leaf[0] == "!="):
            string += (
                f"{str1}\n"
                f"sw $a0 0($sp)\n"
                f"addiu $sp $sp -4\n"
                f"{str2}\n"
                f"lw $t1 4($sp)\n"
                f"bne $a0 $t1 true{self.beq_counter}\n"
                f"li $a0 0\n"
                f"b eo_true{self.beq_counter}\n"
                f"true{self.beq_counter}:\n"
                f"li $a0 1\n"
                f"eo_true{self.beq_counter}:\n"
                f"addiu $sp $sp 4\n"
            )
            self.beq_counter += 1
        elif(rexp_rexp.leaf[0] == "<="):
            string += (
                f"{str1}\n"
                f"sw $a0 0($sp)\n"
                f"addiu $sp $sp -4\n"
                f"{str2}\n"
                f"lw $t1 4($sp)\n"
                f"slt $a0 $a0 $t1\n"
                f"beq $a0 $zero true{self.beq_counter}\n"
                f"li $a0 0\n"
                f"b eo_true{self.beq_counter}\n"
                f"true{self.beq_counter}:\n"
                f"li $a0 1\n"
                f"eo_true{self.beq_counter}:\n"
                f"addiu $sp $sp 4\n"
            )
            self.beq_counter += 1
        elif(rexp_rexp.leaf[0] == ">="):
            string += (
                f"{str1}\n"
                f"sw $a0 0($sp)\n"
                f"addiu $sp $sp -4\n"
                f"{str2}\n"
                f"lw $t1 4($sp)\n"
                f"slt $a0 $t1 $a0\n"
                f"beq $a0 $zero true{self.beq_counter}\n"
                f"li $a0 0\n"
                f"b eo_true{self.beq_counter}\n"
                f"true{self.beq_counter}:\n"
                f"li $a0 1\n"
                f"eo_true{self.beq_counter}:\n"
                f"addiu $sp $sp 4\n"
            )
            self.beq_counter += 1
        string += "//EO_Rexp_Rexp"
        return string

    def cgen_rexp_aexp(self,resp_aexp):
        string = "//Resp_aexp"
        string += self.cgen_aexp(resp_aexp.children[0])
        string += "//EO_Resp_aexp"

    #--------------AEXP--------------#

    def cgen_aexp(self,aexp):
        string = "//AEXP"
        if(len(aexp.children) > 1):
            string += self.cgen_aexp_aexp(aexp)
        else:
            string += self.cgen_aexp_mexp(aexp)
        string += "//EO_AEXP"
        return string

    def cgen_aexp_aexp(self,aexp_aexp):
        string = "//AEXP"
        str1 += self.cgen_aexp(aexp_aexp.children[0])
        str2 += self.cgen_aexp(aexp_aexp.children[1])
        op = "add"
        if(aexp_aexp.leaf[0] == "-"):
            op = "sub"
        string += (
            f"{str1}\n"
            f"sw $a0 0($sp)\n"
            f"addiu $sp $sp -4\n"
            f"{str2}\n"
            f"lw $t1 4($sp)\n"
            f"{op} $a0 $t1 $a0\n"
            f"addiu $sp $sp 4\n"
        )
        string += "//EO_AEXP_AEXP"
        return string

    def cgen_aexp_mexp(self,aexp_mexp):
        string = "//AEXP_MEXP"
        string += self.cgen_mexp(aexp_mexp.children[0])
        string += "//EO_AEXP_MEXP"
        return string

    #--------------MEXP--------------#

    def cgen_mexp(self,mexp):
        string = "//MEXP"
        if(len(mexp.children) > 1):
            string += self.cgen_mexp_mexp(mexp)
        else:
            string += self.cgen_mexp_sexp(mexp)
        string += "//EO_MEXP"
        return string

    def cgen_mexp_mexp(self,mexp_mexp):
        string = "//MEXP"
        str1 += self.cgen_mexp(mexp_mexp.children[0])
        str2 += self.cgen_mexp(mexp_mexp.children[1])
        op = "mul"
        string += (
            f"{str1}\n"
            f"sw $a0 0($sp)\n"
            f"addiu $sp $sp -4\n"
            f"{str2}\n"
            f"lw $t1 4($sp)\n"
            f"{op} $a0 $t1 $a0\n"
            f"addiu $sp $sp 4\n"
        )
        string += "//EO_MEXP_MEXP"
        return string

    def cgen_mexp_sexp(self,mexp_sexp):
        string = "//MEXP_SEXP"
        string += self.cgen_sexp(mexp_sexp.children[0])
        string += "//EO_MEXP_SEXP"
        return string

    #--------------SEXP--------------#

    def cgen_sexp(self,sexp):
        string = "//SEXP"
        if(len(sexp.leaf) > 0):
            if(sexp.leaf[0] == "!"):
                string += self.cgen_sexp_not(sexp)
            elif(sexp.leaf[0] == "-"):
                string += self.cgen_sexp_minus(sexp)
            elif(sexp.leaf[0].lower() == "true"):
                string += self.cgen_sexp_true(sexp)
            elif(sexp.leaf[0].lower() == "false"):
                string += self.cgen_sexp_false(sexp)
            elif(sexp.leaf[0].lower() == "new"):
                string += self.cgen_sexp_new(sexp)
            elif(sexp.leaf[0].lower() == "null"):
                string += self.cgen_sexp_null(sexp)
            elif(sexp.leaf[0] == "."):
                string += self.cgen_sexp_dot(sexp)
            elif(sexp.leaf[0] == "["):
                string += self.cgen_sexp_lsb(sexp)
            else:
                string += self.cgen_sexp_number(sexp)
        else:
            string += self.cgen_pexp(sexp)
        string += "//EO_SEXP"
        return string

    def cgen_sexp_not(self,sexp_not):
        string = "//SEXP_NOT"
        str1 = self.cgen_sexp(sexp_not.children[0])
        string += (
            f"{str1}\n"
            f"nor $a0 $a0 $zero\n"
        )
        string += "//EO_SEXP_NOT"
        return string

    def cgen_sexp_minus(self,sexp_minus):
        string = "//SEXP_minus"
        str1 = self.cgen_sexp(sexp_minus.children[0])
        string += (
            f"{str1}\n"
            f"neg $a0 $a0\n"
        )
        string += "//EO_SEXP_minus"
        return string

    def cgen_sexp_true(self,sexp_true):
        string = "//SEXP_true"
        string += (
            f"li $a0 1\n"
        )
        string += "//EO_SEXP_true"
        return string

    def cgen_sexp_false(self,sexp_false):
        string = "//SEXP_false"
        string += (
            f"li $a0 0\n"
        )
        string += "//EO_SEXP_false"
        return string

    def cgen_sexp_number(self,sexp_number):
        string = "//SEXP_number"
        num = int(sexp_number.children[0])
        string += (
            f"li $a0 {num}\n"
        )
        string += "//EO_SEXP_number"
        return string

    def cgen_sexp_null(self,sexp_null):
        string = "//SEXP_null"
        string += (
            f"li $a0 0\n"
        )
        string += "//EO_SEXP_null"
        return string

    def cgen_sexp_new(self,sexp_new):
        pass

    def cgen_sexp_dot(self,sexp_dot):
        pass

    def cgen_sexp_lsb(self,sexp_lsb):
        pass

    def cgen_sexp_pexp(self,sexp_pexp):
        string = "//SEXP_pexp"
        string += self.cgen_pexp(sexp_pexp.children[0])
        string += "//EO_SEXP_pexp"
        return string

    #--------------PEXP--------------#

    def cgen_pexp(self,pexp_id):
        pass

    def cgen_pexp_id(self,pexp_id):
        pass

    def cgen_pexp_this(self,pexp_this):
        pass

    def cgen_pexp_new(self,pexp_new):
        pass

    def cgen_pexp_lp(self,pexp_lp):
        pass

    def cgen_pexp_pexp(self,pexp_pexp):
        pass

    def cgen_pexp_pexplp(self,pexp_pexplp):
        pass

    #--------------EXPS--------------#

    def cgen_exps_exp(self,exps_exp):
        pass

    #--------------[OPICIONAL]--------------#

    def cgen_optextends_part(self,optextends_part):
        pass

    def cgen_optparams_part(self,optparams_part):
        pass

    def cgen_optexps_part(self,optexps_part):
        pass

    #--------------{LOOP}--------------#

    def cgen_loopvar_ini(self,loopvar_ini):
        string = "//LOOPvar\n"
        if(len(loopvar_ini.children) != 0):
            string += self.cgen_var_tipo(loopvar_ini.children[0])
            string += self.cgen_loopvar_ini(loopvar_ini.children[1])
        string += "//EO_LOOPvar\n"
        return string

    def cgen_loopmetodo_ini(self,loopmetodo_ini):
        string = "//LOOPmetodo\n"
        if(len(loopmetodo_ini.children) != 0):
            string += self.cgen_metodo_public(loopmetodo_ini.children[0])
            string += self.cgen_loopmetodo_ini(loopmetodo_ini.children[1])
        string += "//EO_LOOPmetodo\n"
        return string

    def cgen_loopclasse_ini(self,loopclasse_ini):
        string = "//LOOPCLASSE\n"
        if(len(loopclasse_ini.children) != 0):
            string += self.cgen_classe_id(loopclasse_ini.children[0])
            string += self.cgen_loopclasse_ini(loopclasse_ini.children[1])
        string += "//EO_LOOPCLASSE\n"
        return string

    def cgen_loopcmd_ini(self,loopcmd_ini):
        string = "//LOOPcmd\n"
        if(len(loopcmd_ini.children) != 0):
            string += self.cgen_cmd(loopcmd_ini.children[0])
            string += self.cgen_loopcmd_ini(loopcmd_ini.children[1])
        string += "//EO_LOOPcmd\n"
        return string

    def cgen_loopvirgulatipoid_ini(self,loopvirgulatipoid_ini):
        pass

    def cgen_loopvirgulaexp_ini(self,loopvirgulaexp_ini):
        pass

    #------------------------------FIM------------------------------#

