from src.GraphLogic import Zone, Connection


class Drone:
    _all_drones: list["Drone"] = []

    def __init__(self) -> None:
        self.id: str = "D" + str(len(Drone._all_drones) + 1)
        self.path: list[Zone] = []
        self.route: list[Zone] = []
        Drone._all_drones.append(self)

    def act(self, graph: dict[Zone, list[Connection]]) -> str:
        if not self.route:
            route = self.path_finder()
        movement: str = self.move()
        if not movement:
            route = self.path_finder()
        movement = self.move()
        return movement

    def move(self) -> str: ...

    def path_finder(self) -> list[Zone]: ...
