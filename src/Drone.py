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

    def path_finder(self, graph: dict[Zone, list[Connection]],
                    start: Zone, goal: Zone) -> (int, list[Zone]) | float:
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

        while pq:
            dist, zone, path = priority_queue.pop()
            if zone.visited:
                continue
            path.append(zone)
            zone.visited = True
            if zone == goal:
                return dist, path
            for connection in zone.connections:
                next_zone = connection.next_zone
                # could be interesting to also take previous_zone into consideration
                #in cases where backtracking could be useful
                if next_zone.visited:
                    continue
                weight: float = 1
                if next_zone.type == "restricted":
                    weight = 2
                elif next_zone.type == "priority":
                    weight = 0.5
                new_dist = dist + weight
                if new_dist < get(best[next_zone], float("inf"):
                    best[next_zone] = new_dist
                    heapq.heappush(pq, new_dist,
                                   next_zone, path)
        return float("inf)
