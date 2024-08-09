from abc import ABC, abstractmethod
from tarkash.track.log import log_trace

class Validator(ABC):

    def __set_name__(self, owner, name, immutable=False):
        self.original_name = name
        self.private_name = '_' + name
        self._immutable = immutable
        self._assigned = set()

    def __get__(self, obj, objtype=None):
        log_trace(f'__get__ called with obj={repr(obj)}, objtype={objtype}')
        return obj.__dict__[self.private_name]

    def __set__(self, obj, value):
        log_trace(f'__set__ called with obj={repr(obj)}, value={value}')
        try:
            if self._immutable and obj in self._assigned:
                raise AttributeError(f'{self.original_name} is immutable')
            self.validate(value)
        except TypeError as e:
            raise TypeError(f'{self.original_name}: {e}')
        obj.__dict__[self.private_name] = value
        self._assigned.add(obj)
        #setattr(obj, self.private_name, value)
        #self.__data[obj] = value

    @abstractmethod
    def validate(self, value):
        pass
    
    def _raise_type_error(self, value, expected):
        raise TypeError(f'{self.__class__.__name__}Validator got >>{value}<<, but expected >>{expected}<<')
    
class Int(Validator):

    def __init__(self, *, immutable=False, minvalue=None, maxvalue=None):
        super().__init__()
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self._immutable = immutable

    def validate(self, value):
        if not isinstance(value, int):
            self._raise_type_error(value, 'an int')
        if self.minvalue is not None and value < self.minvalue:
            raise ValueError(
                f'Expected {value!r} to be at least {self.minvalue!r}'
            )
        if self.maxvalue is not None and value > self.maxvalue:
            raise ValueError(
                f'Expected {value!r} to be no more than {self.maxvalue!r}'
            )
            
class String(Validator):

    def __init__(self, *, immutable=False):
        super().__init__()
        self._immutable = immutable

    def validate(self, value):
        if not isinstance(value, str):
            self._raise_type_error(value, 'a string')
        
class Boolean(Validator):

    def __init__(self, *, immutable=False):
        super().__init__()
        self._immutable = immutable

    def validate(self, value):
        if not isinstance(value, bool):
            self._raise_type_error(value, 'a bool')
            
class Callable(Validator):

    def __init__(self, *, immutable=False):
        super().__init__()
        self._immutable = immutable

    def validate(self, value):
        if not callable(value):
            self._raise_type_error(value, 'a callable for type conversion')