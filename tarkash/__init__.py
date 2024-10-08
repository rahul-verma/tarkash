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
import sys

def __join_paths(*paths):
    return os.path.abspath(os.path.join(*paths))

__root_dir = __join_paths(os.path.dirname(os.path.realpath(__file__)), "..")
sys.path.insert(0, __root_dir)


# Normal Usage
from tarkash.core.facade import Tarkash
from tarkash.track.log import *
from tarkash.file.common import File, Directory
from tarkash.file.format import FlatFile, IniFile, IniConfigFile, ImageFile, YamlFile


# Advanced Usage
from tarkash.core.tobj import TarkashObject
from tarkash.core.adv.decorator import singleton
from tarkash.type.descriptor import *