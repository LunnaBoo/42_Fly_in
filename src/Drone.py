from src.GraphLogic import Zone, Connection
import heapq


class Drone:
    _all_drones: list["Drone"] = []

    def __init__(self, start_hub: Zone) -> None:
        self.id: str = "D" + str(len(Drone._all_drones) + 1)
        self.path: list[Zone | Connection] = []
        self.path.append(start_hub)
        start_hub.drones_in.append(self)
        self.route: list[Zone] | float = []
        self.finished_traversal: bool = False
        Drone._all_drones.append(self)

    def act(self, start: Zone, goal: Zone) -> str:
        if self.finished_traversal is True:
            return ""
        if not self.route:
            self.route = self.path_finder(start, goal)
        if isinstance(self.route, float):
            return ""
        return self.move(goal)

    def move(self, goal: Zone) -> str:
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
                raise ValueError("ERROR: Drones can't enter next zone neither stay in "
                                 "connection for another turn.")
            next_stop.drones_in.append(self)
            currently_at.drones_in.remove(self)
            self.path.append(next_stop)
            if next_stop == goal:
                self.finished_traversal = True
            return f"{self.id} - {next_stop.name}"
        return ""

    def get_next_stop(self, currently_at: Zone) -> Zone:
        found = False
        if isinstance(self.route, list):
            for zone in self.route:
                if found == True:
                    return zone
                if zone == currently_at:
                    found = True
        raise ValueError("ERROR: Something went wrong during path-finding")

    def check_zone(self, zone: Zone) -> tuple[bool, bool]:
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
                    goal: Zone) -> list[Zone] | float:
        """
        1. While pq
        2. Check if Zone is visited, continue if it is
        3. If not, add Zone to path and mark it
        4. If Zone is Goal, return distance and path
        5. For Connection in Zone
        6. If Connection.next_zone is visited, continue
        7. Set Connection.next_zone dist to be equal to dist + it's weight
        8. If new_dist is lesser than best[Connection.next_zone], which stores
           smallest weight to get to that zone:
            1. Declare best[Connection.next_zone] to equal new_dist
            2. heappush (new_dist, Connection.next_zone, path)

        9. If while pq exits return float("inf"), meaning goal is unreachable
        """

        priority_queue: list = [(0, start)]
        heapq.heapify(priority_queue)
        best_distance: dict = {start: 0}
        predecessor: dict = {start: None}
        visited: list = []

        while priority_queue:
            dist, zone = heapq.heappop(priority_queue)
            if zone in visited:
                continue
            else:
                visited.append(zone)
            if zone == goal:
                path = []
                current = goal
                while current:
                    path.append(current)
                    current = predecessor.get(current)
                path.reverse()
                return path
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
        return float("inf")
