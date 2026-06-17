from textual.app import App, ComposeResult, ScreenStackError
from textual.css.query import NoMatches
from textual.widgets import (Footer, Header, Static,
                             Label, TabPane, TabbedContent, Tab)
from textual.widgets._tabbed_content import ContentTabs
from textual.widget import Widget
from textual.containers import Container, Horizontal, ScrollableContainer, VerticalScroll
from textual.screen import Screen
from textual.reactive import reactive
from textual.color import Color, ColorParseError
from textual import getters, events
from src.Simulation import Simulation
from src.GraphLogic import Zone, Connection
import sys


class FlyInApp(App):
    """App class responsable for the front-end of our program."""

    CSS_PATH = "grid_layout.tcss"

    argv = sys.argv
    simulation = Simulation()
    simulation.configure(argv[1])
    turn_number = reactive(0)
    finished = reactive(0)

    def compose(self) -> ComposeResult:
        """Creates child widgets for the app."""

        yield Header(icon="boo!")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "✦ │  F l y - i n │ ✦"
        self.push_screen(WarningScreen())


class WarningScreen(Screen):
    TITLE = """
▗▖ ▗▖   ▗▄▖   ▗▄▄▖   ▗▖  ▗▖  ▗▄▄▄▖  ▗▖  ▗▖   ▗▄▄▖
▐▌ ▐▌  ▐▌ ▐▌  ▐▌ ▐▌  ▐▛▚▖▐▌    █    ▐▛▚▖▐▌  ▐▌
▐▌ ▐▌  ▐▛▀▜▌  ▐▛▀▚▖  ▐▌ ▝▜▌    █    ▐▌ ▝▜▌  ▐▌▝▜▌
▐▙█▟▌  ▐▌ ▐▌  ▐▌ ▐▌  ▐▌  ▐▌  ▗▄█▄▖  ▐▌  ▐▌  ▝▚▄▞▘
    """

    def compose(self) -> ComposeResult:
        yield Container(Static(
                        "[bold]About Connections... [/]\n"
                        "In the Visual Output tab "
                        "connections are represented by "
                        "lines, but they DO NOT represent faithfully"
                        " the actual "
                        "connections stated in the map.txt file."
                        "\nThey're only supposed "
                        "to serve as visual aid. To check the actual "
                        "connections go to "
                        "the Textual Output tab in the next screen.\n\n"
                        "[bold]Terminal sizing...[/]\nThis application runs "
                        "in your "
                        "terminal emulator, meaning you'll have to zoom in"
                        " and out "
                        "manually.\n"
                        "Resizing shortcuts may very depending on your "
                        "terminal emulator."
                        "\n\n[blink]Press any key to continue[/]",
                        id="warning-text"), Static(self.TITLE, id="title"),
                        id="warning-container")

    async def on_key(self) -> None:
        await self.skip_warning()

    async def skip_warning(self) -> None:
        try:
            self.dismiss()
        except ScreenStackError:
            pass
        self.app.call_after_refresh(lambda: self.app.push_screen(MainScreen()))

class FinishedScreen(Screen):
    TITLE = """
    ▗▄▄▄▖▗▄▄▄▖▗▖  ▗▖▗▄▄▄▖ ▗▄▄▖▗▖ ▗▖▗▄▄▄▖▗▄▄▄  
    ▐▌     █  ▐▛▚▖▐▌  █  ▐▌   ▐▌ ▐▌▐▌   ▐▌  █ 
    ▐▛▀▀▘  █  ▐▌ ▝▜▌  █   ▝▀▚▖▐▛▀▜▌▐▛▀▀▘▐▌  █ 
    ▐▌   ▗▄█▄▖▐▌  ▐▌▗▄█▄▖▗▄▄▞▘▐▌ ▐▌▐▙▄▄▖▐▙▄▄▀ 
    """

    def compose(self) -> ComposeResult:
        yield Container(Static(
                        "[bold]Simulation finished![/]\n\n"
                        "You may look at simulation statistics in "
                        "the Textual tab.\n Just press 'space' and "
                        "change tabs with 'tab'."
                        "\n\n[blink]Press SPACE to continue[/]",
                        id="finished-text"), Static(self.TITLE, id="title-3"),
                        id="finished-container")

    async def on_key(self, event: events.Key) -> None:
        if event.key != "d":
            self.skip_warning()

    def skip_warning(self) -> None:
        self.app.pop_screen()


