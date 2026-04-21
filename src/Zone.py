class Zone:
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

    def get_connection(self) -> "Zone": ...

#class Connection:
#    def __init__(self, previous_zone: Zone,
#                 next_zone: Zone,
#                 max_link_capacity: int = 1) -> None:
#        self.previous_zone = previous_zone
#        self.next_zone = next_zone
#        self.max_link_capacity = max_link_capacity
