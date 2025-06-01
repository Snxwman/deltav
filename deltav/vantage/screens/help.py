from typing import override
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Label, Placeholder, Rule


class HelpScreen(ModalScreen[None]):
    BINDINGS = [('escape', 'app.pop_screen')]

    DEFAULT_CSS = """
    HelpScreen {
        align: center middle;
    }

    #help-container {
        align: center middle;
        height: auto;
        width: auto;
        max-height: 80%;
        min-height: 60%; 
        max-width: 60%;
        padding: 0 2;
        border: round $accent;
    }
    
    #help-title {
        width: 100%;
        text-align: center;
        color: greenyellow;
    }

    #help-title-rule {
        height: 1;
    }

    Placeholder {
        height: 100%;
        align: center top;
    }

    Rule {
        color: $accent
    }

    Label#help-exit-tip {
        margin: 1 0 0 0;
        color: gray;
        width: 100%;
        text-align: right;
    }
    """

    @override
    def compose(self) -> ComposeResult:
        with Container(id='help-container'):
            with Container():
                yield Label('[b]Vantage Terminal Manual[/]', id='help-title')
                yield Rule(line_style='double', id='help-title-rule')
                yield Placeholder('Help text...')

            yield Label('ESC to close', id='help-exit-tip')

