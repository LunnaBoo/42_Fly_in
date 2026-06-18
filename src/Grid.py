from typing import Any
from src.GraphLogic import Zone, Connection
from collections.abc import MutableSequence


class Grid:
    """
    Custom class responsible for building the grid, based on the Graph
    data, used by Textual lib in App.py file to render the visual
    representation of the graph.
    """

    def __init__(self, map: dict[str, Any]) -> None:
        self.nb_drones: int = map.get("nb_drones", -1)
        hub = map.get("hub", {})
        connection = map.get("connection", {})
        self.hubs: list[Zone] = hub._all_zones
        self.connections: list[Connection] = connection._all_connections
        self.matrix: list[MutableSequence[
            Zone | int | Connection
            ]] | None = None
        self.height: int = 0
        self.width: int = 0
        self.y_offset: int = 0
        self.x_offset: int = 0

    @staticmethod
    def get_area(hubs: list[Zone]) -> dict[str, int]:
        """
        Calculates the necessary measures for the
        generate_grid() method to define the area of the
        grid which will represent the graph.

        Parameters
        ----------
        hubs: dict[Zone]
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
    def fill_grid(
            grid: list[MutableSequence[Zone | int]],
            height: int, width: int
            ) -> list[MutableSequence[Zone | int]]:
        """
        Get's the chosen measures for the grid
        and fills it all in with 0's.

        Parameters
        ----------
        grid: list[list[Zone | int]]
            The empty grid matrix.
        height: int
            Chosen height for the graph matrix.
        width: int
            Chosen width for the graph matrix.

        Returns
        -------
        list[list[Zone | int]]
            The updated grid matrix with all spaces
            filled with 0's.
        """

        for _ in range(height):
            row: MutableSequence = []
            for _ in range(width):
                row.append(0)
            grid.append(row)
        return grid

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
        hubs: list[Zone]
            Dictionary containing all zones from the current
            map.

        Returns
        -------
        Zone:
            If a zone is found at the given coordinates,
            returns a zone object.
        int:
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
    def fill_n_grid(
            n_grid: list[MutableSequence[Zone | Connection | int]],
            height: int, width: int
            ) -> list[MutableSequence[Zone | Connection | int]]:
        """
        Same as fill_grid method, but in a grid with double the size
        in order to also accommodate Connections.

        Parameters
        ----------
        n_grid: list[list[Zone | Connection | int]]
            The empty grid matrix.
        height: int
            Chosen height for the graph matrix.
        width: int
            Chosen width for the graph matrix.

        Returns
        -------
        list[list[Zone | Connection | int]]
            The updated grid matrix with all spaces
            filled with 0's.
        """

        new_height: int = height + (height - 1)
        new_width: int = width + (width - 1)
        for _ in range(new_height):
            row: MutableSequence = []
            for _ in range(new_width):
                row.append(0)
            n_grid.append(row)
        return n_grid

    @staticmethod
    def check_connections(
            zone: Zone, connection_list: list[Connection]
            ) -> tuple[list[Connection], list[int]]:
        """
        Defines the grid coordinate of connections in relation to other
        zones and returns the Connection object and the direction it is
        positioned in the grid.

        Parameters
        ----------
        zone: Zone
            Zone object to check in order to find neighbour connections.
        connection_list: list[Connection]:
            A list of all Connection objects present in the simulation.

        Returns
        -------
        tuple[list[Connection], list[int]]:
            A tuple containing a list of Connection objects and another list
            with integers representing the directions of each zone in the
            first list.
        """

        directions: list[tuple[int, int]] = [
                (-1, 1),  # foward above
                (0, 1),   # foward
                (1, 0),   # down
                (1, 1)    # foward down
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
            grid: list[MutableSequence[Zone | int]],
            width: int, height: int,
            connections: list[Connection]
                    ) -> list[MutableSequence[Zone | Connection | int]]:
        """
        Adds Connection objects to the grid and defines a str to
        it's 'char' attribute based on it's direction in relation
        to other zones. This attribute is later used by the front-end.

        Parameters
        ----------
        grid: list[list[Zone | int]]
            Bidimensional matrix representing the grid. Only Zone objects
            and 0's at the moment.
        width: int
            Grid width.
        height: int
            Grid height.
        connections: list[Connection]
            List of all Connection objects present in the simulation.

        Returns
        -------
        list[list[Zone | Connection | int]]
            Bidimensional matrix representing the grid. Now containing
            Zone objects, Connection objects and 0's. Double the size.
        """

        n_grid: list[MutableSequence[Zone | Connection | int]] = []
        n_grid = Grid.fill_n_grid(n_grid, height, width)
        new_width = width + (width - 1)
        new_height = height + (height - 1)
        for y in range(height):
            for x in range(width):
                zone = grid[y][x]
                ny = 2 * y
                nx = 2 * x
                if isinstance(zone, Zone):
                    n_grid[ny][nx] = zone
                    zone.grid_pos = (ny, nx)
                    # this will return a list of all connection positions
                    connection_list, directions = (
                            Grid.check_connections(
                                zone,
                                connections
                            )
                        )
                    for connection, direction in zip(connection_list,
                                                     directions):
                        if direction == 1:
                            dy, dx = -1, 1
                            connection.char = "    ╱\n  ╱\n╱"
                        elif direction == 2:
                            dy, dx = 0, 1
                            connection.char = "\n\n───────"
                        elif direction == 3:
                            dy, dx = 1, 0
                            connection.char = "    │\n    │\n    │"
                        elif direction == 4:
                            dy, dx = 1, 1
                            connection.char = " ╲\n  ╲\n    ╲\n"
                        else:
                            raise ValueError("ERROR: Wrong math used "
                                             "in GridGenerator.add_"
                                             "connections()")
                        target_ny = ny + dy
                        target_nx = nx + dx
                        if (0 <= target_ny < new_height and
                           0 <= target_nx < new_width):
                            n_grid[target_ny][target_nx] = connection
                elif isinstance(zone, int):
                    n_grid[ny][nx] = 0
        return n_grid

    def generate_grid(self) -> dict[str, Any]:
        """
        Generates the grid to be later used in the front-end. Calls
        all previous methods in order to achieve this.

        Returns
        -------
        dict[str, Any]
            A dictionary with the complete grid, containing Zone objects,
            Connection objects and 0's for empty areas, grid width and
            height and x/y offsets, in order to access by index
            specific coordinates in the grid.
        """

        measures: dict[str, int] = Grid.get_area(self.hubs)
        width: int = (measures["x_max"] - measures["x_min"]) + 1
        height: int = (measures["y_max"] - measures["y_min"]) + 1

        grid: list[MutableSequence[Zone | int]] = []
        grid = Grid.fill_grid(grid, height, width)
        y_offset, x_offset = Grid.get_offset(measures)
        for y in range(height):
            for x in range(width):
                zone = Grid.decide_zone(y, x, y_offset,
                                        x_offset, self.hubs)
                grid[y][x] = zone
        n_grid = Grid.add_connections(grid, width,
                                      height, self.connections)
        self.matrix = n_grid
        self.height = (height * 2) - 1
        self.width = (width * 2) - 1
        self.x_offset = x_offset
        self.y_offest = y_offset
        return dict(grid=n_grid, width=width * 2 - 1, height=height * 2 - 1,
                    x_offset=x_offset, y_offset=y_offset)
