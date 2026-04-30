from src.MapParser import MapParser
from src.GraphGenerator import GraphGenerator
from src.Graphics import Graphics
import sys
from src.GraphLogic import Zone


if __name__ == "__main__":
    argv = sys.argv
    argc = len(sys.argv)
    if argc == 2:
        try:
            raw = MapParser.load_data(argv[1])
            res = MapParser.parse_data(raw)
            zone1 = res["hubs"]["start"]
            print(zone1.name)
            graph_gen = GraphGenerator(res)
            graph_res = graph_gen.generate_graph()
            graph = graph_res["graph"]
            width = graph_res["width"]
            height = graph_res["height"]
        except Exception as e:
            print(e)
            sys.exit(1)
