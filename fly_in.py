from src.MapParser import MapParser
import sys


if __name__ == "__main__":
    argv = sys.argv
    argc = len(sys.argv)
    if argc == 2:
        try:
            raw = MapParser.load_data(argv[1])
            res = MapParser.parse_data(raw)
            print(res)
        except Exception as e:
            print(e)
            sys.exit(1)
