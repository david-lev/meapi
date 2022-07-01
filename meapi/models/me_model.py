import inspect
import json
from abc import ABCMeta
from datetime import datetime, date
from meapi.utils.exceptions import MeException

IGNORED_KEYS = []


class _ParameterReader(ABCMeta):
    """Internal class to get class init parameters"""
    def __init__(cls, *args, **kwargs):
        parameters = inspect.signature(cls.__init__).parameters
        parameters = {key: value for key, value in parameters.items() if key not in ['self', 'args', 'kwargs']}
        try:
            cls._init_parameters = cls.__bases__[0]._init_parameters.copy()
            cls._init_parameters.update(parameters)
        except AttributeError:
            cls._init_parameters = parameters

        super().__init__(*args, **kwargs)


class MeModel(metaclass=_ParameterReader):
    def __init__(self):
        self.__init_done = True

    def __str__(self) -> str:
        return self.as_json_string()

    def __eq__(self, other) -> bool:
        return other and self.as_dict() == other.as_dict()

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        if hasattr(self, 'id'):
            return hash(self.id)
        else:
            raise TypeError('unhashable type: {} (no id attribute)'.format(type(self)))

    def __setattr__(self, key, value):
        """
        Prevent attr changes after the init in protected data classes
        """
        if getattr(self, '_MeModel__init_done', None):
            raise MeException(f"You cannot change protected attr '{key}' of '{self.__class__.__name__}'!")
        return super().__setattr__(key, value)

    def as_json_string(self, ensure_ascii=True) -> str:
        """
        Return class data in json format
        """
        return json.dumps(self.as_dict(), ensure_ascii=ensure_ascii, sort_keys=True)

    def as_dict(self) -> dict:
        """
        Return class data as dict
        """
        data = {}
        for (key, value) in self.__dict__.items():
            if str(key).startswith("_"):
                continue
            elif isinstance(getattr(self, key, None), (list, tuple, set)):
                data[key] = list()
                for subobj in getattr(self, key, None):
                    if getattr(subobj, 'as_dict', None):
                        data[key].append(subobj.as_dict())
                    else:
                        data[key].append(subobj)

            elif getattr(getattr(self, key, None), 'as_dict', None):
                data[key] = getattr(self, key).as_dict()

            elif isinstance(value, (date, datetime)):
                data[key] = str(getattr(self, key, None))

            elif getattr(self, key, None):
                data[key] = getattr(self, key, None)
        return data

    @classmethod
    def new_from_json_dict(cls, data: dict, _client=None, **kwargs):
        """
        Create new instance from json_dict
        """
        if not data or data is None:
            return None
        cls_attrs = cls._init_parameters.keys()
        if '_client' in cls_attrs:
            data['_client'] = _client
        json_data = data.copy()
        if kwargs:
            for key, val in kwargs.items():
                json_data[key] = val
        for key in json_data.copy():
            if key not in cls_attrs:
                if key not in IGNORED_KEYS and not key.startswith('_'):
                    print(f"- {cls.__name__}: The key '{key}' with the value of '{json_data[key]}' just skipped. "
                          f"Try to update meapi to the latest version (pip3 install -U meapi) "
                          f"If it's still skipping, open issue in github: <https://github.com/david-lev/meapi/issues>")
                del json_data[key]
        c = cls(**json_data)
        return c

