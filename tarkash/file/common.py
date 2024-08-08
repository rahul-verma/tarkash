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

import os
from typing import List, Dict, Any, Optional

from tarkash.core.tobj import TarkashObject
from tarkash.type.descriptor import *

class File(TarkashObject): 
    _path = String(immutable=True)
    _try_relative_path = Boolean(immutable=True)
    _should_exist = Boolean(immutable=True)
    
    """
    
    Base Class for all File Content as well as File Writer Classes
    
    Args:
        file_path (str): Path to the file. If try_relative_path is True, it is relative to the current working directory.
        
    Keyword Arguments:
        name (bool): If True, file_path is relative to the file where the call is made. Else, it is an absolute path.
        try_relative_path (bool): If True, file_path is relative to the file where the call is made. Else, it is an absolute path.
        should_exist(bool): If True, the file should exist. Else, it does not matter.
        
    In addition to the above, you can pass the keyword arguments supported by TarkashObject e.g. name.
    """
    
    def __init__(self, path: str, *, should_exist: bool=False, try_relative_path: bool=True, **kwargs):
        """
        Initializes the FlatFileReader with the provided file path and try_relative_path flag.
        """
        super().__init__(**kwargs)
        self._path = path
        self._should_exist = should_exist
        self._try_relative_path = try_relative_path
        self._exists = False
        self._relative = False
        self._full_path = "NOT_SET"
        self.__determine_file_path()
        
    @property
    def path(self):
        """
        Path to the file.
        
        Returns:
            str: Path to the file.
        """
        return self._path
    
    @property
    def try_relative_path(self):
        """
        Flag to try out relative path.
        
        Returns:
            bool: True if relative path is tried out, else False.
        """
        return self._try_relative_path
    
    @property
    def should_exist(self):
        """
        Flag to check whether the file should exist.
        
        Returns:
            bool: True if the file should exist, else False.
        """
        return self._should_exist
    
    @property
    def has_relative_path(self):
        """
        Checks whether the file path is relative.
        
        Returns:
            bool: True if the file path is relative, else False.
        """
        return self._relative
    
    @property
    def full_path(self):
        """
        Full path of the file.
        
        Returns:
            str: Full path of the file.
        """
        return self._full_path
    
    @property
    def exists(self):
        """
        Checks whether the file exists.
        
        Returns:
            bool: True if the file exists, else False.
        """
        return os.path.exists(self._full_path)
    
    @property
    def is_file(self):
        """
        Checks whether the path is a file.
        
        Returns:
            bool: True if the path is a file, else False.
        """
        return os.path.exists(self._full_path) and os.path.isfile(self._full_path)

    def __convert_to_abs_path(self):
        """
        Populate full_path with absolute path.
            
        Note:
            If base_path is not provided, it will be considered in the following order:
            1. If defined, from PROJECT_ROOT_DIR environment variable.
            2. Current working directory.
        """
        if os.environ.get("PROJECT_ROOT_DIR"):
            base_path = os.environ.get("PROJECT_ROOT_DIR")
            self._traces.append(f"Found PROJECT_ROOT_DIR environment variable with value: {base_path}.")
        else:
            base_path = os.getcwd()
            self._traces.append(f"As PROJECT_ROOT_DIR environment variable is not defined, base path is set to current working directory: {base_path}.")
            
        self._full_path = File.get_canonical_path(os.path.join(base_path, self.path))
    
    def __check_path_exists(self, file_path):
        from .error import IncorrectFilePathError
        if not os.path.exists(self.path): 
            self._traces.append(f"File path does not exist.")
            if self.should_exist:
                raise IncorrectFilePathError(self, f"The file does not exist.")
        
    def __determine_file_path(self):
        from .error import IncorrectFilePathError
        self._traces.append(f"Checking the caller-provided file path >>{self.path}<<")
        if os.path.isabs(self.path):
            self._full_path = self.path
            self.__check_path_exists(self.path)
        else:
            self._relative = True
            self._traces.append(f"It's a relative path.")
            if not self._try_relative_path:
                if self.should_exist:
                    raise IncorrectFilePathError(self, f"Expected absolute path (relative path might be correct but not relevant).")
            else:
                self._traces.append(f"Converting to absolute path.")
                self.__convert_to_abs_path()
                self._traces.append(f"Calculated path: >>{self._full_path}<<.")
                self.__check_path_exists(self._full_path)
    
    @staticmethod
    def get_canonical_path(file_path):
        return os.path.abspath(file_path)

    @staticmethod
    def join_paths(parent_path, child_path):
        return File.get_canonical_path(os.path.join(parent_path, child_path))
    
    @property
    def meta(self) -> dict:
        """
        Properties of the object as a dictionary.
        """
        
        props = TarkashObject.merge_properties(super(), {
            "path": self.path,
            "full_path": self.full_path,
            "has_relative_path": self.has_relative_path,
            "is_file": self.is_file,
            "should_exist": self.should_exist,
            "exists": self.exists
        })
        return props