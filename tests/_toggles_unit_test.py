import pytest

from app_toggles import Toggles, InvalidDecisionFunction


class TestTogglesDecisionMethod:
    def test__injects_the_method_to_retrieve_toggles_to_the_decision_method(self, mocker):
        provider = mocker.Mock()
        when_on = mocker.Mock()
        when_off = mocker.Mock()
        decision_function = mocker.Mock(return_value=when_on)
        toggles = Toggles(provider=provider)

        decided_value = toggles.toggle_decision(decision_function)(when_on=when_on, when_off=when_off)

        decision_function.assert_called_with(provider.get_toggles, when_on, when_off)
        assert decided_value == when_on
    
    def test__raises_an_error_when_toggle_values_are_from_different_types(self, mocker):
        provider = mocker.Mock()
        when_on = 1
        when_off = "string"
        decision_function = mocker.Mock(return_value=when_on)
        toggles = Toggles(provider=provider)

        with pytest.raises(InvalidDecisionFunction) as error:
            toggles.toggle_decision(decision_function)(when_on=when_on, when_off=when_off)

        assert str(error.value) == (
            "when_on and when_off parameters must be of the same type. "
            "when_on parameter is <class 'int'> and when_off parameter is <class 'str'>"
        )

    def test__raises_an_error_when_toggle_values_are_boolean(self, mocker):
        provider = mocker.Mock()
        when_on = True
        when_off = False
        decision_function = mocker.Mock(return_value=when_on)
        toggles = Toggles(provider=provider)

        with pytest.raises(InvalidDecisionFunction) as error:
            toggles.toggle_decision(decision_function)(when_on=when_on, when_off=when_off)

        assert str(error.value) == (
            "when_on and when_off parameters can't be boolean. "
            "We have added this restriction to avoid a lot of is statements in your app"
        )