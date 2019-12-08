import src.node as nd
import src.sem as sm

class Code:
    def __init__(self,stab):
        self.stab = stab
        self.beq_counter = 0
        self.exe_table = None
        self.currClass = None
        self.currMethod = None

    #passa arvore sintatica
    def gera_mips(self,tree):
        self.currClass = None
        self.currMethod = None
        self.exe_table = dict()
        with open('out.asm', 'w') as out:
            str1 = ""
            for classe in self.stab.keys():
                for metodo in self.stab[classe].keys():
                    clm = self.stab[classe][metodo]
                    # print("clm params", clm.params)
                    # print("clm scope", clm.scopeVars)
                    if clm.scopeVars is not None:
                        for vname in clm.scopeVars.keys():
                            va = clm.scopeVars[vname]
                            if va.paramlen is None: # É variável
                                if va.vtype == 'array':
                                    try:
                                        str1 += f"{classe}_{metodo}_{vname}: .word {', '.join(map(str, [0]*va.len))}\n"
                                    except:
                                        print(f"Array \'{vname}\' não inicializado, logo não foi escrito no .data")
                                else:
                                    str1 += f"{classe}_{metodo}_{vname}: .word 0\n"
            string = (
                f".data\n"
                f"newline: .asciiz \"\\n\"\n"
                f"{str1}"
                f".text\n"
            )
            string += self.cgen_prog_main(tree)
            string += "end_program:"
            out.write(string)
            print("Compilação concluída: Arquivo \'out.asm\' foi gerado com sucesso.")

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
        self.currClass = main_class.leaf[1].lower()
        self.currMethod = "main"
        string_ch1 = ""
        if(main_class.children[0] is not None):
            string_ch1 += self.cgen_cmd(main_class.children[0])

        # main por enquanto não avalia o args
        string = (
            f"exe_main:\n"
            f"  {string_ch1}"
            f"  b end_program\n"
        )
        return string

    #--------------CLASSE--------------#

    def cgen_classe_id(self,classe_id):
        self.currClass = classe_id.leaf[1].lower()
        self.currMethod = None
        string = f"class_{self.currClass}:\n"
        string += self.cgen_loopvar_ini(classe_id.children[1])
        string += self.cgen_loopmetodo_ini(classe_id.children[2])
        return string

    #--------------VAR--------------#

    def cgen_var_tipo(self,var_tipo):
        return ""

    #--------------METODO--------------#

    def cgen_metodo_public(self,metodo_public):
        # variável da classe já esta no .data
        # vl += self.cgen_loopvar_ini(metodo_public.children[2])
        self.currMethod = metodo_public.leaf[1].lower()
        n = self.stab[self.currClass][self.currMethod].paramlen
        z = 4 * n + 8
        cmds = self.cgen_loopcmd_ini(metodo_public.children[3])
        ret = self.cgen_exp(metodo_public.children[4])
        string = (
            f"def_{self.currClass}_{self.currMethod}:\n"
            f"move $fp, $sp\n"
            f"sw $ra, 0($sp)\n"
            f"addiu $sp, $sp, -4\n"
            f"# cmds do metodo\n"
            f"{cmds}"
            f"# retorno\n"
            f"{ret}"
            f"# prepara saida\n"
            f"lw $ra, 4($sp)\n"
            f"addiu $sp, $sp, {z}\n"
            f"lw $fp, 0($sp)\n"
            f"jr $ra\n\n"
        )
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
        string = ""
        string += self.cgen_loopcmd_ini(cmd_chave.children[0])
        return string

    def cgen_cmd_if(self,cmd_if):
        string = ""
        cond = self.cgen_exp(cmd_if.children[0])
        str1 = self.cgen_exp(cmd_if.children[1])
        string += (
            f"{cond}\n"
            f"sw $a0, 0($sp)\n"
            f"addiu $sp, $sp, -4\n"
            f"beq $a0, $zero, false{self.beq_counter}\n"
            f"{str1}\n"
            f"false{self.beq_counter}:\n"
            f"addiu $sp, $sp, 4\n"
            )
        self.beq_counter += 1
        return string

    def cgen_cmd_ifelse(self,cmd_ifelse):
        string = ""
        cond = self.cgen_exp(cmd_ifelse.children[0])
        str1 = self.cgen_cmd(cmd_ifelse.children[1])
        str2 = self.cgen_cmd(cmd_ifelse.children[2])
        string += (
            f"{cond}\n"
            f"sw $a0, 0($sp)\n"
            f"addiu $sp, $sp, -4\n"
            f"bne $a0, $zero, true{self.beq_counter}\n"
            f"{str2}\n"
            f"b eo_true{self.beq_counter}\n"
            f"true{self.beq_counter}:\n"
            f"{str1}\n"
            f"eo_true{self.beq_counter}:\n"
            f"addiu $sp, $sp, 4\n"
            )
        self.beq_counter += 1
        return string

    def cgen_cmd_while(self,cmd_while):
        string = ""
        cond = self.cgen_exp(cmd_ifelse.children[0])
        str1 = self.cgen_cmd(cmd_ifelse.children[1])
        string += (
            f"{cond}\n"
            f"sw $a0, 0($sp)\n"
            f"addiu $sp, $sp, -4\n"
            f"start{self.beq_counter}:\n"
            f"beq $a0, $zero, false{self.beq_counter}\n"
            f"{str1}\n"
            f"b start{self.beq_counter}\n"
            f"false{self.beq_counter}:\n"
            f"addiu $sp, $sp, 4\n"
            )
        self.beq_counter += 1
        return string

    def cgen_cmd_sout(self,cmd_sout):
        exp = self.cgen_exp(cmd_sout.children[0])
        string = (
            f"#sout\n"
            f"{exp}"
            f"li $v0, 1 # especifica o servico de print int\n"
            f"syscall # printa o $a0\n"
            f"li $v0, 4 # especifica o servico de print string\n"
            f"la $a0, newline\n"
            f"syscall # printa o newline\n"
            f"# eo_sout\n"
        )
        return string

    def cgen_cmd_ideq(self,cmd_ideq):
        string = ""
        var = cmd_ideq.leaf[0].lower()
        cname = self.currClass
        mname = self.currMethod
        str1 = self.cgen_exp(cmd_ideq.children[0])
        if str1 == "":
            return ""
        else:
            string += (
                f"{str1}"
                f"# Computou a expressao\n"
                f"la $t1, {cname}_{mname}_{var}\n"
                f"sw $a0, 0($t1) #Atribuiu a variavel\n"
            )
        return string

    def cgen_cmd_id(self,cmd_id):
        string = ""
        var = cmd_id.leaf[0].lower()
        cname = self.currClass
        mname = self.currMethod
        str1 = self.cgen_exp(cmd_id.children[1])

        # pega posição do array desde que seja estática
        child = cmd_id.children[0]
        while len(child.children) > 0:
            child = child.children[0]
        i = int(child.leaf[0])
        pos = 4 * i

        string += (
            f"{str1}"
            f"# Computou a expressao\n"
            f"la $t1, {cname}_{mname}_{var}\n"
            f"sw $a0, {pos}($t1) #Atribuiu a posicao {i} do array\n"
        )
        return string

    #--------------EXP--------------#

    def cgen_exp(self,exp):
        string = ""
        if(len(exp.children) > 1):
            string += self.cgen_exp_exp(exp)
        else:
            string += self.cgen_exp_rexp(exp)
        return string


    def cgen_exp_exp(self,exp_exp):
        string = ""
        str1 = cgen(exp_exp.children[0])
        str2 = cgen(exp_rexp.children[1])
        string += (
            f"{str1}\n"
            f"sw $a0, 0($sp)\n"
            f"addiu $sp, $sp, -4\n"
            f"{str2}\n"
            f"lw $t1, 4($sp)\n"
            f"and $a0, $t1, $a0\n"
            f"addiu $sp, $sp, 4\n"
        )
        return string

    def cgen_exp_rexp(self,exp_rexp):
        string = ""
        string += self.cgen_rexp(exp_rexp.children[0])
        return string

    #--------------REXP--------------#

    def cgen_rexp(self,rexp):
        string = ""
        if(len(rexp.children) > 1):
            string += self.cgen_rexp_rexp(rexp)
        else:
            string += self.cgen_rexp_aexp(rexp)
        return string

    def cgen_rexp_rexp(self,rexp_rexp):
        string = ""
        str1 = self.cgen_rexp(rexp_rexp.children[0])
        str2 = self.cgen_aexp(rexp_rexp.children[1])
        if(rexp_rexp.leaf[0] == "<"):
            string += (
                f"{str1}\n"
                f"sw $a0, 0($sp)\n"
                f"addiu $sp, $sp, -4\n"
                f"{str2}\n"
                f"lw $t1, 4($sp)\n"
                f"slt $a0, $t1, $a0\n"
                f"addiu $sp, $sp, 4\n"
            )
        elif(rexp_rexp.leaf[0] == ">"):
            string += (
                f"{str1}\n"
                f"sw $a0, 0($sp)\n"
                f"addiu $sp, $sp, -4\n"
                f"{str2}\n"
                f"lw $t1, 4($sp)\n"
                f"slt $a0, $a0, $t1\n"
                f"addiu $sp, $sp, 4\n"
            )
        elif(rexp_rexp.leaf[0] == "=="):
            string += (
                f"{str1}\n"
                f"sw $a0, 0($sp)\n"
                f"addiu $sp, $sp, -4\n"
                f"{str2}\n"
                f"lw $t1, 4($sp)\n"
                f"beq $a0, $t1, true{self.beq_counter}\n"
                f"li $a0, 0\n"
                f"b eo_true{self.beq_counter}\n"
                f"true{self.beq_counter}:\n"
                f"li $a0, 1\n"
                f"eo_true{self.beq_counter}:\n"
                f"addiu $sp, $sp, 4\n"
            )
            self.beq_counter += 1
        elif(rexp_rexp.leaf[0] == "!="):
            string += (
                f"{str1}\n"
                f"sw $a0, 0($sp)\n"
                f"addiu $sp, $sp, -4\n"
                f"{str2}\n"
                f"lw $t1, 4($sp)\n"
                f"bne $a0, $t1, true{self.beq_counter}\n"
                f"li $a0, 0\n"
                f"b eo_true{self.beq_counter}\n"
                f"true{self.beq_counter}:\n"
                f"li $a0, 1\n"
                f"eo_true{self.beq_counter}:\n"
                f"addiu $sp, $sp, 4\n"
            )
            self.beq_counter += 1
        elif(rexp_rexp.leaf[0] == "<="):
            string += (
                f"{str1}\n"
                f"sw $a0, 0($sp)\n"
                f"addiu $sp, $sp, -4\n"
                f"{str2}\n"
                f"lw $t1, 4($sp)\n"
                f"slt $a0, $a0, $t1\n"
                f"beq $a0, $zero, true{self.beq_counter}\n"
                f"li $a0, 0\n"
                f"b eo_true{self.beq_counter}\n"
                f"true{self.beq_counter}:\n"
                f"li $a0, 1\n"
                f"eo_true{self.beq_counter}:\n"
                f"addiu $sp, $sp, 4\n"
            )
            self.beq_counter += 1
        elif(rexp_rexp.leaf[0] == ">="):
            string += (
                f"{str1}\n"
                f"sw $a0, 0($sp)\n"
                f"addiu $sp, $sp, -4\n"
                f"{str2}\n"
                f"lw $t1, 4($sp)\n"
                f"slt $a0, $t1, $a0\n"
                f"beq $a0, $zero, true{self.beq_counter}\n"
                f"li $a0, 0\n"
                f"b eo_true{self.beq_counter}\n"
                f"true{self.beq_counter}:\n"
                f"li $a0, 1\n"
                f"eo_true{self.beq_counter}:\n"
                f"addiu $sp, $sp, 4\n"
            )
            self.beq_counter += 1
        return string

    def cgen_rexp_aexp(self,resp_aexp):
        string = ""
        string += self.cgen_aexp(resp_aexp.children[0])
        return string

    #--------------AEXP--------------#

    def cgen_aexp(self,aexp):
        string = ""
        if(len(aexp.children) > 1):
            string += self.cgen_aexp_aexp(aexp)
        else:
            string += self.cgen_aexp_mexp(aexp)
        return string

    def cgen_aexp_aexp(self,aexp_aexp):
        string = ""
        str1 = self.cgen_aexp(aexp_aexp.children[0])
        str2 = self.cgen_aexp(aexp_aexp.children[1])
        op = "add"
        if(aexp_aexp.leaf[0] == "-"):
            op = "sub"
        string += (
            f"{str1}"
            f"sw $a0, 0($sp)\n"
            f"addiu $sp, $sp, -4\n"
            f"{str2}"
            f"lw $t1, 4($sp)\n"
            f"{op} $a0, $t1, $a0\n"
            f"addiu $sp, $sp, 4\n"
        )
        return string

    def cgen_aexp_mexp(self,aexp_mexp):
        string = ""
        string += self.cgen_mexp(aexp_mexp.children[0])
        return string

    #--------------MEXP--------------#

    def cgen_mexp(self,mexp):
        string = ""
        if(len(mexp.children) > 1):
            string += self.cgen_mexp_mexp(mexp)
        else:
            string += self.cgen_mexp_sexp(mexp)
        return string

    def cgen_mexp_mexp(self,mexp_mexp):
        string = ""
        str1 = self.cgen_mexp(mexp_mexp.children[0])
        str2 = self.cgen_mexp(mexp_mexp.children[1])
        op = "mul"
        string += (
            f"{str1}"
            f"sw $a0, 0($sp)\n"
            f"addiu $sp, $sp, -4\n"
            f"{str2}"
            f"lw $t1, 4($sp)\n"
            f"{op} $a0, $t1, $a0\n"
            f"addiu $sp, $sp, 4\n"
        )
        return string

    def cgen_mexp_sexp(self,mexp_sexp):
        string = ""
        string += self.cgen_sexp(mexp_sexp.children[0])
        return string

    #--------------SEXP--------------#

    def cgen_sexp(self,sexp):
        string = ""
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
        return string

    def cgen_sexp_not(self,sexp_not):
        string = ""
        str1 = self.cgen_sexp(sexp_not.children[0])
        string += (
            f"{str1}\n"
            f"beq $a0 $zero zerocheck_{self.beq_counter}\n"
            f"li $a0 0\n"
            f"b eo_zerocheck_{self.beq_counter}\n"
            f"zerocheck_{self.beq_counter}:\n"
            f"li $a0 1\n"
            f"eo_zerocheck_{self.beq_counter}:\n"
        )
        self.beq_counter += 1
        return string

    def cgen_sexp_minus(self,sexp_minus):
        string = ""
        str1 = self.cgen_sexp(sexp_minus.children[0])
        string += (
            f"{str1}\n"
            f"neg $a0 $a0\n"
        )
        return string

    def cgen_sexp_true(self,sexp_true):
        string = ""
        string += (
            f"li $a0, 1\n"
        )
        return string

    def cgen_sexp_false(self,sexp_false):
        string = ""
        string += (
            f"li $a0, 0\n"
        )
        return string

    def cgen_sexp_number(self,sexp_number):
        string = ""
        num = int(sexp_number.leaf[0])
        string += (
            f"li $a0, {num}\n"
        )
        return string

    def cgen_sexp_null(self,sexp_null):
        string = ""
        string += (
            f"li $a0, 0\n"
        )
        return string

    def cgen_sexp_new(self,sexp_new):
        # inicialização do array é feito no gera_mips
        return ""

    def cgen_sexp_dot(self,sexp_dot):
        string = ""
        var = sexp_dot.children[0].leaf[0].lower()
        metodo = self.stab[self.currClass][self.currMethod]
        arrlen = metodo.scopeVars[var].len
        string += (
            f"li $a0, {arrlen}\n"
        )
        return string

    def cgen_sexp_lsb(self,sexp_lsb):
        string = ""
        var = sexp_lsb.children[0].leaf[0].lower()
        cname = self.currClass
        mname = self.currMethod

        # pega posição do array desde que seja estática
        child = sexp_lsb.children[1]
        while True:
            child = child.children[0]
            if len(child.children) < 1:
                break
        pos = 4 * int(child.leaf[0])

        string += (
            f"la $t1, {cname}_{mname}_{var}\n"
            f"lw $a0, {pos}($t1)\n"
        )
        return string

    def cgen_sexp_pexp(self,sexp_pexp):
        string = ""
        string += self.cgen_pexp(sexp_pexp.children[0])
        return string

    #--------------PEXP--------------#

    def cgen_pexp(self,pexp):
        string = ""
        if (len(pexp.children[0].leaf) == 1 
            and pexp.children[0].leaf[0].lower() != "this"):
            string += self.cgen_pexp_id(pexp.children[0])

        elif (len(pexp.children[0].leaf) == 2
            and pexp.children[0].leaf[0] == "("):
            string += self.cgen_pexp_lp(pexp.children[0])

        elif (len(pexp.children[0].leaf) == 2
            and pexp.children[0].leaf[0] != "("):
            string += self.cgen_pexp_pexp(pexp.children[0])

        elif (len(pexp.children[0].leaf) == 4
            and pexp.children[0].leaf[0].lower() != "new"):
            string += self.cgen_pexp_pexplp(pexp.children[0])

        return string

    def cgen_pexp_id(self,pexp_id):
        # retorna valor do id
        vname = pexp_id.leaf[0].lower()
        cname = self.currClass
        mname = self.currMethod
        scopeVars = self.stab[cname][mname].scopeVars
        params = self.stab[cname][mname].params

        if scopeVars is not None and vname in scopeVars.keys():
            var_str = f"{cname}_{mname}_{vname}"
            string = (
                f"la $t1, {var_str}\n"
                f"lw $a0, 0($t1) # Acessa variavel\n"
            )
        else:
            i = 1
            for pa in params.keys():
                if pa == vname:
                    z = 4 * i
                    string = (
                        f"lw $a0, {z}($fp) # Pega arg do metodo\n"
                    )
                    break
                else:
                    i += 1

        return string

    def cgen_pexp_this(self,pexp_this):
        # folha sem efeito no cgen
        # variável acessada pelo 'cgen_pexp_pexp'
        return ""

    def cgen_pexp_new(self,pexp_new):
        # Construtor de classe sem efeito no cgen
        # pois construtores não recebem argumentos
        return ""

    def cgen_pexp_lp(self,pexp_lp):
        string = self.cgen_exp(pexp_lp.children[0])
        return string

    def cgen_pexp_pexp(self,pexp_pexp):
        # acessa propriedade de classe
        vname = pexp_pexp.leaf[1].lower()

        cname = self.currClass
        mname = self.currMethod
        string = (
            f"la $t1, {cname}_{mname}_{vname}\n"
            f"lw $a0, 0($t1)\n"
        )
        return string

    def cgen_pexp_pexplp(self,pexp_pexplp):
        # execução de método da classe
        vname = pexp_pexplp.leaf[1].lower()

        # new Classe().metodo()
        if len(pexp_pexplp.children[0].leaf) > 1:
            cname = pexp_pexplp.children[0].leaf[1].lower()
        # this.metodo()
        else:
            cname = self.currClass

        paramlen = self.stab[cname][vname].paramlen
        params = self.stab[cname][vname].params
        optexps = self.cgen_optexps_part(pexp_pexplp.children[1])
        label = f"exe_{cname}_{vname}"
        if label in self.exe_table:
            self.exe_table[label] +=1
            label += f"{self.exe_table[label]}"
        else:
            self.exe_table[label] = 1
            label += f"{self.exe_table[label]}"
        string = (
            f"{label}:\n"
            f"sw $fp, 0($sp)\n"
            f"addiu $sp, $sp, -4\n"
            f"{optexps}"
            f"jal def_{cname}_{vname}\n"
        )
        # for k in sorted(params.keys(), reverse=True):
        #     print("k: ",k)

        return string

    #--------------EXPS--------------#

    def cgen_exps_exp(self,exps_exp):
        exp = self.cgen_exp(exps_exp.children[0])
        loopvirg = self.cgen_loopvirgulaexp_ini(exps_exp.children[1])
        string = (
            f"{loopvirg}"
            f"{exp}"
            f"sw $a0, 0($sp)\n"
            f"addiu $sp, $sp, -4\n"
        )
        return string

    #--------------[OPICIONAL]--------------#

    def cgen_optextends_part(self,optextends_part):
        # verificação de extenção
        pass

    def cgen_optparams_part(self,optparams_part):
        # montagem dos params da def do método
        # contagem feita na analise semantica
        pass

    def cgen_optexps_part(self,optexps_part):
        # verificação de arg da chamada do método
        string = ""
        if len(optexps_part.children) > 0:
            string += self.cgen_exps_exp(optexps_part.children[0])
        return string

    #--------------{LOOP}--------------#

    def cgen_loopvar_ini(self,loopvar_ini):
        string = ""
        if(len(loopvar_ini.children) != 0):
            string += self.cgen_var_tipo(loopvar_ini.children[0])
            string += self.cgen_loopvar_ini(loopvar_ini.children[1])
        return string

    def cgen_loopmetodo_ini(self,loopmetodo_ini):
        string = ""
        if(len(loopmetodo_ini.children) != 0):
            string += self.cgen_metodo_public(loopmetodo_ini.children[0])
            string += self.cgen_loopmetodo_ini(loopmetodo_ini.children[1])
        return string

    def cgen_loopclasse_ini(self,loopclasse_ini):
        string = ""
        if(len(loopclasse_ini.children) != 0):
            string += self.cgen_classe_id(loopclasse_ini.children[0])
            string += self.cgen_loopclasse_ini(loopclasse_ini.children[1])
        return string

    def cgen_loopcmd_ini(self,loopcmd_ini):
        string = ""
        if(len(loopcmd_ini.children) != 0):
            string += self.cgen_cmd(loopcmd_ini.children[0])
            string += self.cgen_loopcmd_ini(loopcmd_ini.children[1])
        return string

    def cgen_loopvirgulatipoid_ini(self,loopvirgulatipoid_ini):
        # verificação de param da def do método
        # contagem dos parametros da def feitas
        # na análise semantica
        pass

    def cgen_loopvirgulaexp_ini(self,loopvirgulaexp_ini):
        # verificação de arg da chamada do método
        string = ""
        if len(loopvirgulaexp_ini.children) > 0:
            exp = self.cgen_exp(loopvirgulaexp_ini.children[0])
            loopvirg = self.cgen_loopvirgulaexp_ini(loopvirgulaexp_ini.children[1])
            string = (
                f"{loopvirg}"
                f"{exp}"
                f"sw $a0, 0($sp)\n"
                f"addiu $sp, $sp, -4\n"
            )
        return string

    #------------------------------FIM------------------------------#

