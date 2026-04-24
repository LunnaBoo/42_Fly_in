from src.MapParser import MapParser
from src.GraphGenerator import GraphGenerator
from src.Graphics import Graphics
import sys
from src.Zone import Zone


if __name__ == "__main__":
    argv = sys.argv
    argc = len(sys.argv)
    if argc == 2:
        try:
            raw = MapParser.load_data(argv[1])
            res = MapParser.parse_data(raw)
            print(res)
            graph_gen = GraphGenerator(res)
            graph_res = graph_gen.generate_graph()
            graph = graph_res["graph"]
            def print_ascii_graph() -> None:
                for row in graph:
                    print()
                    for item in row:
                        if isinstance(item, Zone):
                            print(1, end=" ")
                        else:
                            print(0, end=" ")
                print()
            width = graph_res["width"]
            height = graph_res["height"]
            Graphics.render_frame(graph, width, height)
        except Exception as e:
            print(e)
            sys.exit(1)
