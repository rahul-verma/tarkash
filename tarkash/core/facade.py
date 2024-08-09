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


from tarkash.core.adv.decorator import singleton

@singleton
class _TarkashSingleton:
    
    def __init__(self):
        from tarkash.config.dummy_ref_config import RefConfig
        self.__ref_config = RefConfig()

    _INITLIASED = False

    def init(self):
        if self._INITLIASED: return
        
        from dotenv import load_dotenv, find_dotenv
        _ = load_dotenv(find_dotenv()) # read local .env file
        
        self._INITLIASED = True
        from tarkash.track.log import _Logger
        self.__logger = _Logger(self.__ref_config)
        
    @property
    def logger(self):
        return self.__logger.logger
    
    def get_option_value(self, option_name):
        return self.__ref_config.value(option_name)


class Tarkash:
    '''
        Tarkash is the facade of Tarkash framework.
        Contains static methods which wrapper an internal singleton class for easy access to top level Tarkash functions.
    '''
    _TARKASH_SINGLETON = None
    
    @classmethod
    def init(cls):
        cls._TARKASH_SINGLETON = _TarkashSingleton()
        cls._TARKASH_SINGLETON.init()
        
    @classmethod
    def get_logger(cls):
        '''
            Returns framework logger.
        '''
        return cls._TARKASH_SINGLETON.logger
    
    @classmethod
    def get_option_value(cls, enum_option):
        '''
        Get configured value for an option.
        '''
        return cls._TARKASH_SINGLETON.get_option_value(enum_option)
