from src.Zone import Zone


class Drone:
    _all_drones: list["Drone"] = []
    def __init__(self) -> None:
        self.id: int = len(Drone._all_drones) + 1
        self.path: list[Zone] = []
        self.route: list[Zone] = []
      # self.lock = threading.lock()
        Drone._all_drones.append(self)

    def act(self) -> None:
        if not self.route:
            route = self.path_finder()
        can_move: bool = self.move()
        if can_move is False:
            route = self.path_finder()
        can_move = self.move()
        return

    def move(self) -> bool: ...
    # Needs a lock

    def path_finder(self) -> list[Zone]: ...
