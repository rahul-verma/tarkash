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
from enum import Enum, auto

class LoggingLevel(Enum):
    TRACE = auto()
    DEBUG = auto()
    INFO = auto()
    WARN = auto()
    ERROR = auto()
    FATAL = auto()

class TarkashOption(Enum):
    '''
        Represents all built-in configuration options for Tarkash.

        Any option name which is does not correspond to TarkashOption enum constant is treated as an extended option.
    '''
    
    ROOT_DIR = auto()
    '''Root Directory of Tarkash Installed/Imported in a session'''

    EXTERNAL_IMPORTS_DIR = auto()
    '''Directory of third party libs directly included in Tarkash.'''

    LOG_NAME = auto()
    '''Name of Tarkash's log file'''

    RUN_ID = auto()
    '''An alnum string representing current test run. Default is **mrun**'''

    RUN_SESSION_NAME = auto()
    '''Current session name.'''

    RUN_HOST_OS = auto()
    '''Host Operating System type: Windows/Mac/Linux.'''

    LOG_FILE_LEVEL = auto()
    '''Minimum level for a message to be logged to log file.'''

    LOG_CONSOLE_LEVEL = auto()
    '''Minimum level for a message to be displayed on console'''

    LOG_ALLOWED_CONTEXTS = auto()
    '''Allowed context strings for logging (file as well as display). Messages without contexts always get logged.'''

    L10N_LOCALE = auto()
    '''Default Locale type to be used for Localization call. Values as per Tarkash.tpi.constant.Locale'''

    L10N_STRICT = auto()
    '''Sets Localization mode to strict. Default is False.'''

    L10N_DIR = auto()
    '''Directory containing Localization files.'''

    PROJECT_NAME = auto()
    '''Test Project Name'''

    PROJECT_DIR = auto()
    '''Test Project Root Directory'''

    CONF_PROJECT_FILE = auto()
    '''Project conf file path.'''

    CONF_PROJECT_LOCAL_FILE = auto()
    '''Local Project conf file path.'''

    REPORT_DIR = auto()
    '''Reporting directory for current test run under REPORTS_DIR. Name is generated with RUN_ID and Current Timestamp. With --static-rid CLI switch, timestamp is not appended.'''

    LOG_DIR = auto()
    '''Directory containing Tarkash.log for current test run.'''

    TOOLS_DIR = auto()
    '''Directory containing external tool binaries in Tarkash test project.'''

    DEPS_DIR = auto()
    '''Directory containing external tool binaries in Tarkash test project.'''

    TEMP_DIR = auto()
    '''Temporary directory for this session.'''

    CONF_DIR = auto()
    '''Test Project configuration directory'''

    CONF_DATA_FILE = auto()
    '''File that contains all data configurations.'''

    CONF_DATA_LOCAL_FILE = auto()
    '''Local File that contains all data configurations.'''

    CONF_ENVS_FILE = auto()
    '''File that contains all environment configurations.'''

    CONF_ENVS_LOCAL_FILE = auto()
    '''Local File that contains all environment configurations.'''

    DATA_DIR = auto()
    '''Directory containing data files in test project.'''

    DATA_SRC_DIR = auto()
    '''Directory containing data source files in test project.'''

    DATA_REF_DIR = auto()
    '''Directory containing contextual data reference files in test project.'''

    DATA_REF_CONTEXTUAL_DIR = auto()
    '''Directory containing contextual data reference files in test project.'''

    DATA_REF_INDEXED_DIR = auto()
    '''Directory containing indexed data reference files in test project.'''

    DATA_FILE_DIR = auto()
    '''Directory containing files used as file data.'''
