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
import re
from typing import List, Dict, Any, Optional

from tarkash.core.tobj import TarkashObject
from tarkash.type.descriptor import *
from tarkash import log_debug

class File(TarkashObject): 
    _path = DString(immutable=True)
    _try_relative_path = DBoolean(immutable=True)
    _should_exist = DBoolean(immutable=True)
    
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

    def __convert_to_abs_path(self, file_path):
        """
        Populate full_path with absolute path.
            
        Note:
            If base_path is not provided, it will be considered in the following order:
            1. If defined, from PROJECT_ROOT_DIR environment variable.
            2. Current working directory.
        """
        if os.environ.get("PROJECT_ROOT_DIR"):
            base_path = os.environ.get("PROJECT_ROOT_DIR")
            log_debug(f"Found PROJECT_ROOT_DIR environment variable with value: {base_path}.", tobj=self)
        else:
            base_path = os.getcwd()
            log_debug(f"As PROJECT_ROOT_DIR environment variable is not defined, base path is set to current working directory: {base_path}.", tobj=self)
            
        log_debug(f"Base path: {base_path}. Relative path: {file_path}", tobj=self)
        self._full_path = File.get_canonical_path(os.path.join(base_path, file_path))
            
    def __remove_pathsep_from_beginning(self, fpath):
        updated = re.sub(r"^[\\]+(.*)$", r"\1", fpath)
        updated = re.sub(r"^[/]+(.*)$", r"\1", updated)
        return updated
        
    def __determine_file_path(self):
        updated_path = self.path
        from .error import IncorrectFilePathError
        log_debug(f"Checking the caller-provided file path >>{self.path}<<", tobj=self)
        if os.path.isabs(self.path):
            log_debug(f"Trying it as an absolute path.", tobj=self)
            log_debug(self.path)
            if os.path.exists(self.path):
                log_debug(f"It's an absolute path.", tobj=self)
                self._relative = False
                self._exists = True
                self._full_path = self.path
                return
            else:
                # On Mac and linux the absolute path can start with /
                # The user can provide / as the beginning of a relative path. In this case os.path.abs returns True which is misleading.
                updated_path = self.__remove_pathsep_from_beginning(self.path)
                if os.path.isabs(updated_path):
                    self._full_path = updated_path
                    # This can happen on Windows. This is indeed an absolute path which does not exist
                    log_debug(f"It's an absolute path.", tobj=self)
                    if self.should_exist:
                        raise IncorrectFilePathError(self, f"The file does not exist.")
                    else:
                        return
                elif not self._try_relative_path:
                    raise IncorrectFilePathError(self, f"The absolute path is incorrect (relative path might be correct but not relevant).")
                    
        self._relative = True
        log_debug(f"It's a relative path.", tobj=self)
        log_debug(f"Converting to absolute path.", tobj=self)
        self.__convert_to_abs_path(updated_path)
        log_debug(f"Calculated path: >>{self._full_path}<<.", tobj=self)
        if not os.path.exists(self._full_path):
            if self.should_exist:
                raise IncorrectFilePathError(self, f"The file does not exist.")   
    
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