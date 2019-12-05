import sys
import argparse
import src.cgen as cd
import src.parser as pa
import src.node as nd
import src.sem as sm

def run():
    entrada = argparse.ArgumentParser(description='faz o parser do Minijava.')
    entrada.add_argument('arquivo', type=str,
                    help='arquivo para parsear')
    entrada.add_argument('-g','--graph', action='store_true',
                    help='gera a arvore sintatica no graphviz')

    args = entrada.parse_args()
    parser = pa.Parser()
    tree = parser.run(args.arquivo)
    if args.graph:
        print(nd.tree_to_graphviz(tree))
    else:
        nd.print_tree(tree)
    
    sa = sm.Semantic()
    sa.make_table(tree)
    tab = sa.stab
    
    cg = cd.Code(tab)
    cg.gera_mips(tree)


if __name__ == '__main__':
    run()

#python main.py | dot -T png | display