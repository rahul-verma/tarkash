# This file is a part of Tarkash
# Copyright 2015-2024 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from abc import ABC, abstractmethod
from tarkash.track.log import log_trace

class _Descriptor(ABC):

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
        raise TypeError(f'{self.__class__.__name__}Descriptor got >>{value}<< of type >>{type(value)}<<, but expected >>{expected}<<')
  
  
class DTarkashObject(_Descriptor):

    def __init__(self, *, immutable=False):
        super().__init__()
        self._immutable = immutable

    def validate(self, value):
        from .tobj import TarkashObject
        if not isinstance(value, TarkashObject):
            self._raise_type_error(value, 'a TarkashObject')