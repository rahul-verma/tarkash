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

from typing import List

from tarkash.core.error import TarkashError
from .common import File

def _format_file_path_msg(fobj):
    file_msg = fobj.path 
    if fobj.has_relative_path:
        file_msg = file_msg + f" (with relative path resolved to {fobj.get_canonical_path(fobj.full_path)})" 
    return file_msg
        
def _format_message(msg):
    from tarkash.str.utils import append_dot
    return append_dot(msg)

class IncorrectFilePathError(TarkashError):
    """
        Exception for incorrect file path.
        
        Arguments:
            tobj (TarkashObject): TarkashObject for which the exception is raised.
            file_path (str): File path that is problematic.
            message (str): Message to be displayed.
        """
    def __init__(self, fobj: File, message: str):     
        super().__init__(fobj, f"Incorrect file path for reading/writing: >>{_format_file_path_msg(fobj) }<<. {_format_message(message)}")


class FileIOError(TarkashError):
    """
        Exception for error in reading/writing a file.
        
        Arguments:
            tobj (File): File for which the exception is raised.
            message (str): Message to be displayed.
            
    """
    from .common import File
    def __init__(self, fobj: File, message: str):  
        emsg = _format_file_path_msg(fobj)
        super().__init__(fobj, f"Error in file operation: >>{_format_file_path_msg(fobj) }<<. {_format_message(message)}")
