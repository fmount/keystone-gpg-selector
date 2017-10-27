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


from __future__ import print_function
from prettytable import PrettyTable


# define Python user-defined exceptions
class Error(Exception):
    
    def __init__(self, *argv, **kwargs):
        super.__init__(self, *argv, **kwargs)
    '''
    Base class for other exceptions
    '''
    pass


class KeyError(Exception):

    #def __init__(self, *argv, **kwargs):
    #    super.__init__(self, *argv, **kwargs)
    '''
    Raised when the ring key is wrong
    '''
    pass


class MissingParameters(Exception):
    '''
    Raised when there are missing params in
    the config provided and it cannot be
    validated
    '''
    pass