class ColorScreen(Screen):
    TITLE = """
    ▗▖ ▗▖▗▖ ▗▖▗▄▄▖      ▗▄▄▖ ▗▄▖ ▗▖    ▗▄▖ ▗▄▄▖  ▗▄▄▖
    ▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌    ▐▌   ▐▌ ▐▌▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌   
    ▐▛▀▜▌▐▌ ▐▌▐▛▀▚▖    ▐▌   ▐▌ ▐▌▐▌   ▐▌ ▐▌▐▛▀▚▖ ▝▀▚▖
    ▐▌ ▐▌▝▚▄▞▘▐▙▄▞▘    ▝▚▄▄▖▝▚▄▞▘▐▙▄▄▖▝▚▄▞▘▐▌ ▐▌▗▄▄▞▘
    """

    def compose(self) -> ComposeResult:
        yield Container(Static(
                        "[on#87286a]This color means RESTRICTED - Drones take 2 turns"
                        " to enter these hubs.[/]\n\n"
                        "[on#fe6c90]This color means PRIORITY - Drones will prioritize "
                        "these hubs over other types.[/]\n\n"
                        "[on#260d34]This color means BLOCKED - Drones cannot enter "
                        "these hubs.[/]\n\n"
                        "[on#d03791]This color means NORMAL - Nothing special about" 
                        "these hubs.[/]\n\n"
                        "\n[blink]Press any key to continue[/]",
                        id="color-text"), Static(self.TITLE, id="title-4"),
                        id="color-container")

    async def on_key(self, event: events.Key) -> None:
        if event.key != "h":
            await self.skip_warning()

    async def skip_warning(self) -> None:
        try:
            self.dismiss()
        except ScreenStackError:
            pass
        self.app.call_after_refresh(lambda: self.app.push_screen(MainScreen()))


