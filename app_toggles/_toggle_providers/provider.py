import abc
import typing


class Provider(abc.ABC):
    @abc.abstractmethod
    def get_toggles(self, toggle_names: typing.List[str]) -> typing.Tuple[bool, ...]:
        raise NotImplementedError
