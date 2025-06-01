from typing import Any, Iterable, override

from textual.app import App, SystemCommand
from textual.binding import Binding
from textual.screen import Screen

from deltav.vantage.commands import GameCmd
from deltav.vantage.screens.game import GameScreen
from deltav.vantage.screens.help import HelpScreen
from deltav.vantage.screens.welcome import WelcomeScreen


class VantageApp(App[None]):
    # CSS_PATH = './styles/'

    SCREENS = {
        'welcome': WelcomeScreen,
        'game': GameScreen
    }

    BINDINGS = [
        ('f1, ?', 'show_help')
    ]


    @override
    def get_system_commands(self, screen: Screen[Any]) -> Iterable[SystemCommand]:
        for cmd in GameCmd:
            yield SystemCommand(cmd.title, cmd.desc, self.bell)


    def on_ready(self) -> None:
        self.push_screen('game')
        self.push_screen('welcome')


    def on_mount(self) -> None:
        self.title = 'Vantage Terminal'


    def action_show_help(self) -> None:
        self.push_screen(HelpScreen())
