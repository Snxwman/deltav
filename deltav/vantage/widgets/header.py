from textual.widgets import Header as TextualHeader


class Header(TextualHeader):
    # DEFAULT_CSS = """
    # Header {
    #     height: 3;
    #     dock: top;
    # }
    # """


    def __init__(self, **kwargs) -> None:
        return super().__init__(**kwargs)

