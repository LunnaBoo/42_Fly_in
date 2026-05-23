from typing import Any
from src.GraphLogic import Zone, Connection


class GridGenerator:
    def __init__(self, map: dict[str, Any]) -> None:
        self.nb_drones: int = map.get("nb_drones", -1)
        hub = map.get("hub", {})
        connection = map.get("connection", {})
        self.hubs: list[Zone] = hub._all_zones
        self.connections: list[Connection] = connection._all_connections

    @staticmethod
    def get_area(hubs: list[Zone]) -> dict[str, int]:
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
        for zone in hubs:
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
                    hubs: list[Zone]) -> Zone | int:
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

        for zone in hubs:
            zone_y, zone_x = zone.pos
            if (zone_y == (y_index - y_offset)
               and zone_x == (x_index - x_offset)):
                return zone
        return 0

    @staticmethod
    def fill_n_graph(
            n_graph: list[list[Zone | Connection | int]],
            height: int, width: int
            ) -> list[list[Zone | Connection | int]]:
        new_height: int = height + (height - 1)
        new_width: int = width + (width - 1)
        for _ in range(new_height):
            row = []
            for _ in range(new_width):
                row.append(0)
            n_graph.append(row)
        return n_graph

    @staticmethod
    def check_connections(
            zone: Zone, connection_list: list[Connection]
            ) -> tuple[list[Connection], list[int]]:
        directions: list[tuple[int, int]] = [
                (-1, 1),  # acima frente
                (0, 1),   # frente
                (1, 0),   # abaixo
                (1, 1)    # abaixo frente
                ]
        connection_directions: list[int] = []
        object_list: list[Connection] = []
        for item in connection_list:
            if item.previous_zone == zone:
                neighbour_pos = item.next_zone.pos
            elif item.next_zone == zone:
                neighbour_pos = item.previous_zone.pos
            else:
                continue
            zone_pos = zone.pos
            y = zone_pos[0]
            x = zone_pos[1]
            direction = 1
            for dy, dx in directions:
                ny = y + dy
                nx = x + dx
                if (ny, nx) == neighbour_pos:
                    item.grid_pos = neighbour_pos
                    object_list.append(item)
                    connection_directions.append(direction)
                direction += 1
        return (object_list, connection_directions)

    @staticmethod
    def add_connections(
            graph: list[list[Zone | int]],
            width: int, height: int,
            connections: list[Connection]
                    ) -> list[list[Zone | Connection | int]]:
        n_graph: list[list[Zone | Connection | int]] = []
        n_graph = GridGenerator.fill_n_graph(n_graph, height, width)
        new_width = width + (width - 1)
        new_height = height + (height - 1)
        for y in range(height):
            for x in range(width):
                zone = graph[y][x]
                ny = 2 * y
                nx = 2 * x
                if isinstance(zone, Zone):
                    n_graph[ny][nx] = zone
                    zone.grid_pos = (ny, nx)
                    # this will return a list of all connection positions
                    connection_list, directions = (
                            GridGenerator.check_connections(
                                zone,
                                connections
                            )
                        )
                    for connection, direction in zip(connection_list,
                                                     directions):
                        if direction == 1:
                            dy, dx = -1, 1
                            check: bool = False
                            try:
                                check = True
                            except Exception:
                                pass
                            if check is True:
                                continue
                            connection.char = "  ┌──\n│\n│"
                        elif direction == 2:
                            dy, dx = 0, 1
                            connection.char = "───────"
                        elif direction == 3:
                            dy, dx = 1, 0
                            connection.char = "  │\n  │\n  │"
                        elif direction == 4:
                            dy, dx = 1, 1
                            check: bool = False
                            try:
                                check = True
                            except Exception:
                                pass
                            if check is True:
                                continue
                            connection.char = " │\n│\n  └──"
                        else:
                            raise ValueError("ERROR: Wrong math used "
                                             "in GridGenerator.add_"
                                             "connections()")
                        target_ny = ny + dy
                        target_nx = nx + dx
                        if (0 <= target_ny < new_height and
                           0 <= target_nx < new_width):
                            n_graph[target_ny][target_nx] = connection
                elif isinstance(zone, int):
                    n_graph[ny][nx] = 0
        return n_graph

# diretamente a frente
# diretamente em baixo
# diretamente em cima
# em cima  a frente
# em baixo a frente

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
        n_graph = GridGenerator.add_connections(graph, width,
                                                height, self.connections)
        return dict(grid=n_graph, width=width * 2 - 1, height=height * 2 - 1,
                    x_offset=x_offset, y_offset=y_offset)
