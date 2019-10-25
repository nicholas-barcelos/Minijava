import sys
import argparse

import src.parser as pa
import src.node as nd

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


if __name__ == '__main__':
    run()

#python main.py | dot -T png | display