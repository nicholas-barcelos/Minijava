import src.parser as pa
import src.node as nd

def run():
    parser = pa.Parser()
    tree = parser.run()
    nd.print_tree(tree)

if __name__ == '__main__':
    run()