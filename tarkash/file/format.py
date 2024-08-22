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

import os, copy
import yaml

from .error import FileIOError
from .common import FileContent

from tarkash.type.descriptor import *
from tarkash import log_debug

from typing import Any, Callable

class FlatFile(FileContent):
    _path = DString(immutable=True)
    
    """
    Loads a flat text file. Note that the file is read in one go and the contents are stored in memory, at the time of creation of the object.
    
    Args:
        path (str): Path to the file. If try_relative_path is True, it is relative to the current working directory.
        
    Keyword Arguments:
        try_relative_path (bool): If True, file_path is relative to the file where the call is made. Else, it is an absolute path.
        
    Raises:
        IncorrectFilePathError: If the file does not exist.
        FileIOError: If there is an error reading the file.
    """
 
    def __init__(self, path, **kwargs):
        """
        Initializes the FlatFile with the provided file path and try_relative_path flag. The file must exist.
        """
        super().__init__(path, should_exist=True, **kwargs)
        self.__contents = self.__read()
        
    @property
    def content(self) -> str:
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
        
        log_debug("Attempting to read the file.", tobj=self)
        try:
            with open(self.full_path, 'r', encoding='utf-8') as file:
                contents = file.read()
            return contents
        except FileIOError as e:
            raise FileIOError(self, f"An error occurred while reading the file: {e}")
        
class YamlFile(FileContent):
    
    _path = DString(immutable=True)
    
    """
    Loads a YAML file. Note that the file is read in one go and the contents are stored in memory, at the time of creation of the object.
    
    Args:
        path (str): Path to the file. If try_relative_path is True, it is relative to the current working directory.
        
    Keyword Arguments:
        try_relative_path (bool): If True, file_path is relative to the file where the call is made. Else, it is an absolute path.
        
    Raises:
        IncorrectFilePathError: If the file does not exist.
        FileIOError: If there is an error reading the file.
    """
 
    def __init__(self, path, **kwargs):
        """
        Initializes the YamlFile with the provided file path and try_relative_path flag. The file must exist.
        """
        super().__init__(path, should_exist=True, **kwargs)
        self.__contents = self.__read()
        
    @property
    def content(self) -> dict:
        """
        Contents of the file.
        
        Returns:
            dict: Contents of the file.
        """
        return self.__contents
    
    def __read(self) -> dict:
        """
        Reads the contents of the file.
        
        Returns:
            dict: The contents of the file as a dictionary.
        
        Raises:
            FileIOError: If there is an error reading the file.
        """
        
        log_debug("Attempting to read the file.", tobj=self)
        try:
            import yaml
            with open(self.full_path, 'r') as file:
                contents = yaml.safe_load(file)
            return contents
        except FileIOError as e:
            raise FileIOError(self, f"An error occurred while reading the file: {e}")

from tarkash.data.process import StringsJoiner
string_joiner = StringsJoiner(delimiter="\n")

class IniFile(FileContent):
    
    _path = DString(immutable=True)
    _content_type = DCallable
    
    """
    Loads an INI file. Note that the file is read in one go and the contents are stored in memory, at the time of creation of the object.
    
    Args:
        path (str): Path to the file. If try_relative_path is True, it is relative to the current working directory.
        
    Keyword Arguments:
        try_relative_path (bool): If True, file_path is relative to the file where the call is made. Else, it is an absolute path.
        
    Raises:
        IncorrectFilePathError: If the file does not exist.
        FileIOError: If there is an error reading the file.
    """
 
    def __init__(self, path, content_processor:Callable= string_joiner, **kwargs):
        """
        Initializes the IniFile with the provided file path and try_relative_path flag. The file must exist.
        
        You can iterate over the sections of the file using the object.
        """
        super().__init__(path, should_exist=True, **kwargs)
        self.__content_processor = content_processor
        self.__sections = dict()
        self.__parse_file()
        
        self.__closed = False        

    def __parse_file(self):
        current_section = None
        with open(self.full_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith(';') or line.startswith('#'):
                    continue  # Skip blank lines and comments
                if line.startswith('[') and line.endswith(']'):
                    current_section = line[1:-1]
                    self.__sections[current_section] = []
                elif current_section:
                    self.__sections[current_section].append(line)

        section_data = {}
        for section in self.__sections:
            section_data[section] = self.__content_processor(self.__sections[section])
        self.__sections = section_data
      
    @property  
    def sections(self) -> tuple:
        """
        Returns section names
            
        Returns:
            tuple: Section names
        """
        return tuple(self.__sections)

    def get_section_data(self, section: str) -> Any:
        """
        Returns the data in the section.
        
        Args:
            section (str): Section name.
            
        Returns:
            dict: Data in the section
        """
        return self.__sections[section]

    def __iter__(self):
        if self.__closed:
            raise FileIOError(self, "I/O operation on closed file.")
        self.__temp_sections = [k for k in self.__sections.keys()]
        return self

    def __next__(self):
        if self.__closed:
            raise FileIOError(self, "I/O operation on closed file.")
        if self.__temp_sections:
            return self.get_section_data(self.__temp_sections.pop(0))
        else:
            self.__temp_sections = []
            raise StopIteration()
    @property
    def content(self) -> dict:
        """
        Get INI file contents as a dictionary.

        Returns:
            dict: All file contents as a dictionary.
        """
        if self.__closed:
            raise FileIOError(self, "I/O operation on closed file.")
        return copy.deepcopy(self.__sections)

    def close(self):
        """
        Closes the file.
        """
        self.__closed = True
        del self.__f

from tarkash.data.process import StringsToDictConverter
strings_to_dict = StringsToDictConverter(delimiter='=')

class IniConfigFile(IniFile):
    
    _path = DString(immutable=True)
    _content_type = Callable
    
    """
    Loads an INI config file. Note that the file is read in one go and the contents are stored in memory, at the time of creation of the object.
    
    The INI file contents are supposed to have key-value pairs as a=b, one per line.
    
    Args:
        path (str): Path to the file. If try_relative_path is True, it is relative to the current working directory.
        
    Keyword Arguments:
        try_relative_path (bool): If True, file_path is relative to the file where the call is made. Else, it is an absolute path.
        
    Raises:
        IncorrectFilePathError: If the file does not exist.
        FileIOError: If there is an error reading the file.
    """
 
    def __init__(self, path, content_processor:Callable=strings_to_dict, **kwargs):
        """
        Initializes the IniFile with the provided file path and try_relative_path flag. The file must exist.
        
        You can iterate over the sections of the file using the object.
        """
        super().__init__(path, content_processor=content_processor, **kwargs)
        
class ImageFile(FileContent):
    
    _path = DString(immutable=True)
    
    """
    Loads an image file. Note that the file is read in one go and the contents are stored in memory, at the time of creation of the object.
    
    Args:
        path (str): Path to the file. If try_relative_path is True, it is relative to the current working directory.
        
    Keyword Arguments:
        try_relative_path (bool): If True, file_path is relative to the file where the call is made. Else, it is an absolute path.
        
    Raises:
        IncorrectFilePathError: If the file does not exist.
        FileIOError: If there is an error reading the file.
    """
 
    def __init__(self, path, **kwargs):
        """
        Initializes the ImageFile with the provided file path and try_relative_path flag. The file must exist.
        """
        super().__init__(path, should_exist=True, **kwargs)
        self.__contents = self.__read()
        
    @property
    def content(self) -> str:
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
        
        log_debug("Attempting to read the file.", tobj=self)
        try:
            with open(self.full_path, 'rb') as file:
                contents = file.read()
            return contents
        except FileIOError as e:
            raise FileIOError(self, f"An error occurred while reading the file: {e}")