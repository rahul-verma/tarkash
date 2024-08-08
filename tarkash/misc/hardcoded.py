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
from ..track.stack import Stack

class HardCoded:
    '''
        It's sole purpose is to increase responsibility of test author when there is a need for **time.sleep**
    '''

    @classmethod
    def __log(cls, invoker, why, seconds):
        from Tarkash import log_warning
        log_warning("Hardcoded sleep executed for {} seconds by {}. Reason by author: {}".format(seconds, invoker, why))

    @classmethod
    def sleep(cls, why: str, seconds: float) -> None:
        '''
            Fixed/Static sleep.

            Logs a warning message mentioning the caller, reason and number of seconds.
            Arguments:
                why: Reason for using static wait instead of dynamic waits that Tarkash provides.
                seconds: Number of seconds for sleeping.
        '''
        time.sleep(seconds)
        cls.__log(_Stack.get_invoker(), why, seconds)