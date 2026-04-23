from src.MapParser import MapParser
from src.GraphGenerator import GraphGenerator
import sys
from src.Zone import Zone


if __name__ == "__main__":
    argv = sys.argv
    argc = len(sys.argv)
    if argc == 2:
        try:
            raw = MapParser.load_data(argv[1])
            res = MapParser.parse_data(raw)
            #print(res)
            graph_gen = GraphGenerator(res)
            graph = graph_gen.generate_graph()
            for row in graph:
                print()
                for item in row:
                    if isinstance(item, Zone):
                        print(1, end=" ")
                    else:
                        print(0, end=" ")
        except Exception as e:
            print(e)
            sys.exit(1)
