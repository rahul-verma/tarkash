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


from typing import Any
from abc import ABC, abstractmethod

class Processor(ABC):
    
    def __init__(self, **kwargs: Any):
        self.__dict__.update(kwargs)
        
    def __call__(self, input) -> Any:
        return self._process(input)
        
    @abstractmethod
    def _process(self, input):
        pass
        
class SequenceProcessor(Processor):
    
    def __init__(self, **kwargs: Any):
        super().__init__( **kwargs)

class StringsJoiner(SequenceProcessor):
    
    def __init__(self, delimiter:str=' '):
        super().__init__(delimiter=delimiter)
        
    def _process(self, input):
        return self.delimiter.join(input)
    
class StringsToDictConverter(SequenceProcessor):
    
    def __init__(self, delimiter:str='='):
        super().__init__(delimiter=delimiter)
        
    def _process(self, input):
        out = dict()
        for i in input:
            k, v = i.split(self.delimiter)
            out[k.strip()] = v.strip()
        return out
        