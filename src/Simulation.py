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
        self.all_drones: list[Drone] = []
        self.drones: list[Drone] = []
        self.output: str = ""
        self.finished = False

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
            import os
            if os.path.exists("output.txt"):
                os.remove("output.txt")
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
            drone = Drone(self.start_hub)
            self.drones.append(drone)
        self.all_drones = self.drones.copy()

    def next_turn(self) -> str:
        self.__validate()
        if self.finished is True:
            return "FINISHED"
        turn_output: str = ""
        if isinstance(self.graph, Graph):
            start_hub = self.graph.start_hub
            end_hub = self.graph.end_hub
        else:
            raise ValueError("ERROR: Something went wrong during Graph "
                             "configure() method.")

        i = 0
        for drone in self.drones:
            i += 1
            if (isinstance(start_hub, Zone) and
               isinstance(end_hub, Zone)):
                action_output = drone.act(start_hub, end_hub)
            else:
                raise ValueError("ERROR: Something went wrong during map "
                                 "parsing.")
            turn_output += action_output
            if i < len(self.drones) and action_output:
                turn_output += " "

        i = 0
        for drone in self.drones:
            if drone.finished_traversal is True:
                del self.drones[i]
            i += 1
        if len(self.drones) < 1:
            self.finished = True

        self.output += turn_output + "\n"
        self.__write_output_file()
        return turn_output

    def restart_simulation(self) -> None:
        self.__validate()
        self.finished = False

        # Remove drones from all zones
        if isinstance(self.graph, Graph):
            if isinstance(self.graph.hubs, list):
                for zone in self.graph.hubs:
                    zone.drones_in.clear()
            if isinstance(self.graph.connections, list):
                for connection in self.graph.connections:
                    connection.drones_in.clear()


        # Remove self.route from all drones
        for drone in self.all_drones:
            if isinstance(self.graph, Graph):
                if isinstance(self.graph.start_hub, Zone):
                    drone.reset()
        self.all_drones.clear()
        self.drones.clear()
        
        if isinstance(self.graph, Graph):
            for _ in range(self.graph.nb_drones):
                if isinstance(self.graph.start_hub, Zone):
                    drone = Drone(self.graph.start_hub)
                    self.drones.append(drone)
        self.all_drones = self.drones.copy()

        self.output = ""

        import os
        if os.path.exists("output.txt"):
            os.remove("output.txt")

    def __write_output_file(self) -> None:
        with open("output.txt", "w") as file:
            file.write(self.output)

    def __validate(self) -> None:
        if not self.graph:
            raise ValueError("ERROR: Simulation configure() method must run "
                             "before anything else.")
