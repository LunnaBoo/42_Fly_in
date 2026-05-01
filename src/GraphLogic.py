from typing import Union


class Zone:
    _all_zones: list["Zone"] = []
    def __init__(self, name: str, zone_type: str,
                 pos: tuple[int, int],
                 is_start: bool = False,
                 is_end: bool = False,
                 max_drones: int = 1,
                 color: str | None = None) -> None:
        self.name = name
        self.zone_type = zone_type
        self.pos = pos
        self.is_start = is_start
        self.is_end = is_end
        self.max_drones = max_drones
        self.color = color
        Zone._all_zones.append(self)


class Connection:
    _all_connections: list["Connection"] = []
    def __init__(self, name: str,
                 previous_zone: Zone,
                 next_zone: Zone,
                 max_link_capacity: int = 1) -> None:
        self.name = name
        self.previous_zone = previous_zone
        self.next_zone = next_zone
        self.max_link_capacity = max_link_capacity
        Connection._all_connections.append(self)
