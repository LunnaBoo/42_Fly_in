from typing import Any
import heapq


class Zone:
    _all_zones: list["Zone"] = []

    def __init__(self, name: str, zone_type: str,
                 pos: tuple[int, int],
                 is_start: bool = False,
                 is_end: bool = False,
                 max_drones: int = 1,
                 color: str | None = None) -> None:
        self.id: str = "Z" + str(len(Zone._all_zones) + 1)
        self.name = name
        self.zone_type = zone_type
        self.pos = pos
        self.is_start = is_start
        self.is_end = is_end
        self.max_drones = max_drones
        self.color = color
        self.drones_in: list = []
        self.grid_pos: tuple = (0, 0)
        Zone._all_zones.append(self)


class Connection:
    _all_connections: list["Connection"] = []

    def __init__(self, name: str,
                 previous_zone: Zone,
                 next_zone: Zone,
                 max_link_capacity: int = 1) -> None:
        self.id: str = "C" + str(len(Connection._all_connections) + 1)
        self.name = name
        self.previous_zone = previous_zone
        self.next_zone = next_zone
        self.max_link_capacity = max_link_capacity
        self.grid_pos: tuple[int, int] = (0, 0)
        self.char: str = ""
        Connection._all_connections.append(self)


class GraphGenerator:
    @staticmethod
    def generate_graph(map: dict[str, Any]) -> dict[Zone, list[Connection]]:
        """
        Generates a graph based on it's class attributes
        represented by an adjacency list.

        Returns
        -------
        dict[Zone, Connection | None]:
            A dictionary with Zone objects as keys and a list of
            Connection objects as values.
        """

        zones = map["hub"]._all_zones
        connections = map["connection"]._all_connections
        nb_drones = map["nb_drones"]
        if len(zones) < 1 or len(connections) < 1 or nb_drones < 1:
            raise ValueError
        graph: dict[Zone, list[Connection]] = {}
        for zone in zones:
            zone_connections = []
            for connection in connections:
                if (connection.previous_zone == zone or
                   connection.next_zone == zone):
                    zone_connections.append(connection)
            graph[zone] = zone_connections
        return graph



    @staticmethod
    def validate_graph(map: dict[str, Any]) -> None:
        zones = map["hub"]._all_zones
        connections = map["connection"]._all_connections
        nb_drones = map["nb_drones"]
        if len(zones) < 1 or len(connections) < 1 or nb_drones < 1:
            raise ValueError("ERROR: Map file is incomplete.")
