import typing

TOGGLED_VALUE = typing.TypeVar("TOGGLED_VALUE")
TOGGLE_RETRIEVER = typing.Callable[[typing.List[str]], typing.Tuple[bool, ...]]
TOOGLE_DECISION = typing.Callable[
    [TOGGLE_RETRIEVER, TOGGLED_VALUE, TOGGLED_VALUE], TOGGLED_VALUE
]
