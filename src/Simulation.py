from src.MapParser import MapParser
from src.GraphLogic import Graph, Zone, Connection
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
            graph.configure(map)
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
        turn_output: str = ""
        if isinstance(self.graph, Graph):
            start_hub = self.graph.start_hub
            end_hub = self.graph.end_hub
        else:
            raise ValueError("ERROR: Something went wrong during Graph "
                             "configure() method.")

        for i in range(len(self.drones)):
            if (isinstance(start_hub, Zone) and
               isinstance(end_hub, Zone)):
                if self.drones[i].finished_traversal is True:
                    del self.drones[i]
                    continue
                action_output = self.drones[i].act(start_hub, end_hub)
            else:
                raise ValueError("ERROR: Something went wrong during map "
                                 "parsing.")
            turn_output += action_output
            if i != len(self.drones) and action_output:
                turn_output += " "

        self.output += turn_output + "\n"
        return turn_output

    def previous_turn(self) -> str:
        output: str = ""

        return output

    def validate(self) -> None:
        if not self.graph:
            raise ValueError("ERROR: Simulation configure() method must run "
                             "before anything else.")
