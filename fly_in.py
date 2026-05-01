from src.MapParser import MapParser
from src.Graphics import Graphics
from src.GraphGenerator import GraphGenerator
import sys
from src.GraphLogic import Zone


if __name__ == "__main__":
    argv = sys.argv
    argc = len(sys.argv)
    if argc == 2:
        try:
            raw = MapParser.load_data(argv[1])
            res = MapParser.parse_data(raw)
            GraphGenerator.configure_graph(res)
            GraphGenerator.generate_graph()
        except Exception as e:
            print(e)
            sys.exit(1)
