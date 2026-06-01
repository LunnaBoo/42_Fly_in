from typing import Any


class Zone:
    """

    """
    _all_zones: list["Zone"] = []

    def __init__(self, name: str, zone_type: str,
                 pos: tuple[int, int],
                 is_start: bool = False,
                 is_end: bool = False,
                 max_drones: int = 1,
                 color: str | None = None) -> None:
        self.id: str = "Z" + str(len(Zone._all_zones) + 1)
        self.name = name
        self.kind = zone_type
        self.pos = pos
        self.visited: bool = False
        self.is_start = is_start
        self.is_end = is_end
        self.max_drones = max_drones
        self.color = color
        self.weight: float = 1
        self.connections: list[Connection] = []
        self.drones_in: list = []
        self.grid_pos: tuple = (0, 0)
        if self.kind == "restricted":
            self.weight = 2
        elif self.kind == "priority":
            self.weight = 0.5
        elif self.kind == "blocked":
            self.weight = float("inf")
        Zone._all_zones.append(self)

    def __lt__(self, zone: Zone):
        if not isinstance(zone, Zone):
            raise ValueError("ERROR: Zone objects can only be "
                             "compared against other zone objects.")
        return self.weight < zone.weight


class Connection:
    """

    """
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
        self.drones_in: list = []
        Connection._all_connections.append(self)


class Graph:
    """

    """
    def __init__(self) -> None:
        self.hubs: list[Zone] | None = None
        self.connections: list[Connection] | None = None
        self.nb_drones: int = 0
        self.start_hub: Zone | None = None
        self.end_hub: Zone | None = None

    def configure(self, map: dict[str, Any]) -> None:
        """
        """

        zones = map["hub"]._all_zones
        connections = map["connection"]._all_connections
        nb_drones = map["nb_drones"]

        self.hubs = zones
        self.connections = connections
        self.nb_drones = nb_drones
        self.start_hub = map["start_hub"]
        self.end_hub = map["end_hub"]

        Graph.validate_graph(zones, connections, nb_drones)
        for zone in zones:
            for connection in connections:
                if (connection.previous_zone == zone or
                   connection.next_zone == zone):
                    zone.connections.append(connection)

    @staticmethod
    def validate_graph(zones: list[Zone],
                       connections: list[Connection],
                       nb_drones: int) -> None:
        """

        """
        if len(zones) < 1 or len(connections) < 1 or nb_drones < 1:
            raise ValueError("ERROR: Map file is incomplete.")
