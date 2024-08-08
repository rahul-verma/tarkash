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

import time
import inspect
import os

class Stack:

    @classmethod
    def get_invoker(cls):
        frame = inspect.stack()[2]
        mod = inspect.getmodule(frame[0])
        mod_file = frame.filename
        mod_name = os.path.basename(mod_file).split(".")[0]
            
        mod_script = ""
        if mod is not None and mod.__name__ == "__main__":
            mod_script = "Script:<{}> at ".format(mod.__file__)
        else:
            mod_script = "Module:<{}> File:<{}>".format(mod_name, mod_file)
        func = frame[3]
        if func == "<module>":
            func = ""
        else:
            func = "Function/Method: <{}> in ".format(func)
        line = frame[2]
        return "{}{}Line: {}".format(func, mod_script, line)
