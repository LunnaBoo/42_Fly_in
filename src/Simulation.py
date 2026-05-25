from src.MapParser import MapParser
from src.GraphLogic import Graph
from src.Drone import Drone
from src.Grid import Grid
from typing import Any
import sys


class Simulation:
    def __init__(self) -> None:
        self.graph: Graph | None = None
        self.grid: Grid | None = None
        self.drones: list[Drone] = []
        self.output: str = ""

    def configure(self, filename: str) -> None:
        """
        Generates the graph structure based on data passed as
        parameter and stores the data and graph as class attributes.

        Parameters
        ----------
        map: dict[str, Any]
            Dictionary with all data regarding the graph and simulation.
        """

        try:
            map: dict[str, Any] = MapParser.parse_data(filename)
            self.start_hub = map["start_hub"]
            self.end_hub = map["end_hub"]
            self.grid = Grid(map)
            self.grid.generate_grid()
            graph = Graph()
            graph.graph_config(map)
        except FileNotFoundError as e:
            print(f"ERROR: Map file not found: {e}")
            sys.exit(1)
        except PermissionError as e:
            print(f"ERROR: No permission to read map file: {e}")
            sys.exit(1)
        except Exception as e:
            print(e)
            sys.exit(1)
        self.graph = graph
        for _ in range(graph.nb_drones):
            drone = Drone()
            self.drones = drone._all_drones

    def next_turn(self) -> str:
        output: str = ""

        return output

    def previous_turn(self) -> str:
        output: str = ""

        return output

    def validate(self) -> None:
        if not self.graph:
            raise ValueError("ERROR: Simulation configure() method must run "
                             "before anything else.")
