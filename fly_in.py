import sys


if __name__ == "__main__":
    argc = len(sys.argv)
    if argc == 2:
        try:
            from src.App import FlyInApp
            app = FlyInApp()
            app.run()
            print("FLY_IN: Simulation data written to output.txt file.")
        except Exception as e:
            print(e)
            sys.exit(1)
    elif argc < 2:
        print("Missing arguments. Run 'python3 fly_in.py map.txt'")
        sys.exit(1)
    else:
        print("Too many arguments. Run 'python3 fly_in.py map.txt'")
        sys.exit(1)
