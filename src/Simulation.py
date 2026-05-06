from src.MapParser import MapParser
from src.GraphLogic import Zone, Connection, GraphGenerator
from src.Drone import Drone
from typing import Any


class Simulation:
    graph: dict[Zone, list[Connection]] = {}
    zones: list[Zone] = []
    connections: list[Connection] = []
    drones: list[Drone] = []
    nb_drones: int = 0
    output: str = ""

    @classmethod
    def configure(cls, filename: str) -> None:
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
        except ValueError as e:
            raise ValueError(e)
        cls.graph = GraphGenerator.generate_graph(map)
        cls.zones = map["hub"]._all_zones
        cls.connections = map["connection"]._all_connections
        cls.nb_drones = map["nb_drones"]
        for _ in range(cls.nb_drones):
            drone = Drone()
            cls.drones = drone._all_drones

    @classmethod
    def __run_turn(cls) -> str: ...

    @classmethod
    def run(cls) -> str:
        output: str = ""
        if not cls.graph:
            raise ValueError("ERROR: Simulation configure() method must run "
                             "before run() method.")

        return output
