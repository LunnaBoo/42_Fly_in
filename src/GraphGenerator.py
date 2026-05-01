from src.GraphLogic import Zone, Connection
from typing import Any


class GraphGenerator:
    zones: list[Zone] = []
    connections: list[Connection] = []
    nb_drones: int = 0

    @classmethod
    def generate_graph(cls) -> dict[Zone, list[Connection]]:
        """
        Generates a graph based on it's class attributes 
        represented by an adjacency list.

        Returns
        -------
        dict[Zone, Connection | None]:
            A dictionary with Zone objects as keys and a list of
            Connection objects as values.
        """

        if len(cls.zones) < 1 or len(cls.connections) < 1 or cls.nb_drones < 1:
            raise ValueError
        graph: dict[Zone, list[Connection]] = {}
        for zone in cls.zones:
            zone_connections = []
            for connection in cls.connections:
                if connection.previous_zone == zone or connection.next_zone == zone:
                    zone_connections.append(connection)
            graph[zone] = zone_connections
        return graph

    @classmethod
    def configure_graph(cls, map: dict[str, Any]) -> None:
        """
        Gets parsed data from MapParser and stores it as class attributes
        later used in the generate_graph() method.

        Parameters
        ----------
        map: dict[str, Any]
            Data read from a text file and parsed by MapParser class.
        """

        cls.nb_drones = map["nb_drones"]
        hubs = map["hubs"]
        connections = map["connections"]
        for key in hubs:
            zone = hubs[key]
            cls.zones = zone._all_zones
            break
        for key in connections:
            connection = connections[key]
            cls.connections = connection._all_connections
            break
