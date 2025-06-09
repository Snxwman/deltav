def indent(string: str, level: int, start_even: bool = False) -> str:
    level = level - 1 if start_even else level

    _string = '\n'.join(
        f'{'\t' * level}{line.replace("\r", "")}'
        for line in str(string).splitlines()
    )  # fmt: skip

    return _string.lstrip('\n\t') if start_even else _string
