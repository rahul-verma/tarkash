# This file is a part of Arjuna
# Copyright 2015-2021 Rahul Verma

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

def append_dot(sentence):
    """
    Append a dot at the end of the sentence if it doesn't have one.

    Args:
    sentence (str): Input sentence.

    Returns:
    str: Updated sentence with a dot at the end, if applicable.
    """
    if sentence.strip()[-1] not in [".", "!", "?"]:
        return sentence + "."
    return sentence

if __name__ == "__main__":
    print(append_dot("Hello, World"))
    print(append_dot("Hello, World."))
    print(append_dot("Hello, World!"))
    print(append_dot("Hello, World?"))