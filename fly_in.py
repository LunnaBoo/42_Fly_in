from src.Simulation import Simulation
from src.Graphics import FlyInApp
import sys
from src.GraphLogic import Zone


if __name__ == "__main__":
    argv = sys.argv
    argc = len(sys.argv)
    if argc == 2:
        try:
            Simulation.configure(argv[1])
            app = FlyInApp(argv[1])
            app.run()
        except Exception as e:
            print(e)
            sys.exit(1)
    else:
        print("Missing arguments. Run 'python3 fly_in.py map.txt'")
