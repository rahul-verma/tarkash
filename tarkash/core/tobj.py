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

from tarkash.type.descriptor import *
from typing import List, Dict, Any

class TarkashObject:
    _purpose: String()
    _klass: str = String()
    #_traces: List[str] = PrivateAttr(default_factory=list) 

    # class Config:
    #     arbitrary_types_allowed = True

    def __init__(self, purpose:str = "NOT_SET", **kwargs):
        self._klass = self.__module__ + "." + self.__class__.__name__
        self._purpose = purpose
        self._traces = []
        
    @property
    def purpose(self) -> str:
        """
        Class of the object.
        """
        return self._purpose
        
        
    @property
    def klass(self) -> str:
        """
        Class of the object.
        """
        return self._klass
    
    @property
    def traces(self) -> List[str]:
        """
        Trace messages associated with the object.
        """
        return tuple(self._traces)

    @property
    def meta(self) -> Dict[str, Any]:
        """
        Tarkash Properties of the object as a dictionary.
        """
        return {
            "purpose": self.purpose,
            "class": self.klass
        }

    def _format_properties_str(self, props_dict: Dict[str, Any]) -> str:
        obj_props = ""
        for k, v in props_dict.items():
            k = k.title()
            obj_props += f"{k}: {v}\n"
        return obj_props

    def __str__(self) -> str:
        obj_props = "Object Properties:\n"
        obj_props += self._format_properties_str(self.meta)
        return obj_props

    @staticmethod
    def merge_properties(tobj1: 'TarkashObject', props_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge meta-data of the first Tarkash object with the provided dictionary.
        """
        return {**tobj1.meta, **props_dict}
