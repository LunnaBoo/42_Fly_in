from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static, Button, Label
from textual.widget import Widget
from textual.containers import Container
from textual.screen import Screen
from textual.reactive import reactive, var
from src.Simulation import Simulation
from src.GraphLogic import Zone, Connection
from typing import Any
import sys


argv = sys.argv
simulation = Simulation()
simulation.configure(argv[1])


class ZoneWidget(Screen):
    pass


class Map(Container):

    def on_mount(self) -> None:
        self.styles.grid_size_rows = simulation.grid_height
        self.styles.grid_size_columns = simulation.grid_width
        zones_to_mount = []
        for y in range(simulation.grid_height):
            for x in range(simulation.grid_width):
                zone = simulation.grid[y - simulation.y_offset][x - simulation.x_offset]
                if isinstance(zone, Zone):
                    zones_to_mount.append(Button("", id=str(zone.id), tooltip=zone.name))
                else:
                    zones_to_mount.append(Static())
        self.mount_all(zones_to_mount)


class VisualOutput(Widget):

    def compose(self) -> ComposeResult:
        yield Map()

    def action_previous_turn(self) -> None: ...
    """Action method to show the previous simulation turn."""

    def action_next_turn(self) -> None: ...
    """Action method to show the next simulation turn"""

    def action_start_or_pause(self) -> None: ...
    """Action method to start or pause the animation"""

    def action_change_colorscheme(self) -> None: ...
    """Action method to change simulation colorscheme"""


class TextualOutput(): ...


class FlyInApp(App):
    """App class responsable for the front-end of our program."""

    CSS_PATH = "grid_layout.tcss"
    BINDINGS = [
        ("left", "previous_turn", "Shows previous turn"),
        ("right", "next_turn", "Shows next turn"),
        ("p", "start_or_pause", "Starts/pauses the animation"),
        ("c", "change_colorscheme", "Change colorscheme"),
        ("tab", "change_tab", "Change current tab")
        ]
    
    def compose(self) -> ComposeResult:
        """Creates child widgets for the app."""

        yield Header()
        yield VisualOutput()
        yield Footer()
