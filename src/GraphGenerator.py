from typing import Any
from src.Zone import Zone


class GraphGenerator:
    def __init__(self, map: dict[str, Any]) -> None:
        self.nb_drones: int = map.get("nb_drones", -1)
        self.hubs: dict[str, Zone] = map.get("hubs", {})
        self.connections: dict[str, int] = map.get("connections", {})

    @staticmethod
    def get_area(hubs: dict[str, Zone]) -> tuple[int, int]:
        # PROBABLY WON'T WORK WITH NEGATIVE X, Y VALUES
        x: int = 0
        y: int = 0
        for key in hubs:
            zone = hubs[key]
            x_value, y_value = zone.pos
            if x_value > x:
                x = x_value
            if y_value > y:
                y = y_value
        return (x, y)

    def generate_graph(self) -> list[list[Zone]]:
        """
        Generates the graph to be later traversed by the
        drones.

        Returns
        -------
        list[list[Zone]]
            A bidimensional matrix of Zone objects.
        """

        #x, y probably won't be used ever
        width, height = GraphGenerator.get_area(self.hubs)

        graph: list[list[Zone]] = []
        y = 0
        while y < height:
            row: list[Zone] = []
            x = 0


        return graph
