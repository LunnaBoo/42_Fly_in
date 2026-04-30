from src.GraphLogic import Zone
from collections import deque


class Graphics:
    @staticmethod
    def render_frame(graph: list[list[Zone | int]],
                     width: int, height: int) -> None:
        zone_char: str = "\x1b[48;2;150;251;199m   \x1b[0m"
        vertical_line: str = "|"
        horizontal_line: str = "-"
        top_left_corner: str = "┌"
        top_right_corner: str = "┐"
        bottom_left_corner: str = "└"
        bottom_right_corner: str = "┘"
        result: str = ""
        d_graph: deque = deque(graph)
        for y in range(height):
            if d_graph:
                first_cell_line = deque(d_graph.popleft())
                if d_graph:
                    second_cell_line = deque(d_graph.popleft())
                    if d_graph:                                    
                        third_cell_line = deque(d_graph.popleft())
            else:
                break
            first_line = ""
            second_line = ""
            third_line = ""
            for x in range(width):
                if first_cell_line:
                    cell = first_cell_line.popleft()
                    if isinstance(cell, int):
                        first_line += "   "
                    else:
                        first_line += zone_char
                
                if second_cell_line:
                    cell = second_cell_line.popleft()
                    if isinstance(cell, int):
                        second_line += "   "
                    else:
                        second_line += zone_char
                if third_cell_line:
                    cell = third_cell_line.popleft()
                    if isinstance(cell, int):
                        third_line += "   "
                    else:
                        third_line += zone_char

            result += first_line + "\n"
            result += second_line + "\n"
            result += third_line + "\n"
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
