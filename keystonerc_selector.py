#! /usr/bin/python

from __future__ import print_function
from prettytable import PrettyTable
from collections import defaultdict
import optparse
from GnuPGClient import GnuPGClient
from Ring import Ring
import os
import subprocess
import json
import re
from pprint import pprint
import logging


'''

# user,psw,project_id

'''

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

KEYSTONERC_HOME = "/home/fmount/.keystonerc_ring"
GNUPG_HOME = "~/.gnupg/"

EXT = ".gpg"
PREFIX = "keystonerc_"


def init_ring():
	'''
	Three Rings for the Elven-kings under the sky,
	Seven for the Dwarf-lords in their halls of stone,
	Nine for Mortal Men doomed to die,
	One for the Dark Lord on his dark throne
	In the Land of Mordor where the Shadows lie.
	One Ring to rule them all, One Ring to find them,
	One Ring to bring them all and in the darkness bind them
	In the Land of Mordor where the Shadows lie.
	'''

	print("INIT RING")

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
	
	for key, value in dic.iteritems():
		message += key + "=" + value + "\n"
	
	
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


def printUsage():
	pass


def cli():

	parser = optparse.OptionParser('\nkeystonerc_selector \nusage %prog -u USER -p PASSPHRASE -t TENANT -e endpoint')
	
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
					print("WTF")

	# Scenario 0 (Run command without parameters)
	elif(user is None and tenant is None and passphrase is None and endpoint is None):
		init_ring()
		extracted = RING.select_from_ring()
		#print("Switch user to: " + str(extracted))
	
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
