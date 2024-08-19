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

import os, sys
from tarkash.core.adv.decorator import singleton

@singleton
class _TarkashSingleton:
    
    def __init__(self):
        pass

    _INITLIASED = False

    def init(self, project_dir:str=None):
        if self._INITLIASED: return
        
        from dotenv import load_dotenv, find_dotenv
        _ = load_dotenv(find_dotenv()) # read local .env file
        
        self._INITLIASED = True
        
        if project_dir is None:
            project_dir = os.environ["PROJECT_DIR"]
        from tarkash.config.ref_config import RefConfig
        self.__ref_config = RefConfig(project_dir)
        
        # Making project importable
        sys.path.append(os.path.join(project_dir, ".."))
        
        from tarkash.track.log import _Logger
        self.__logger = _Logger(self.__ref_config)
        
    @property
    def logger(self):
        return self.__logger.logger
    
    def get_option_value(self, option_name):
        return self.__ref_config.value(option_name)
    
    def get_ref_config(self):
        return self.__ref_config
    
    def register_framework_config_defaults(self, prefix, config):
        self.__ref_config.register_framework_config_defaults(prefix, config)


class Tarkash:
    '''
        Tarkash is the facade of Tarkash framework.
        Contains static methods which wrapper an internal singleton class for easy access to top level Tarkash functions.
    '''
    _TARKASH_SINGLETON = None
    
    @classmethod
    def _TWrapper(cls):
        if cls._TARKASH_SINGLETON is None:
            raise ValueError("Tarkash has not been initialized.")
        return cls._TARKASH_SINGLETON
    
    @classmethod
    def init(cls):
        cls._TARKASH_SINGLETON = _TarkashSingleton()
        cls._TARKASH_SINGLETON.init()
        
    @classmethod
    def get_logger(cls):
        '''
            Returns framework logger.
        '''
        return cls._TWrapper().logger
    
    @classmethod
    def get_option_value(cls, enum_option):
        '''
        Get configured value for an option.
        '''
        return cls._TWrapper().get_option_value(enum_option)
    
    @classmethod
    def register_framework_config_defaults(cls, prefix, config):
        '''
        Register default values for framework configuration.
        '''
        if type(prefix) is not str or not prefix:
            raise ValueError("Prefix should be a string and not empty.")
        elif type(config) is not dict or not config:
            raise ValueError("Config should be a dictionary and not empty.")
        else:
            cls._TWrapper().register_framework_config_defaults(prefix,config)
    
    @classmethod
    def get_ref_config(cls):
        return cls._TWrapper().get_ref_config()