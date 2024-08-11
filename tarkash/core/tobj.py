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

from __future__ import annotations

from tarkash.type.descriptor import *
from typing import List, Dict, Any
from abc import ABC

class TarkashObject(ABC):
    _object_name: DString()
    _class_name: str = DString()

    def __init__(self, object_name:str = "NOT_SET", **kwargs):
        self._class_name = self.__module__ + "." + self.__class__.__name__
        self._object_name = object_name
        self._traces = []
        
    @property
    def object_name(self) -> str:
        """
        Name of the object for logging purposes.
        """
        return self._object_name
        
    @property
    def class_name(self) -> str:
        """
        Fully qualified Class name of the object.
        """
        return self._class_name
    
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
            "object_name": self.object_name,
            "class": self.class_name
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
    def merge_properties(tobj:TarkashObject, props_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge meta-data of the first Tarkash object with the provided dictionary.
        """
        return {**tobj.meta, **props_dict}
    
    def append_trace(self, message):
        """
        Append a trace message to the object.
        
        Args:
            message (str): Message
        """
        self._traces.append(message)
