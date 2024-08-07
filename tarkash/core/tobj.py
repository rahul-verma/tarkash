# This file is a part of Arjuna
# Copyright 2015-2021 Rahul Verma

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

class TarkashObject:
    """
        Base class for all Tarkash objects in Tarkash.
        
        The purpose is to guarantee that all Tarkash objects have a some properties that can be utilised e.g. at the time of reporting exceptions etc.
    """
    def __init__(self, **kwargs):
        self.__class = self.__module__ + "." + self.__class__.__name__
        if "name" in kwargs:
            self.__purpose = kwargs['name']
        else:
            self.__purpose = "NOT_SET"
        self.__traces = []

    @property
    def purpose(self) -> str:
        """
            Name of the object.
        """
        return self.__purpose
    
    @property
    def klass(self) -> str:
        """
            Class of the object.
        """
        return self.__class
    
    @property
    def meta(self) -> dict:
        """
            Tarkash Properties of the object as a dictionary.
        """
        return {
            "purpose": self.purpose,
            "class": self.klass
        }   
        
    @property
    def traces(self) -> str:
        """
            Trace messages associated with the object.
        """
        return self.__traces
    
    def _format_properties_str(self, props_dict):
        obj_props = ""
        for k,v in props_dict.items():
            k = k.title()
            obj_props += f"{k}: {v}\n"
        return obj_props

    def __str__(self):
        obj_props = "Object Properties:\n"
        obj_props += self._format_properties_str(self.meta)
        return obj_props
    
    @staticmethod
    def merge_properties(tobj1, props_dict):
        """
            Merge meta-data of the first Tarkash object with the provided dictionary.
        """
        return {**tobj1.meta, **props_dict}