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


from __future__ import print_function
from prettytable import PrettyTable
from pprint import pprint
import gnupg
import json
import six
import getpass
import os

GNUPG_BIN = "/usr/bin/gpg"


class GnuPGClient():
    
    
    def __init__(self, homedir, GNUPG_BIN, kr, sr):
        self.GNUPG_HOME = homedir
        self.keyring = kr
        self.secring = sr
        self.ring = {}
        self.gpg = gnupg.GPG(GNUPG_BIN, self.GNUPG_HOME, False, False, self.keyring,
                self.secring, True)


    def get_secret_keys(self):
        
        sk = self.gpg.list_keys(True)

        if(len(sk) is 0):
            print("No keys found")
        else:
            return sk


    def get_key_from_ring(self, keyid):
        return self.ring.get('keyid', -1)


    def load_skey(self):
        ks = self.get_secret_keys()

        for k in range(len(ks)):
            self.ring[ks[k].get('keyid', -1)] = ks

        pprint(self.ring)

    def get_public_keys(self):

        pk = self.gpg.list_keys()

        if(len(pk) is 0):
            print("No keys found")
            return
        else:
            pprint(pk)
        return pk


    def select_key(self):
        '''
        Just for now by default I return the first key
        inside the keyring
        '''
        #if six.PY2:
        for keyid, key in six.iteritems(self.ring):
            return key[0]['fingerprint']

        #else:
        #    for keyid, key in self.ring.items():
        #        return key[0]['fingerprint']

    def encrypt(self, stream, k, fname_output):

        # Expand fname_output if it is a relative path

        if fname_output.startswith('~'):
            fname_output = os.path.expanduser(fname_output)

        enc_data = self.gpg.encrypt(stream, k)
        if enc_data.ok:
            with open(fname_output, "w") as f:
                f.write(str(enc_data))
            return "Encrypted"
        else:
            return enc_data.stderr


    def decrypt(self, fname_input, key, passph):

        s = ""
        with open(fname_input, "r") as f:
            for line in f.readlines():
                s += line
            dec_data = self.gpg.decrypt(str(s), passphrase=passph)

            if(dec_data.ok):
                return dec_data
            else:
                return - 1
