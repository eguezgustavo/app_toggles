from functools import wraps
import typing

from ._toggle_providers import Provider
from . import _types
from . import _exceptions


class Toggles:
    def __init__(self, provider: Provider) -> None:
        self.provider = provider

    def toggle_decision(self, decision_function: _types.TOOGLE_DECISION):
        @wraps(decision_function)
        def _wraps(when_on: _types.TOGGLED_VALUE=None, when_off: _types.TOGGLED_VALUE=None):
            if str(type(when_on)) != str(type(when_off)):
                raise _exceptions.InvalidDecisionFunction((
                    "when_on and when_off parameters must be of the same type. "
                    f"when_on parameter is {str(type(when_on))} and when_off parameter is {type(when_off)}"
                ))

            if isinstance(when_on, bool) or isinstance(when_off, bool):
                raise _exceptions.InvalidDecisionFunction((
                    "when_on and when_off parameters can't be boolean. "
                    "We have added this restriction to avoid a lot of is statements in your app"
                ))

            return decision_function(self.provider.get_toggles, when_on=when_on, when_off=when_off)
        return _wraps
