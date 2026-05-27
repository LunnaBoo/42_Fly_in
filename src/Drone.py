from src.GraphLogic import Zone, Connection
import heapq


class Drone:
    _all_drones: list["Drone"] = []

    def __init__(self) -> None:
        self.id: str = "D" + str(len(Drone._all_drones) + 1)
        self.path: list[Zone] = []
        self.route: list[Zone] | float = []
        Drone._all_drones.append(self)

    def act(self, start: Zone, goal: Zone) -> str:
        if not self.route:
            self.route = self.path_finder(start, goal)
        if isinstance(self.route, float):
            return ""
        return self.move(start, goal)

    def move(self, start: Zone, goal: Zone) -> str:
        if len(self.path) >= 1:
            currently_at = self.path[len(self.path) - 1]
        else:
            currently_at = start
            self.path.append(start)
            start.drones_in.append(self)
        if isinstance(currently_at, Zone):
            next_stop = get_next_stop(currently_at)
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
                    else:
                        next_zone.drones_in.append(self)
                        currently_at.drones_in.remove(self)
                        self.path.append(next_zone)
                        return f"{self.id} - {next_zone.name}"
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
            self.path.append(next_zone)
            return f"{self.id} - {next_zone.name}"

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

    def get_next_stop(self, zone: Zone) -> Any: ...

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

        priority_queue: list = [(0, start, [])]
        heapq.heapify(priority_queue)
        best: dict = {start: 0}

        while priority_queue:
            dist, zone, path = priority_queue.pop()
            if zone.visited:
                continue
            path.append(zone)
            zone.visited = True
            if zone == goal:
                return (path)
            for connection in zone.connections:
                next_zone = connection.next_zone
                # could be interesting to also take previous_zone into consideration
                # in cases where backtracking could be useful
                if next_zone.visited:
                    continue
                weight: float = 1
                if next_zone.kind == "restricted":
                    weight = 2
                elif next_zone.kind == "priority":
                    weight = 0.5
                elif next_zone.kind == "blocked":
                    weight = float("inf")
                new_dist = dist + weight
                if new_dist < best.get(next_zone, float("inf")):
                    best[next_zone] = new_dist
                    heapq.heappush(priority_queue, (new_dist,
                                   next_zone, path))
        return float("inf")
