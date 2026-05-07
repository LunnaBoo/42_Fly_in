from src.Simulation import Simulation
import sys
from src.GraphLogic import Zone


if __name__ == "__main__":
    argv = sys.argv
    argc = len(sys.argv)
    if argc == 2:
        try:
            Simulation.configure(argv[1])
        except Exception as e:
            print(e)
            sys.exit(1)
