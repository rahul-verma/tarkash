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
from .tobj import TarkashObject

# Helper Functions
def format_msg(msg):
    return msg and  "Error message: {}".format(msg) or ""

# Tarkash Base Exception Classes
class TarkashError(Exception):
    """
        Base class for all exceptions in Tarkash.
        
        Arguments:
            tobj (TarkashObject): TarkashObject for which the exception is raised.
            file_path (str): File path that is problematic.
            message (str): Message to be displayed.
            
        Keyword Arguments:
            trace_messages (List[str]): List of trace messages to be displayed. They are flattened and appended to the message.
    """
    def __init__(self, tobj: TarkashObject, message: str):            
        from tarkash.str.utils import append_dot
        traces = " ".join([append_dot(m.strip()) for m in tobj.traces if m.strip()])
        if traces:
            traces = "Additional Info: " + traces
        super().__init__(f"{tobj.class_name}::{tobj.object_name}:: {message} {traces}")


class CorruptStateError(TarkashError):
    """
        Exception for a command-query to a Tarkash object that is in a corrupt state. 
        
        This will typically happen when a user puts a try-except block around a Taraksh object initialization or functionality and later tries to give a command/query which depends on a clean state.
        
        Arguments:
            tobj (TarkashObject): TarkashObject for which the exception is raised.
            message (str): Message to be displayed.
        """
    def __init__(self, tobj: TarkashObject, message: str):
        super().__init__(tobj, f"There is a state issue. Check your exception handling. {message}")
        
class WaitableError(TarkashError):

    def __init__(self, message):
        super().__init__(message)


# Concrete General Exception Classes
class TimeoutError(WaitableError):

    def __init__(self, context, message):
        super().__init__(". Timeout in {}. Error Message: {}".format(context, message))  
