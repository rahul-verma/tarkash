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

'''
This is a dummy reference configuration that is based on environment variables in the project, till this feature is developed and ported from Tarkash.
'''

import os
from enum import Enum

class RefConfig:
    '''
        Dummy Reference Configuration
    '''
    def __init__(self, project_dir: str):
        self.__config = {"PROJECT_NAME": os.path.basename(project_dir), 
                         "PROJECT_DIR": project_dir,
                         "LOG_CONSOLE_LEVEL": "INFO",
                         "LOG_FILE_LEVEL": "DEBUG",
                         "LOG_DIR": f"{project_dir}/log",
                         "REPORT_DIR": f"{project_dir}/report",
        }
    
    def value(self, option: Enum):
        if option.name in ("PROJECT_NAME", "PROJECT_DIR"):
            return self.__config[option.name]
        try:
            return os.environ[option.name]
        except:
            return self.__config[option.name]
    
    def register_framework_config_defaults(self, prefix, config):
        for k,v in config.items():
            if type(v) in (tuple,list):
                if v[1] == "project_relative_path":
                    absolute_path = f"{self.__config['PROJECT_DIR']}/{v[0]}"
                    self.__config[k] = absolute_path
                elif v[1] == "absolute_path":
                    self.__config[k] = v[0]
                else:
                    raise ValueError(f"Unrecognized config value type. {v[1]}")
            else:
                self.__config[k] = v