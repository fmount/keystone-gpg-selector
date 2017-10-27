#!/usr/bin/env python

############################################################################
#
#       Licensed under the MIT License (the "License"); you may not use this file
#       except in compliance with the License.  You may obtain a copy of the License
#       in the LICENSE file or at
#
#           https://opensource.org/licenses/MIT
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#    author: fmount <fmount9@autistici.org>
#    version: 0.1
#    company: --
#
#############################################################################



from functools import wraps
from handlers import MissingParameters
import os
import sys
import json


# Config validator
def needValidConfig(function):
    @wraps(function)
    def wrapper():
        try:
            print("Here I need to validate parameters and return the error")
            function()
        except:
            print("RAISE the exception")
    return wrapper


# Looking for mandatory parameters
def check_mandatory_params(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            print("Here I need to validate parameters and return the error")
            jsonconf = args[0].get("globals")
            for key, value in jsonconf.items():
                print(key)
                if(key == "gnupghome"):
                    GNUPG_HOME = value
                if(key == "gnupgbin"):
                    GNUPG_BIN = value
                if(key == "pubring"):
                    PUBRING = value
                if(key == "secring"):
                    SECRING = value
                if(key == "keystonerchome"):
                    KEYSTONERC_HOME = value

            if(GNUPG_HOME is not None and GNUPG_BIN is not None and PUBRING is not None and
                    SECRING is not None and KEYSTONERC_HOME is not None):
                return function(*args, **kwargs)
            else:
                raise MissingParameters("Missing Parameters!")
        except:
            print("RAISE the exception")
    return wrapper
