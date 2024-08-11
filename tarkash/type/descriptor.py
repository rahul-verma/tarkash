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

from tarkash.core.descriptor import _Descriptor

class DNumber:

    def __init__(self, *, immutable=False, minvalue=None, maxvalue=None):
        super().__init__()
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self._immutable = immutable

    def validate(self, value):
        if not isinstance(value, float) and not isinstance(value, int):
            self._raise_type_error(value, 'a number')
        if self.minvalue is not None and value < self.minvalue:
            raise ValueError(
                f'Expected {value!r} to be at least {self.minvalue!r}'
            )
        if self.maxvalue is not None and value > self.maxvalue:
            raise ValueError(
                f'Expected {value!r} to be no more than {self.maxvalue!r}'
            ) 

class DInt(_Descriptor):

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
            
class DFloat(_Descriptor):

    def __init__(self, *, immutable=False, minvalue=None, maxvalue=None):
        super().__init__()
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self._immutable = immutable

    def validate(self, value):
        if not isinstance(value, float):
            self._raise_type_error(value, 'a float')
        if self.minvalue is not None and value < self.minvalue:
            raise ValueError(
                f'Expected {value!r} to be at least {self.minvalue!r}'
            )
        if self.maxvalue is not None and value > self.maxvalue:
            raise ValueError(
                f'Expected {value!r} to be no more than {self.maxvalue!r}'
            )
            
 
    
            
class DString(_Descriptor):

    def __init__(self, *, immutable=False):
        super().__init__()
        self._immutable = immutable

    def validate(self, value):
        if not isinstance(value, str):
            self._raise_type_error(value, 'a string')
        
class DBoolean(_Descriptor):

    def __init__(self, *, immutable=False):
        super().__init__()
        self._immutable = immutable

    def validate(self, value):
        if not isinstance(value, bool):
            self._raise_type_error(value, 'a bool')
            
class DCallable(_Descriptor):

    def __init__(self, *, immutable=False):
        super().__init__()
        self._immutable = immutable

    def validate(self, value):
        if not callable(value):
            self._raise_type_error(value, 'a callable for type conversion')