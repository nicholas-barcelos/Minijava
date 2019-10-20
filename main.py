import sys

import src.parser as pa
import src.node as nd

def run():
    parser = pa.Parser()
    tree = parser.run()
    if "-g" in sys.argv:
        print(nd.tree_to_graphviz(tree))
    else:
        nd.print_tree(tree)


if __name__ == '__main__':
    run()

#python main.py | dot -T png | display