from typing import Any
from src.GraphLogic import Zone


class GridGenerator:
    def __init__(self, map: dict[str, Any]) -> None:
        self.nb_drones: int = map.get("nb_drones", -1)
        self.hubs: dict[str, Zone] = map.get("hubs", {})
        self.connections: dict[str, int] = map.get("connections", {})

    @staticmethod
    def get_area(hubs: dict[str, Zone]) -> dict[str, int]:
        """
        Calculates the necessary measures for the
        generate_graph() method to define the area of the
        grid which will represent the graph.

        Parameters
        ----------
        hubs: dict[str, Zone]
            Dictionary with all Zones from the current map.

        Returns
        -------
        dict[str, int]
            A dictionary with measures needed to calculate
            the area.
        """

        x_list: list = []
        y_list: list = []
        for key in hubs:
            zone = hubs[key]
            y, x = zone.pos
            x_list.append(x)
            y_list.append(y)
        x_max: int = max(x_list)
        y_max: int = max(y_list)
        x_min: int = min(x_list)
        y_min: int = min(y_list)
        return dict(x_max=x_max, y_max=y_max,
                    x_min=x_min, y_min=y_min)

    @staticmethod
    def fill_graph(
            graph: list[list[Zone | int]],
            height: int, width: int
            ) -> list[list[Zone | int]]:
        """
        Get's the chosen measures for the graphic
        and fills it all in with 0's.

        Parameters
        ----------
        graph: list[list[Zone | int]]
            The empty graph matrix.
        height: int
            Chosen height for the graph matrix.
        width: int
            Chosen width for the graph matrix.

        Returns
        -------
        list[list[Zone | int]]
            The updated graph matrix with all spaces
            filled with 0's.
        """

        for _ in range(height):
            row = []
            for _ in range(width):
                row.append(0)
            graph.append(row)
        return graph

    @staticmethod
    def get_offset(measures: dict[str, int]) -> tuple[int, int]:
        """
        Calculates the offset to be used when accessing
        coordinates in the graph matrix. Useful when there
        are negative y or x coordinates, since lists cannot
        have negative indexes.

        Parameters
        ----------
        measures: dict[str, int]
            Dictionary with all necessary measures for
            calculating the y and x offsets.

        Returns
        -------
        tuple[int, int]
            A tuple with the offset of y and the offset of
            x, respectively.
        """

        x_min = measures["x_min"]
        y_min = measures["y_min"]
        x_offset: int = 0
        y_offset: int = 0
        if x_min < 0:
            x_offset = abs(x_min)
        if y_min < 0:
            y_offset = abs(y_min)
        return (y_offset, x_offset)

    @staticmethod
    def decide_zone(y_index: int, x_index: int,
                    y_offset: int, x_offset: int,
                    hubs: dict[str, Zone]) -> Zone | int:
        """
        Checks if there is a zone in the given coordinates
        or not. If there is, returns it, else returns 0.

        Parameters
        ----------
        y_index: int
            current y index on the graph matrix.
        x_index: int
            current x index on the graph matrix.
        y_offset: int
            y offset used to access the correct coordinate
            in the graph matrix.
        x_offset: int
            x offset used to access the correct coordinate
            in the graph matrix.
        hubs: dict[str, Zone]
            Dictionary containing all zones from the current
            map.

        Returns
        -------
        Zone:
            If a zone is found at the given coordinates,
            returns a zone object.
        Int:
            If no zone is found at the given coordinates,
            returns 0.
        """

        for key in hubs:
            zone = hubs[key]
            zone_y, zone_x = zone.pos
            if (zone_y == (y_index - y_offset)
               and zone_x == (x_index - x_offset)):
                return zone
        return 0

    def generate_graph(self) -> dict[str, Any]:
        """
        Generates the graph to be later traversed by the
        drones.

        Returns
        -------
        list[list[Zone | int]]
            A bidimensional matrix of Zone and int objects.
            Zone objects in their given coordinates passed
            through self.hubs and int, zeros, where there
            are no zones.
            In a nutshell:
            0 = blank space,
            Zone object = actual zone.
        """

        measures: dict[str, int] = GridGenerator.get_area(self.hubs)
        width: int = (measures["x_max"] - measures["x_min"]) + 1
        height: int = (measures["y_max"] - measures["y_min"]) + 1

        graph: list[list[Zone | int]] = []
        graph = GridGenerator.fill_graph(graph, height, width)
        y_offset, x_offset = GridGenerator.get_offset(measures)
        for y in range(height):
            for x in range(width):
                zone = GridGenerator.decide_zone(y, x, y_offset,
                                                  x_offset, self.hubs)
                graph[y][x] = zone
        return dict(grid=graph, width=width, height=height)
