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

from .error import FileIOError
from .common import File

class FlatFile(File):
    """
    Loads a flat text file. Note that the file is read in one go and the contents are stored in memory, at the time of creation of the object.
    
    Args:
        file_path (str): Path to the file. If try_relative_path is True, it is relative to the current working directory.
        
    Keyword Arguments:
        try_relative_path (bool): If True, file_path is relative to the file where the call is made. Else, it is an absolute path.
        should_exist(bool): If True, the file should exist. Else, it should not exist.
        
    Raises:
        IncorrectFilePathError: If the file does not exist.
    """
    
    def __init__(self, file_path: str, *, try_relative_path: bool = True, should_exist=True):
        """
        Initializes the FlatFileReader with the provided file path and try_relative_path flag.
        """
        super().__init__(file_path, try_relative_path=try_relative_path, should_exist=should_exist)
        self.__contents = self.__read()
        
    @property
    def contents(self) -> str:
        """
        Contents of the file.
        
        Returns:
            str: Contents of the file.
        """
        return self.__contents
    
    def __read(self) -> str:
        """
        Reads the contents of the file.
        
        Returns:
            str: The contents of the file as a string.
        
        Raises:
            FileIOError: If there is an error reading the file.
        """
        
        self.traces.append("Attempting to read the file.")
        try:
            with open(self.full_path, 'r') as file:
                contents = file.read()
            return contents
        except FileIOError as e:
            raise FileIOError(self, f"An error occurred while reading the file: {e}")
 