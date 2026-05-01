from src.GraphLogic import Zone, Connection
from src.GraphGenerator import GraphGenerator
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
    def configure_simulation(cls, map: dict[str, Any]) -> None:
        """
        Generates the graph structure based on data passed as
        parameter and stores the data and graph as class attributes.

        Parameters
        ----------
        map: dict[str, Any]
            Dictionary with all data regarding the graph and simulation.
        """

        try:
            GraphGenerator.configure_graph(map)
        except ValueError:
            raise ValueError("Simulation ERROR: configure_simulation() "
                             "method must be ran before run_simulation()!")
        cls.graph = GraphGenerator.generate_graph()
        cls.zones = GraphGenerator.zones
        cls.connections = GraphGenerator.connections
        cls.nb_drones = GraphGenerator.nb_drones
        for _ in range(cls.nb_drones):
            drone = Drone()
            cls.drones = drone._all_drones

    @classmethod
    def __run_turn(cls) -> str: ...

    @classmethod
    def run_simulation(cls) -> str: ...
