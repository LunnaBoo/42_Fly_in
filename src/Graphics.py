from src.Zone import Zone
from collections import deque


class Graphics:
    @staticmethod
    def render_frame(graph: list[list[Zone | int]],
                     width: int, height: int) -> None:
        zone_char: str = "\x1b[48;2;150;251;199m   \x1b[0m"
        connection_char: str = "○"
        vertical_line: str = "┃"
        horizontal_line: str = "━"
        result: str = ""
        d_graph: deque = deque(graph)
        for y in range(height):
            if d_graph:
                zone_line = deque(d_graph.popleft())
            else:
                break
            line = ""
            for x in range(width):
                zone = zone_line.popleft()
                if isinstance(zone, int):
                    line += "---"
                else:
                    line += zone_char
                    if zone_line:
                        line += horizontal_line
            result += line
        print(result)

    class Colorscheme:
        @staticmethod
        def get_colorscheme() -> dict[str, str]:
            start: str = ""
            end: str = ""
            restricted: str = ""
            normal: str = ""
            priority: str = ""
            blocked: str = "\x1b[48;2;216;191;216m   \x1b[0m"
            return dict(start=start, end=end, restricted=restricted,
                        normal=normal, priority=priority, blocked=blocked)
