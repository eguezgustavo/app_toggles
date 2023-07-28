import json
import pytest
import os
import typing

from app_toggles import JsonToggleProvider, Provider, ToggleNotFoundError

_TOGGLES_FILE = "/tmp/app_toggles_test.json"


@pytest.fixture(autouse=True)
def _clear_toggles_file():
    yield
    if os.path.exists(_TOGGLES_FILE):
        os.remove(_TOGGLES_FILE)


@pytest.fixture(name="add_toggles")
def _add_toggles():
    def _add(toggles: typing.Dict[str, bool]) -> None:
        with open(_TOGGLES_FILE, "w") as toggles_file:
            json.dump(toggles, toggles_file)
    return _add


class TestGetTogglesMethod:
    def test__returns_the_toggles_specified_in_the_file(self, add_toggles: typing.Callable[[typing.Dict[str, bool]], None]):
        toggles = {"some_toggle": True, "another_toggle": False}
        add_toggles(toggles)

        toggle_provider: Provider = JsonToggleProvider(_TOGGLES_FILE)
        some_toggle, another_toggle = toggle_provider.get_toggles(["some_toggle", "another_toggle"])

        assert some_toggle == toggles["some_toggle"]
        assert another_toggle == toggles["another_toggle"]

    def test__raises_an_error__if_one_of_the_toggles_does_not_exist(self, add_toggles: typing.Callable[[typing.Dict[str, bool]], None]):
        toggles = {"some_toggle": True}
        add_toggles(toggles)
        toggle_provider: Provider = JsonToggleProvider(_TOGGLES_FILE)

        with pytest.raises(ToggleNotFoundError) as error:
            toggle_provider.get_toggles(["some_toggle", "another_toggle"])

        assert str(error.value) == 'The follwing toggles where not found: another_toggle'
