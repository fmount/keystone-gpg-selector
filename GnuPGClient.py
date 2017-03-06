#! /usr/bin/python

from __future__ import print_function
from prettytable import PrettyTable
from pprint import pprint
import gnupg
import json
import getpass

GNUPG_HOME = "~/.gnupg"
GNUPG_BIN = "/usr/bin/gpg"


class GnuPGClient():
	
	
	def __init__(self, homedir, kr, sr):
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
		for keyid, key in self.ring.iteritems():
			return key[0]['fingerprint']


	def encrypt(self, stream, k, fname_output):
		enc_data = self.gpg.encrypt(stream, k)
		if enc_data.ok:
			with open(fname_output, "w") as f:
				f.write(str(enc_data))
			return "Encrypted"
		else:
			return enc_data.stderr


	def decrypt(self, fname_input, key, passph):
		s = ""
		with open(fname_input, "rb") as f:
			for line in f.readlines():
				s += line
			dec_data = self.gpg.decrypt(str(s), passphrase=passph)
			
			if(dec_data.ok):
				return dec_data
			else:
				return -1
