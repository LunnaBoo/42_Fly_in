from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, ProgressBar
from textual.widget import Widget


class VisualOutput(Widget):

    BINDINGS = [
        ("left", "previous_turn", "Shows previous turn"),
        ("right", "next_turn", "Shows next turn"),
        ("p", "start_or_pause", "Starts/pauses the animation"),
        ("c", "change_colorscheme", "Change colorscheme")
        ]

    def compose(self) -> ComposeResult:
        yield ProgressBar()

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

    BINDINGS = [("tab", "change_tab", "Change tab")]

    def compose(self) -> ComposeResult:
        """Creates child widgets for the app."""

        yield Header()
        yield VisualOutput()
        yield Footer()



if __name__ == "__main__":
    app = FlyInApp()
    app.run()
