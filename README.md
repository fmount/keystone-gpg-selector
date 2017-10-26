KEYSTONERC SELECTOR
---
This is a little utility to help openstack operators to manage their keystonerc
in a more safety way. 
In particular this tool makes use of gpg to crypt/decrypt the secret credentials
containing sensitive informations.
It also allow operators to generate new keystonerc-encrypted credentials passing the
mandatory parameters needed to interact with the openstack client.


Installation
---
You can simply:

    $ git clone https://github.com/fmount/keystone-gpg-selector.git ~/clone/path

and install all the required dependencies:

    $ pip install -r requirements.txt


	{
		globals": {
			"gnupghome": "~/.gnupg",
			"gnupgbin": "/usr/bin/gpg",
			"pubring": "pubring.gpg",
			"secring": "secring.gpg",
			"keystonerchome": "~/.keystonerc_ring"
			}
	}


SOURCING A KEYSTONERC
----
	
	python keystonerc\_selector.py


REGISTER A NEW USER ON A SPECIFIC TENANT
----

	python keystonerc\_selector.py -u [user] -p [password] -t [aTenant] -e [API\_ENDPOINT] --persist


LICENSE
---
It is distruibuted according to the MIT LICENSE.
