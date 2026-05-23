from src.MapParser import MapParser
from src.GraphLogic import Zone, Connection, GraphGenerator
from src.Drone import Drone
from src.GridGenerator import GridGenerator
from typing import Any
import sys


class Simulation:
    def __init__(self) -> None:
        self.graph: dict[Zone, list[Connection]] = {}
        self.zones: list[Zone] = []
        self.connections: list[Connection] = []
        self.drones: list[Drone] = []
        self.nb_drones: int = 0
        self.output: str = ""
        self.grid: list[list[Zone | int]] | None = None
        self.grid_height: int = 0
        self.grid_width: int = 0
        self.y_offset: int = 0
        self.x_offset: int = 0

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
            grid_gen = GridGenerator(map)
            grid_data = grid_gen.generate_graph()
        except FileNotFoundError as e:
            print(f"ERROR: Map file not found: {e}")
            sys.exit(1)
        except PermissionError as e:
            print(f"ERROR: No permission to read map file: {e}")
            sys.exit(1)
        except Exception as e:
            print(e)
            sys.exit(1)
        self.graph = GraphGenerator.generate_graph(map)
        self.zones = map["hub"]._all_zones
        self.connections = map["connection"]._all_connections
        self.grid = grid_data["grid"]
        self.grid_height = grid_data["height"]
        self.grid_width = grid_data["width"]
        self.x_offset = grid_data["x_offset"]
        self.y_offest = grid_data["y_offset"]
        self.nb_drones = map["nb_drones"]
        for _ in range(self.nb_drones):
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
