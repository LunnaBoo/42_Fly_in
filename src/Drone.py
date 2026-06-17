from src.GraphLogic import Zone, Connection
import heapq


class Drone:
    """Custom class to represent the drones in the program's simulation."""

    _all_drones: list["Drone"] = []

    def __init__(self, start_hub: Zone) -> None:
        self.id: str = "D" + str(len(Drone._all_drones) + 1)
        self.path: list[Zone | Connection] = []
        self.path.append(start_hub)
        start_hub.drones_in.append(self)
        self.route: list[Zone] | float = []
        self.dist = float("inf")
        self.finished_traversal: bool = False
        Drone._all_drones.append(self)

    def act(self, start: Zone, goal: Zone) -> str:
        """
        Method called during turn execution in the Simulation class.
        It tries to move the drone through different paths. If there
        are no available paths it stays put.

        Parameters
        ----------
        start: Zone
            The Zone object for the start_hub.
        goal: Zone
            The Zone object for the end_hub.

        Returns
        -------
        str:
            String output containing the movement the drone just performed
            written in a specific format:
            '[Drone ID] - [Name of the zone it moved to]'.
        """

        if self.finished_traversal is True:
            return ""
        if not self.route:
            dist, route = self.path_finder(start, goal)
            self.dist = dist
            self.route = route
        if isinstance(self.route, float):
            return "IMPOSSIBLE"
        move = self.move(goal)
        if move == "":
            alt_dist, alt_route = self.alt_path_finder(start, goal)
            if alt_dist < (self.dist * 3) / 2:
                self.dist = alt_dist
                self.route = alt_route
            else:
                return ""
        else:
            return move
        return self.move(goal)

    def move(self, goal: Zone) -> str:
        """
        Checks where the drone should move next based on a given route
        and tries to move there. If movement is not possible, it returns
        an empty string.

        Parameters
        ----------
        goal: Zone
            Zone object for the end_hub.

        Returns
        -------
        str:
            String output containing the movement the drone just performed
            written in a specific format:
            '[Drone ID] - [Name of the zone it moved to]'.
        """

        currently_at = self.path[len(self.path) - 1]
        if isinstance(currently_at, Zone):
            next_stop = self.get_next_stop(currently_at)
            connections = currently_at.connections
            for connection in connections:
                if connection.next_zone == next_stop:
                    is_restricted, is_full = self.check_zone(next_stop)
                    if is_restricted:
                        if (len(connection.drones_in) <
                           connection.max_link_capacity):
                            # enter connection
                            connection.drones_in.append(self)
                            currently_at.drones_in.remove(self)
                            self.path.append(connection)
                            return f"{self.id} - {connection.name}"
                        else:
                            return ""
                    elif is_full:
                        return ""
                    elif next_stop.kind == "blocked":
                        raise ValueError("Path-finding ERROR: Drone "
                                         "tried to enter a blocked zone.")
                    else:
                        next_stop.drones_in.append(self)
                        currently_at.drones_in.remove(self)
                        self.path.append(next_stop)
                        if next_stop == goal:
                            self.finished_traversal = True
                        return f"{self.id} - {next_stop.name}"
                else:
                    continue
        else:
            next_stop = currently_at.next_zone
            is_restricted, is_full = self.check_zone(next_stop)
            if is_full:
                raise ValueError("ERROR: Drones can't enter next "
                                 "zone neither stay in "
                                 "connection for another turn.")
            next_stop.drones_in.append(self)
            currently_at.drones_in.remove(self)
            self.path.append(next_stop)
            if next_stop == goal:
                self.finished_traversal = True
            return f"{self.id} - {next_stop.name}"
        return ""

    def get_next_stop(self, currently_at: Zone) -> Zone:
        """
        Helper method to find the destination hub, leaving
        from the current one.

        Parameters
        ----------
        currently_at: Zone
            Zone object of the hub the drone is currently in.

        Returns
        -------
        Zone:
            Zone object of the hub the drone is supposed to go next.
        """

        found = False
        if isinstance(self.route, list):
            for zone in self.route:
                if found is True:
                    return zone
                if zone == currently_at:
                    found = True
        raise ValueError("ERROR: Something went wrong during path-finding")

    def check_zone(self, zone: Zone) -> tuple[bool, bool]:
        """
        Helper method to check if a zone is full or restricted.

        Parameters
        ----------
        zone: Zone
            Zone object of the zone to be check by this method.

        Returns
        -------
        tuple[bool, bool]:
            A tuple with a bool marking if the zone is restricted or not,
            and another marking if the zone is full or not.
        """

        if zone.kind == "restricted":
            is_restricted = True
        else:
            is_restricted = False
        if len(zone.drones_in) < zone.max_drones:
            is_full = False
        else:
            is_full = True
        return (is_restricted, is_full)

    def path_finder(self,
                    start: Zone,
                    goal: Zone
                    ) -> tuple[float, list[Zone]] | tuple[float, float]:
        """
        Main path finder method responsible to find the absolute best
        route from start to goal.

        Parameters
        ----------
        start: Zone
            Zone object representing the start_hub.
        goal: Zone
            Zone object representing the end_hub.

        Returns
        -------
        tuple[float, list[Zone]]:
            A tuple with a float representing the distance between start
            and goal in relation to the chosen route and a list of Zones
            representing the route itself.
        tuple[float, float]:
            This will only be returned if there is no possible path
            between start and goal. In this case, distance and route
            will be infinite.
        """

        priority_queue: list = [(0, start)]
        heapq.heapify(priority_queue)
        best_distance: dict = {start: 0}
        predecessor: dict[Zone, Zone | None] = {start: None}
        visited: list = []

        while priority_queue:
            dist, zone = heapq.heappop(priority_queue)
            if zone in visited:
                continue
            else:
                visited.append(zone)
            if zone == goal:
                path = []
                current: Zone | None = goal
                while current:
                    path.append(current)
                    current = predecessor.get(current)
                path.reverse()
                return dist, path
            for connection in zone.connections:
                neighbor = connection.next_zone
                if neighbor == zone:
                    continue
                n_dist = dist + neighbor.weight
                if n_dist < best_distance.get(neighbor, float("inf")):
                    best_distance[neighbor] = n_dist
                    predecessor[neighbor] = zone
                    heapq.heappush(priority_queue,
                                   (n_dist, neighbor))
                else:
                    continue
        return float("inf"), float("inf")

    def alt_path_finder(self,
                        start: Zone,
                        goal: Zone
                        ) -> tuple[float, list[Zone]] | tuple[float, float]:
        """
        Alternative path finder method. It behaves just like the main one,
        except this one takes into consideration hubs that are currently
        full. It finds alternative paths.

        Parameters
        ----------
        start: Zone
            Zone object representing the start_hub.
        goal: Zone
            Zone object representing the end_hub.

        Returns
        -------
        tuple[float, list[Zone]]:
            A tuple with a float representing the distance between start
            and goal in relation to the chosen route and a list of Zones
            representing the route itself.
        tuple[float, float]:
            This will only be returned if there is no possible path
            between start and goal. In this case, distance and route
            will be infinite.
        """

        current_zone = None
        for zone in self.path:
            if self in zone.drones_in:
                current_zone = zone
        if isinstance(current_zone, Zone):
            start = current_zone

        priority_queue: list = [(0, start)]
        heapq.heapify(priority_queue)
        best_distance: dict = {start: 0}
        predecessor: dict[Zone, Zone | None] = {start: None}
        visited: list = []

        while priority_queue:
            dist, zone = heapq.heappop(priority_queue)
            if zone in visited:
                continue
            else:
                visited.append(zone)
            if zone == goal:
                path = []
                current: Zone | None = goal
                while current:
                    path.append(current)
                    current = predecessor.get(current)
                path.reverse()
                return dist, path
            for connection in zone.connections:
                neighbor = connection.next_zone
                if neighbor == zone:
                    continue
                if len(neighbor.drones_in) >= neighbor.max_drones:
                    weight = float("inf")
                else:
                    weight = neighbor.weight
                n_dist = dist + weight
                if n_dist < best_distance.get(neighbor, float("inf")):
                    best_distance[neighbor] = n_dist
                    predecessor[neighbor] = zone
                    heapq.heappush(priority_queue,
                                   (n_dist, neighbor))
                else:
                    continue
        return float("inf"), float("inf")

    @classmethod
    def reset(cls) -> None:
        """Class method for clearing the _all_drones classs attribute"""

        cls._all_drones.clear()
