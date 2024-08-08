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

from tarkash.type.constant import TarkashOption

import os

class RefConfig:
    '''
        Dummy Reference Configuration
    '''
    
    def value(self, option_name: TarkashOption):
        return os.environ.get(option_name.name, None)