from typing import override

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static

vantage_logo = r"""[b]
  /\ \ \/ /
 /  \ \  /
/____\ \/
[/]"""

boot_prompt = 'Press [white b u]<Enter>[/] to boot [greenyellow b]Vantage[/] terminal _'

class WelcomeScreen(Screen[None]):
    DEFAULT_CSS = """
    WelcomeScreen {
        align: center middle;
    }

    WelcomeScreen>Static {
        width: 70;
        content-align-horizontal: center;
    }
    """

    BINDINGS = [
        ('enter', 'app.pop_screen', 'Enter Terminal')
    ]

    @override
    def compose(self) -> ComposeResult:
        yield Static(vantage_logo)
        yield Static('\n\n')
        yield Static(boot_prompt)
