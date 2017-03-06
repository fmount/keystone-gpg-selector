#!/usr/bin/python

from GnuPGClient import GnuPGClient
from prettytable import PrettyTable
from collections import defaultdict
from ConsoleUtils import ANSIColors
import getpass
import json
import re

class Ring(object):

	def __init__(self, GNUPG_HOME):
		self.ring = {}

		self.gpg = GnuPGClient(homedir=GNUPG_HOME, kr="pubring.gpg", sr="secring.gpg")
		
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

		for k, v in self.ring.iteritems():
			# Print the menu
			print(str(count) + ") " + str(k).split(".")[0])
			
			ch[count] = str(k)

			count += 1
		
		choice = input("Select your keystonerc from the Ring\n")
		
		# MANIPULATE THE RESULTING STRING
		#print(str(self.ring[ch[choice]]))

		for item in self.ring[ch[choice]].split("\n"):
			r1 = item.split("=")
			if(re.search(r'USERNAME', r1[0])):
				extracted['OS_USERNAME'] = r1[1]
			elif(re.search(r'TENANT', r1[0])):
				extracted['OS_TENANT_NAME'] = r1[1]
			elif(re.search(r'PASS', r1[0])):
				extracted['OS_PASSWORD'] = r1[1]
			elif(re.search(r'URL', r1[0])):
				extracted['OS_AUTH_URL'] = r1[1]
			else:
				print("No Match")

		return extracted


	def show_ring_content(self):
		
		table = PrettyTable(['Username _ VPDC', 'Export Env Values'])
		
		for k, v in json.loads(json.dumps(self.ring)).items():
			table.add_row([k, v])
		
		print(table)
