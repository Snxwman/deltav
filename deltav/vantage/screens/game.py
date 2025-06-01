from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.suggester import SuggestFromList
from textual.widgets import (
    Input,
    Placeholder,
    Rule,
    TabbedContent,
    TabPane,
)

from deltav.vantage.commands import GameCmd
from deltav.vantage.widgets.footer import Footer
from deltav.vantage.widgets.header import Header


class GameScreen(Screen[None]):
    BINDINGS: list[Binding] = [
        Binding(
            'escape',
            'normal_mode',
            description='NORM',
            tooltip='Enter Normal Mode',
            key_display='󱊷 ',
        ),
        Binding(
            '/',
            'command_mode',
            description='CMD',
            tooltip='Enter Command Mode and focus the command line',
        ),
        Binding(
            'd, D',
            'switch_tab("tab-dashboard")',
            description='Dash',
            tooltip='Show the dashboard tab',
            show=False,
        ),
        Binding(
            'g, G',
            'switch_tab("tab-galaxy")',
            description='Galaxy',
            tooltip='Show the galaxy map tab',
            show=False,
        ),
        Binding(
            'm,M',
            'switch_tab("tab-market")',
            description='Market',
            tooltip='Show the market tab',
            show=False,
        ),
        Binding('ctrl+tab', 'next_tab', description='Next tab', show=False),
        Binding(
            'shift+ctrl+tab', 'previous_tab', description='Previous tab', show=False
        ),
    ]

    DEFAULT_CSS = """
    Screen {
        layout: vertical;
    }

    #cli {
        dock: bottom;
        margin: 1;
    }

    .h1f {
        height: 1fr
    }

    .w1f {
        width: 1fr
    }

    .b1 {
        background: darkblue
    }

    .b0 {
        background: darkcyan
    }

    .g1 {
        background: darkgreen
    }

    .g0 {
        background: darkolivegreen
    }

    #a1 {
        margin: 1 2 0 2;
    }

    #a2 {
        margin: 0 2 0 2;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(icon='ΔV', id='header')

        with Container():
            with TabbedContent(id='tabs'):
                with TabPane('[u]D[/]ashboard', id='tab-dashboard'):
                    with Vertical():
                        with Container(id='a1'):
                            yield Placeholder('Agent 1', classes='h1f')
                            with Horizontal():
                                yield Placeholder('Ship a', classes='w1f')
                                yield Placeholder('Ship b', classes='w1f')
                        yield Rule(line_style='heavy')
                        with Container(id='a2'):
                            yield Placeholder('Agent 2', classes='h1f')
                            with Horizontal():
                                yield Placeholder('Ship a', classes='w1f')
                                yield Placeholder('Ship b', classes='w1f')

                with TabPane('[u]G[/]alaxy', id='tab-galaxy'):
                    yield Placeholder('Galaxy Map', id='g')

                with TabPane('[u]M[/]arket', id='tab-market'):
                    yield Placeholder('Market', id='m')

            yield Input(
                placeholder='Enter command...',
                suggester=SuggestFromList(
                    [cmd.title for cmd in GameCmd], case_sensitive=False
                ),
                id='cli',
            )

        yield Footer(id='footer')

    def action_normal_mode(self) -> None:
        tab = self.get_widget_by_id('tab-dashboard')
        self.set_focus(None)

    def action_command_mode(self) -> None:
        cli = self.get_widget_by_id('cli')
        self.set_focus(cli)

    def action_switch_tab(self, id: str) -> None:
        tabs = self.query_one(TabbedContent)
        tabs.active = id
