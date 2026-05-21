from textual.app import App, ComposeResult
from textual.css.types import AlignHorizontal
from textual.widgets import Tabs, Footer, Header, Static, Button, Label, TabPane, TabbedContent
from textual.widgets._tabbed_content import ContentTabs
from textual.widget import Widget
from textual.containers import Container, ScrollableContainer, Center
from textual.screen import Screen
from textual.reactive import reactive
from textual.events import Key
from textual.color import Color, ColorParseError
from textual import getters, events
from src.Simulation import Simulation
from src.GraphLogic import Zone, Connection
import sys


class FlyInApp(App):
    """App class responsable for the front-end of our program."""

    BINDINGS = [
        ("k", "change_tab", "Change tab"),
    ]
    CSS_PATH = "grid_layout.tcss"

    argv = sys.argv
    simulation = Simulation()
    simulation.configure(argv[1])

    def compose(self) -> ComposeResult:
        """Creates child widgets for the app."""

        yield Header(icon="boo!")
        yield Footer()


    def on_mount(self) -> None:
        self.title = "✦ │  F l y - i n │ ✦"
        self.push_screen(MainScreen())
        self.push_screen(WarningScreen())
 
    def get_tabs_widget(self):
        """Finds the internal Tabs widget (ContentTabs)."""
        main_screen = self.screen
        tabbed_content = main_screen.tabbed_content
        return tabbed_content.query_one(ContentTabs)

    def action_change_tab(self) -> None:
        self.get_tabs_widget().action_next_tab()


class WarningScreen(Screen):
    TITLE = """
▗▖ ▗▖   ▗▄▖   ▗▄▄▖   ▗▖  ▗▖  ▗▄▄▄▖  ▗▖  ▗▖   ▗▄▄▖
▐▌ ▐▌  ▐▌ ▐▌  ▐▌ ▐▌  ▐▛▚▖▐▌    █    ▐▛▚▖▐▌  ▐▌   
▐▌ ▐▌  ▐▛▀▜▌  ▐▛▀▚▖  ▐▌ ▝▜▌    █    ▐▌ ▝▜▌  ▐▌▝▜▌
▐▙█▟▌  ▐▌ ▐▌  ▐▌ ▐▌  ▐▌  ▐▌  ▗▄█▄▖  ▐▌  ▐▌  ▝▚▄▞▘
    """
    def compose(self) -> ComposeResult:
        yield Container(Static("ⓘ", id="left-icon"), Static(
                        "[bold]About Connections... [/]\nIn the Visual Output tab "
                        "connections are represented by "
                        "lines, but they DO NOT represent faithfully the actual "
                        "connections stated in the map.txt file.\nThey're only supposed "
                        "to serve as visual aid. For checking the actual connections, go to "
                        "the Textual Output tab in the next screen.\n\n"
                        "[bold]Terminal sizing...[/]\nThis application runs in your "
                        "terminal emulator, meaning you'll have to zoom in and out "
                        "manually with 'ctrl' + 'shift' + '+' and 'ctrl' + '-'.\n"
                        "These shortcuts may very depending on your terminal emulator."
                        "\n\n[blink]Press any key to continue[/]",
                        id="warning-text"), Static(self.TITLE, id="title"),
                         Static("ⓘ", id="right-icon"),
                        id="warning-container")

    async def on_key(self) -> None:
        self.skip_warning()

    def skip_warning(self) -> None:
        self.app.pop_screen()


class MainScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Header(icon="boo!")
        yield Footer()
        self.tabbed_content = TabbedContent(initial="visual_tab")
        with self.tabbed_content:
            with TabPane("Visual Output", id="visual_tab"):
                yield VisualOutput()
            with TabPane("Textual Output", id="textual_tab"):
                yield TextualOutput()


class ZoneBlock(Static):
    def __init__(self, zone: Zone, **kwargs) -> None:
        super().__init__(**kwargs)
        self.zone = zone

    def on_mount(self) -> None:
        if self.zone.zone_type == "normal":
            self.styles.background = "#d03791"
        elif self.zone.zone_type == "restricted":
            self.styles.background = "white"

    def validate_color(self, zone: Zone) -> None:
        try:
            Color.parse(zone.color)
        except ColorParseError:
            exit(f"ERROR: Color '{zone.color}' selected for hub '{zone.name}' isn't supported.")

    def change_color(self, value: str) -> None:
        if self.zone.color and value == "default":
            self.validate_color(self.zone)
            self.styles.background = self.zone.color
        else:
            self.styles.background = None
            self.on_mount()


class ZoneWidget(Container):
    """Must add tooltip popup on click"""
    def __init__(self, zone: Zone, **kwargs) -> None:
        super().__init__(**kwargs)
        self.zone = zone

    app = getters.app(FlyInApp)

    def compose(self) -> ComposeResult:
        yield ZoneBlock(self.zone)
        yield Label(self.zone.name, id="ZoneLabel")


class ConnectionWidget(Static):
    def __init__(self, connection: Connection, **kwargs) -> None:
        super().__init__(**kwargs)
        self.connection = connection

    def compose(self) -> ComposeResult:
        yield Static(self.connection.char)

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
                elif isinstance(zone, Connection):
                    zones_to_mount.append(Static(zone.char, classes="connection"))
                else:
                    zones_to_mount.append(Static())
        self.mount_all(zones_to_mount)


class VisualOutput(Widget):
    BINDINGS = [
        ("a", "previous_turn", "Shows previous turn"),
        ("d", "next_turn", "Shows next turn"),
        ("p", "start_or_pause", "Starts/pauses the animation"),
        ("c", "change_colorscheme", "Changes zone colorscheme")
        ]

    current_colorscheme = reactive("custom")

    def compose(self) -> ComposeResult:
        yield ScrollableContainer(Map())

    def action_previous_turn(self) -> None: ...
    """Action method to show the previous simulation turn."""

    def action_next_turn(self) -> None: ...
    """Action method to show the next simulation turn"""

    def action_start_or_pause(self) -> None: ...
    """Action method to start or pause the animation"""

    def action_change_colorscheme(self) -> None:
        if self.current_colorscheme == "default":
            self.current_colorscheme = "custom"
        else:
            self.current_colorscheme = "default"
        zones = self.query(ZoneBlock)
        for zone in zones:
            zone.change_color(self.current_colorscheme)
            zone.refresh()


class TextualOutput(Widget): ...
