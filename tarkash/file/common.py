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

import os
from tarkash.core.tobj import TarkashObject

class File(TarkashObject):
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
    
    def __init__(self, path: str, *, try_relative_path: bool = True, should_exist=False, **kwargs):
        """
        Initializes the FlatFileReader with the provided file path and try_relative_path flag.
        """
        super().__init__(**kwargs)
        self.__path = path
        self.__try_relative_path = try_relative_path
        self.__should_exist = should_exist
        self.__exists = False
        self.__relative = False
        self.__full_path = "NOT_SET"
        self.__determine_file_path()

    @property
    def path(self) -> str:
        """
        Path of the file, as provided by caller.
        
        Returns:
            str: Path of the file.
        """
        return self.__path
    
    @property
    def full_path(self) -> str:
        """
        Full Path of the file. Useful if the caller-provided path is relative.
        
        Returns:
            str: Full Path of the file.
        """
        return self.__full_path
        
    @property
    def exists(self):
        """
        Checks whether the file exists.
        
        Returns:
            bool: True if the file exists, else False.
        """
        return os.path.exists(self.__exists)
    
    @property
    def is_relative(self):
        """
        Checks whether the file path is relative.
        
        Returns:
            bool: True if the file path is relative, else False.
        """
        return self.__relative
    
    def __convert_to_abs_path(self):
        """
        Populate full_path with absolute path.
            
        Note:
            If base_path is not provided, it will be considered in the following order:
            1. If defined, from PROJECT_ROOT_DIR environment variable.
            2. Current working directory.
        """
        if not base_path:
            if os.environ.get("PROJECT_ROOT_DIR"):
                base_path = os.environ.get("PROJECT_ROOT_DIR")
            else:
                base_path = os.getcwd()
            
        return os.path.join(base_path, *rel_path_parts)
    
    def __check_path_exists(self, file_path):
        from .error import IncorrectFilePathError
        if not os.path.exists(self.__path): 
            if self.__should_exist:
                raise IncorrectFilePathError(self, f"The file does not exist.")
        
    def __determine_file_path(self):
        from .error import IncorrectFilePathError
        self.traces.append(f"Checking whether the file path is correct.")
        if os.path.isabs(self.__path):
            self.__full_path = self.__path
            self.__check_path_exists(self.__path)
            file_path = self.__path
        else:
            self.__relative = True
            self.traces.append(f"It's a relative path.")
            if not self.__try_relative_path:
                if self.__should_exist:
                    raise IncorrectFilePathError(self, f"Expected absolute path (relative path might be correct but not relevant).")
            else:
                self.traces.append(f"Converting to absolute path.")
                self.__convert_to_abs_path()
                self.__check_path_exists(file_path)
        
        return file_path
    
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
            "is_relative": self.is_relative,
            "should_exist": self.__should_exist,
            "exists": self.exists
        })
        return props