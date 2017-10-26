#! /usr/bin/env python

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

from GnuPGClient import GnuPGClient
from prettytable import PrettyTable
from collections import defaultdict
from utils.ConsoleUtils import ANSIColors
from handlers import KeyError
import getpass
import json
import re
import six
import sys


class Ring(object):

    def __init__(self, GNUPG_HOME, GNUPG_BIN, PUBRING, SECRING):
        self.ring = {}

        self.gpg = GnuPGClient(GNUPG_HOME, GNUPG_BIN, PUBRING, SECRING)
        
        self.pubkeys = self.gpg.load_skey()

        ANSIColors().print_with_color("Unlock your keyring", "NORMAL", "RED")

        self.passph = getpass.getpass()


    def __getattr__(self, attr):
        return attr


    def __setattr__(self, key, value):
        self.__dict__[key] = value

    
    def __repr__(self):
        pass


    def append(self, key, value):
        self.ring[key] = value
    

    def select_from_ring(self):
        
        count = 0
        
        extracted = {}
        
        ch = {}
        
        for k, v in six.iteritems(self.ring):
            
            # Print the menu
            print(str(count) + ") " + str(k).split(".")[0])
            
            ch[count] = str(k)

            count += 1
        
        choice = input("Select your keystonerc from the Ring\n")
        
        try:
            for item in self.ring[ch[int(choice)]].split("\n"):
                r1 = item.split("=")
                if(re.search(r'USERNAME', r1[0])):
                    extracted['OS_USERNAME'] = r1[1]
                elif(re.search(r'TENANT', r1[0])):
                    extracted['OS_TENANT_NAME'] = r1[1]
                elif(re.search(r'PASS', r1[0])):
                    extracted['OS_PASSWORD'] = r1[1]
                elif(re.search(r'URL', r1[0])):
                    extracted['OS_AUTH_URL'] = r1[1]
        except Exception:
            raise KeyError("The key provided doesn't exist: verify that location is correct and it's not malformed")
            sys.exit(-1)

        return extracted


    def show_ring_content(self):

        table = PrettyTable(['Username _ VPDC', 'Export Env Values'])

        for k, v in json.loads(json.dumps(self.ring)).items():
            table.add_row([k, v])
        print(table)
