#! /usr/bin/python3
# -*- coding: utf-8 -*-
#######################################################################
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
#    author: fmount <fmount9@autistici.org>
#    version: 0.1alpha
#    company: --
#
########################################################################



from __future__ import print_function
from prettytable import PrettyTable
from collections import defaultdict
import optparse
from GnuPGClient import GnuPGClient
from Ring import Ring
import os
import sys
import subprocess
import json
import re
import six
from pprint import pprint
import logging


'''

# user,psw,project_id

'''

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

KEYSTONERC_HOME = "~/.keystonerc_ring/"
GNUPG_HOME = "~/.gnupg/"

EXT = ".gpg"
PREFIX = "keystonerc_"


#TODO: Make it more fast
def init_ring():
    '''
    Init the ring
    '''
    global KEYSTONERC_HOME
    if KEYSTONERC_HOME.startswith('~'):
        KEYSTONERC_HOME = os.path.expanduser(KEYSTONERC_HOME)

    for filename in os.listdir(KEYSTONERC_HOME):

        krc_plain = load_element(KEYSTONERC_HOME + "/" + filename)
        RING.append(filename, krc_plain)


def read_credentials(*args):
    '''
    TODO: Read it in a human way..
    '''
    dic = defaultdict(str)
    dic.setdefault('OS_USERNAME', args[0])
    dic.setdefault('OS_PASSWORD', args[1])
    dic.setdefault('OS_TENANT_NAME', args[2])
    dic.setdefault('OS_AUTH_URL', args[3])
    return dic


def save_credentials(dic, fname, KEYSTONERC_HOME):
    
    finger = RING.gpg.select_key()
    
    message = ""
    
    for key, value in six.iteritems(dic):
        message += key + "=" + value + "\n"
    
    print(message)
    RING.gpg.encrypt(message, finger, KEYSTONERC_HOME + "/" + PREFIX + fname + EXT)

    
def load_element(fname):
    
    fingerprint = RING.gpg.select_key()
    plain_msg = RING.gpg.decrypt(fname, fingerprint, RING.passph)
    
    return str(plain_msg)
    


def set_bash_prompt(dic):
    
    for key in dic.keys():
        os.putenv(key, dic[key])
        os.system("echo %s=%s" % (key, dic[key]))
        os.putenv("PS1",
                "\e[0;34mFASTCloud\e[m-\e[0;31m${OS_USERNAME}\e[m_\e[0;32m${OS_TENANT_NAME}\e[m $ ")
    
    subprocess.call(["bash", "-noprofile", "--norc", "-O", "checkwinsize", "-O", "extglob"])


def cli():

    parser = optparse.OptionParser('\nkeystonerc_selector \nusage %prog -u USER -p PASSPHRASE -t TENANT -e ENDPOINT')
    
    parser.add_option('-u', dest='user', type='string', help='a file that contains an image list')
    parser.add_option('-p', dest='passphrase', type='string', help='password to authenticate the specified user on keystone')
    parser.add_option('-t', dest='tenant', type='string', help='tenant name to authenticate on keystone')
    parser.add_option('-e', dest='endpoint', type='string', help='endpoint of the api service')
    parser.add_option('-k', dest='keystonerc', type='string', help='keystonerc file to cypher and load inside the keyring')
    
    parser.add_option('--debug', action='store_true', dest='debug', help='activate DEBUG MODE to print all critical statement during the algorithm execution')
    parser.add_option('--persist', action='store_true', dest='persist', help='Save keystonerc credentials to a file GPG encrypted')

    (options, args) = parser.parse_args()
    
    user = options.user
    passphrase = options.passphrase
    tenant = options.tenant
    endpoint = options.endpoint
    keystonerc = options.keystonerc
    extracted = {}

    debug = options.debug
    persist = options.persist

    if(debug is not None):
        LOG.propagate = True
    else:
        LOG.propagate = False

    if(keystonerc is not None):
        with open(keystonerc, "r") as krc:
            print(krc.readlines())
            for item in list(krc.readlines()):
                r1 = item.split("=")
                if(re.search(r'USERNAME', r1[0])):
                    LOG.debug("DETECTED USERNAME")
                    extracted['OS_USERNAME'] = r1[1]
                    user = r1[1]
                elif(re.search(r'TENANT', r1[0])):
                    LOG.debug("TENANT DETECTED")
                    extracted['OS_TENANT_NAME'] = r1[1]
                    tenant = r1[1]
                elif(re.search(r'PASS', r1[0])):
                    LOG.debug("PASS DETECTED")
                    extracted['OS_PASSWORD'] = r1[1]
                    passphrase = r1[1]
                elif(re.search(r'URL', r1[0])):
                    LOG.debug("URL DETECTED")
                    extracted['OS_AUTH_URL'] = r1[1]
                    endpoint = r1[1]
                else:
                    print("Failed to fetch data!")

    # Scenario 0 (Run command without parameters)
    elif(user is None and tenant is None and passphrase is None and endpoint is None):
        init_ring()
        extracted = RING.select_from_ring()
        print("Switch user to: " + str(extracted))
    
    elif(user is None or tenant is None or passphrase is None or endpoint is None):
        print("ERROR -1")
        LOG.debug("ERROR -1")
        return -1

    else:
        # READ FROM CLI (SIMPLE)
        extracted = read_credentials(user, passphrase, tenant, endpoint)
    

    if(persist is not None):
        print("Persist Credentials")
        
        #Encrypt credentials and add them to the GPG Ring
        save_credentials(extracted, (user + "_" + tenant), KEYSTONERC_HOME)

    # RUN THE ENHANCED BASH
    set_bash_prompt(extracted)


if __name__ == '__main__':
    RING = Ring(GNUPG_HOME)
    cli()
