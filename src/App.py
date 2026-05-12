from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static, Button, Label, Tab, Tabs
from textual.widget import Widget
from textual.containers import Container
from textual.screen import Screen
from textual.reactive import reactive, var
from textual import getters, events
from src.Simulation import Simulation
from src.GraphLogic import Zone, Connection
from typing import Any
import sys


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

    argv = sys.argv
    simulation = Simulation()
    simulation.configure(argv[1])

    def compose(self) -> ComposeResult:
        """Creates child widgets for the app."""

        yield Header()
        yield VisualOutput()
        yield Footer()


class ZoneWidget(Container):
    """Must add tooltip popup on click"""
    def __init__(self, zone: Zone, **kwargs) -> None:
        super().__init__(**kwargs)
        self.zone = zone

    app = getters.app(FlyInApp)
    def compose(self) -> ComposeResult:
        yield Button("", id="ZoneButton")
        yield Label(self.zone.name, id="ZoneLabel")


class Map(Container):
    app = getters.app(FlyInApp)
    def on_mount(self) -> None:
        simulation = self.app.simulation
        self.styles.grid_size_rows = simulation.grid_height
        self.styles.grid_size_columns = simulation.grid_width
        zones_to_mount = []
        for y in range(simulation.grid_height):
            for x in range(simulation.grid_width):
                zone = simulation.grid[y - simulation.y_offset][x - simulation.x_offset]
                if isinstance(zone, Zone):
                    zones_to_mount.append(ZoneWidget(id=zone.id, zone=zone))
                else:
                    zones_to_mount.append(Static())
        self.mount_all(zones_to_mount)


class VisualOutput(Widget):
    def compose(self) -> ComposeResult:
        yield Tabs(
                Tab("Visual Output", id="visual_tab"),
                Tab("Textual Output", id="textual_tab")
                )
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