class MainScreen(Screen):

    BINDINGS = [
        ("tab", "change_tab", "Change tab"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(icon="boo!")
        yield Footer()
        self.tabbed_content = TabbedContent(initial="visual_tab")
        with self.tabbed_content:
            with TabPane("Visual Output", id="visual_tab"):
                yield VisualOutput()
            with TabPane("Textual Output", id="textual_tab"):
                yield TextualOutput()

    def on_mount(self) -> None:
        self.query_one(Map).focus()

    def get_tabs_widget(self):
        """Finds the internal Tabs widget (ContentTabs)."""
        main_screen = self.screen
        tabbed_content = main_screen.tabbed_content
        return tabbed_content.query_one(ContentTabs)

    def action_change_tab(self) -> None:
        current = "visual"
        if self.screen.tabbed_content.active == "textual_tab":
            self.query_one(Map).focus()
            current = "textual"
        tabs = self.query(Tab)
        for tab in tabs:
            if "visual" in tab.id:
                if current == "visual":
                    tab.styles.background = "#d03791"
            else:
                if current == "textual":
                    tab.styles.background = "#d03791"
        self.get_tabs_widget().action_next_tab()
        for tab in tabs:
            if "visual" in tab.id:
                if current == "textual":
                    tab.styles.background = "#e84a9e"
            else:
                if current == "visual":
                    tab.styles.background = "#e84a9e"
            

class ZoneBlock(Static):
    def __init__(self, zone: Zone, **kwargs) -> None:
        super().__init__(**kwargs)
        self.zone = zone

    def update_drones(self) -> None:
        if self.zone.drones_in:
            drones: str = ""
            for drone in self.zone.drones_in:
                drones += drone.id + " "
            self.update(drones)
        else:
            self.update("")

    def on_mount(self) -> None:
        self.update_drones()
        if self.zone.kind == "normal":
            self.styles.background = "#d03791"
        elif self.zone.kind == "restricted":
            self.styles.background = "#87286a"
        elif self.zone.kind == "blocked":
            self.styles.background = "#260d34"
        elif self.zone.kind == "priority":
            self.styles.background = "#fe6c90"

    def validate_color(self, zone: Zone) -> None:
        try:
            Color.parse(zone.color)
        except ColorParseError:
            exit(f"ERROR: Color '{zone.color}' selected for hub "
                 f"'{zone.name}' isn't supported.")

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


class Map(Container):
    app = getters.app(FlyInApp)
    can_focus = True

    def on_mount(self) -> None:
        grid = self.app.simulation.grid
        if grid:
            self.styles.grid_size_rows = grid.height
            self.styles.grid_size_columns = grid.width
            zones_to_mount = []
            for y in range(grid.height):
                for x in range(grid.width):
                    zone = grid.matrix[
                            y - grid.y_offset][x - grid.x_offset]
                    if isinstance(zone, Zone):
                        zones_to_mount.append(ZoneWidget(id=zone.id, zone=zone))
                    elif isinstance(zone, Connection):
                        zones_to_mount.append(Static(zone.char,
                                                     classes="connection"))
                    else:
                        zones_to_mount.append(Static())
            self.mount_all(zones_to_mount)


class ImpossibleScreen(Screen):
    TITLE = """
▗▖ ▗▖   ▗▄▖   ▗▄▄▖   ▗▖  ▗▖  ▗▄▄▄▖  ▗▖  ▗▖   ▗▄▄▖
▐▌ ▐▌  ▐▌ ▐▌  ▐▌ ▐▌  ▐▛▚▖▐▌    █    ▐▛▚▖▐▌  ▐▌
▐▌ ▐▌  ▐▛▀▜▌  ▐▛▀▚▖  ▐▌ ▝▜▌    █    ▐▌ ▝▜▌  ▐▌▝▜▌
▐▙█▟▌  ▐▌ ▐▌  ▐▌ ▐▌  ▐▌  ▐▌  ▗▄█▄▖  ▐▌  ▐▌  ▝▚▄▞▘
    """

    def compose(self) -> ComposeResult:
        yield Container(Static("[bold]Something went wrong...[/]\n\n"
                        "There is no possible route from "
                        "start_hub to end_hub.\nThe map is unsolvable.\n\n"
                        "You may quit the program with\n [blink]ctrl + q[/]",
                        id="impossible-text"), Static(self.TITLE, id="title-2"),
                        id="impossible-container")


class VisualOutput(Widget):
    BINDINGS = [
        ("a", "restart_simulation", "Restarts simulation"),
        ("d", "next_turn", "Shows next turn"),
        ("c", "change_colorscheme", "Changes zone colorscheme"),
        ("h", "show_colors", "Opens hub colors glossary")
        ]

    current_colorscheme = reactive("custom")

    def compose(self) -> ComposeResult:
        yield ScrollableContainer(Map())

    def action_restart_simulation(self) -> None:
        if self.app.turn_number < 1:
            return
        self.app.simulation.restart_simulation()
        self.app.turn_number = 0
        self.app.finished = 0
        zones = self.query(ZoneBlock)
        for zone in zones:
            zone.update_drones()
        self.refresh()

    def action_next_turn(self) -> None:
        """Action method to show the next simulation turn"""
        output = self.app.simulation.next_turn()
        if self.app.simulation.finished is True:
            if self.app.finished == 0:
                self.app.push_screen(FinishedScreen())
                self.app.finished = 1
                self.screen.query_one(TextualOutput)._on_turn_changed()
                zones = self.query(ZoneBlock)
                for zone in zones:
                    zone.update_drones()
            return
        elif output == "IMPOSSIBLE":
            try:
                with open("output.txt", "w") as file:
                    file.write("IMPOSSIBLE")
            except Exception:
                pass
            self.app.push_screen(ImpossibleScreen())
            
        zones = self.query(ZoneBlock)
        for zone in zones:
            zone.update_drones()
        self.app.turn_number += 1

    def action_change_colorscheme(self) -> None:
        if self.current_colorscheme == "default":
            self.current_colorscheme = "custom"
        else:
            self.current_colorscheme = "default"
        zones = self.query(ZoneBlock)
        for zone in zones:
            zone.change_color(self.current_colorscheme)
            zone.refresh()

    def action_show_colors(self) -> None:
        self.app.push_screen(ColorScreen())


class TextualOutput(Widget):

    def on_mount(self) -> None:
        self.watch(self.app, "turn_number", self._on_turn_changed)
        try:
            with open(self.app.argv[1], "r") as file:
                map_lines = file.readlines()
        except FileNotFoundError:
            raise ValueError("ERROR: No map file detected!")
        except PermissionError:
            map_lines = ["Map file data couldn't be shown due to "
                         "permission errors. Change file permissions "
                         "to fix this."]
        left_pane = self.query_one("#left-pane")
        right_pane = self.query_one("#right-pane")
        top_pane = self.query_one("#top-pane")
        left_pane.can_focus = False
        right_pane.can_focus = False
        top_pane.can_focus = False
        top_pane.mount(Static(f"N u m b e r   o f   T u r n s :  0", id="display-turn"))
        for line in map_lines:
            left_pane.mount(Static(line.strip(), markup=False))

    def _on_turn_changed(self) -> None:
        try:
            with open("output.txt", "r") as file:
                output_lines = file.readlines()
        except FileNotFoundError:
            output_lines = []
        except PermissionError:
            output_lines = ["output file data couldn't be shown due to "
                            "permission errors. Change file permissions "
                            "to fix this."]
        right_static = self.query_one("#right-static")
        output = ""
        for line in output_lines:
            output += line.strip() + "\n"
        try:
            display_turn = self.query_one("#display-turn")
            display_turn.update(f"N u m b e r   o f   T u r n s :  {len(output_lines)}")
        except NoMatches:
            pass
        right_static.update(output)
        self.refresh()
    
    def compose(self) -> ComposeResult:
        with Container(id="app-grid"):
            with Container(id="top-pane"):
                yield Static()
            with VerticalScroll(id="left-pane"):
                yield Label("MAP DATA - HUBS AND CONNECTIONS\n", id="textual-left-label")
                yield Static()
            with VerticalScroll(id="right-pane"):
                yield Label("TURN DATA - EACH LINE REPRESENTS A TURN\n", id="textual-right-label")
                yield Static(id="right-static")
