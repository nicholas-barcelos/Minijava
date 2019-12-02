import src.node as nd

def gera_mips(tree): #passa arvore sintatica
    with open('out.txt', 'w') as out:
        string = cgen_prog_main(tree)
        out.write(string)

    #--------------PROG--------------#

def cgen_prog_main(prog_main):
    if(prog_main.children[0] is not None):
        string_ch1 = cgen_main_class(prog_main.children[0])
    if(prog_main.children[1] is not None):
        string_ch2 = cgen_loopclasse_ini(prog_main.children[1])
    string = f"{string_ch1}\n{string_ch2}"
    return string

#--------------MAIN--------------#

def cgen_main_class(main_class):
    string_ch1 = "//MAINCLASS\n"
    if(main_class.children[0] is not None):
        string_ch1 += cgen_cmd(main_class.children[0])

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

def cgen_classe_id(classe_id):
    string = "//CLASSE_ID"
    string += cgen_loopvar_ini(classe_id.children[1])
    string += cgen_loopmetodo_ini(classe_id.children[2])
    string += "//EO_CLASSE_ID"
    return string

#--------------VAR--------------#

def cgen_var_tipo(var_tipo):
    pass

#--------------METODO--------------#

def cgen_metodo_public(metodo_public):
    pass

#--------------PARAMS--------------#

def cgen_params_tipo(params_tipo):
    pass

#--------------TIPO--------------#

def cgen_tipo_inta(tipo_inta):
    pass

def cgen_tipo_bool(tipo_bool):
    pass

def cgen_tipo_int(tipo_int):
    pass

def cgen_tipo_id(tipo_id):
    pass

#--------------CMD--------------#

def cgen_cmd(cmd):
    string_ch1 = ""
    if(cmd.leaf[0] == "{"):
        string_ch1 += cgen_cmd_chave(cmd)
        
    elif(cmd.leaf[0].lower() == "if" and len(cmd.leaf) < 4):
        string_ch1 += cgen_cmd_if(cmd)

    elif(len(cmd.leaf) > 3 and cmd.leaf[3].lower() == "else"):
        string_ch1 += cgen_cmd_ifelse(cmd)

    elif(cmd.leaf[0].lower() == "while"):
        string_ch1 += cgen_cmd_while(cmd)

    elif(cmd.leaf[0].lower() == "system.out.println"):
        string_ch1 += cgen_cmd_sout(cmd)

    elif(cmd.leaf[1].lower() == "="):
        string_ch1 += cgen_cmd_ideq(cmd)

    elif(cmd.leaf[1].lower() == "["):
        string_ch1 += cgen_cmd_id(cmd)
    return string_ch1

def cgen_cmd_chave(cmd_chave):
    return ""

def cgen_cmd_if(cmd_if):
    return ""

def cgen_cmd_ifelse(cmd_ifelse):
    return ""

def cgen_cmd_while(cmd_while):
    return ""

def cgen_cmd_sout(cmd_sout):
    return ""

def cgen_cmd_ideq(cmd_ideq):
    return ""

def cgen_cmd_id(cmd_id):
    return ""

#--------------EXP--------------#

def cgen_exp_exp(exp_exp):
    pass

def cgen_exp_rexp(exp_rexp):
    pass

#--------------REXP--------------#

def cgen_rexp_rexp(rexp_rexp):
    pass

def cgen_resp_aexp(resp_aexp):
    pass

#--------------AEXP--------------#

def cgen_aexp_aexp(aexp_aexp):
    pass

def cgen_aexp_mexp(aexp_mexp):
    pass

#--------------MEXP--------------#

def cgen_mexp_mexp(mexp_mexp):
    pass

def cgen_mexp_sexp(mexp_sexp):
    pass

#--------------SEXP--------------#

def cgen_sexp_not(sexp_not):
    pass

def cgen_sexp_minus(sexp_minus):
    pass

def cgen_sexp_true(sexp_true):
    pass

def cgen_sexp_false(sexp_false):
    pass

def cgen_sexp_number(sexp_number):
    pass

def cgen_sexp_null(sexp_null):
    pass

def cgen_sexp_new(sexp_new):
    pass

def cgen_sexp_dot(sexp_dot):
    pass

def cgen_sexp_lsb(sexp_lsb):
    pass

def cgen_sexp_pexp(sexp_pexp):
    pass

#--------------PEXP--------------#

def cgen_pexp_id(pexp_id):
    pass

def cgen_pexp_this(pexp_this):
    pass

def cgen_pexp_new(pexp_new):
    pass

def cgen_pexp_lp(pexp_lp):
    pass

def cgen_pexp_pexp(pexp_pexp):
    pass

def cgen_pexp_pexplp(pexp_pexplp):
    pass

#--------------EXPS--------------#

def cgen_exps_exp(exps_exp):
    pass

#--------------[OPICIONAL]--------------#

def cgen_optextends_part(optextends_part):
    pass

def cgen_optparams_part(optparams_part):
    pass

def cgen_optexps_part(optexps_part):
    pass

#--------------{LOOP}--------------#

def cgen_loopvar_ini(loopvar_ini):
    string = "//LOOPvar\n"
    if(len(loopvar_ini.children) != 0):
        string += cgen_var_tipo(loopvar_ini.children[0])
        string += cgen_loopvar_ini(loopvar_ini.children[1])
    string += "//EO_LOOPvar\n"
    return string

def cgen_loopmetodo_ini(loopmetodo_ini):
    string = "//LOOPmetodo\n"
    if(len(loopmetodo_ini.children) != 0):
        string += cgen_metodo_public(loopmetodo_ini.children[0])
        string += cgen_loopmetodo_ini(loopmetodo_ini.children[1])
    string += "//EO_LOOPmetodo\n"
    return string

def cgen_loopclasse_ini(loopclasse_ini):
    string = "//LOOPCLASSE\n"
    if(len(loopclasse_ini.children) != 0):
        string += cgen_classe_id(loopclasse_ini.children[0])
        string += cgen_loopclasse_ini(loopclasse_ini.children[1])
    string += "//EO_LOOPCLASSE\n"
    return string

def cgen_loopcmd_ini(loopcmd_ini):
    string = "//LOOPcmd\n"
    if(len(loopcmd_ini.children) != 0):
        string += cgen_cmd(loopcmd_ini.children[0])
        string += cgen_loopcmd_ini(loopcmd_ini.children[1])
    string += "//EO_LOOPcmd\n"
    return string

def cgen_loopvirgulatipoid_ini(loopvirgulatipoid_ini):
    pass

def cgen_loopvirgulaexp_ini(loopvirgulaexp_ini):
    pass

#------------------------------FIM------------------------------#

