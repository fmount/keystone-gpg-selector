KEYSTONERC SELECTOR
---
This is a little utility to help openstack operators to manage their keystonerc
in a more safe way. 
In particular this tool makes use of gpg to crypt/decrypt the secret credentials
containing sensitive informations.
It also allow operators to generate new keystonerc-encrypted credentials passing the
mandatory parameters needed to interact with the openstack client.


Installation
---
Today you can simply:

    $ git clone https://github.com/fmount/keystone-gpg-selector.git ~/clone/path

and install all the required dependencies:


    $ pip install -r requirements.txt

but it could be available soon on Pypy repos and on AUR.



SOURCING A KEYSTONERC
----
python keystonerc\_selector.py


REGISTER A NEW USER ON A SPECIFIC TENANT
----

python keystonerc\_selector.py -u [user] -p [password] -t [aTenant] -e [API\_ENDPOINT] --persist

TODO
---
Parametrize two default parameters:

1. keystonerc ring HOME: This parameter by default is ~/.keystonerc\_ring
2. Gnupg HOME: This parameter by default is ~/.gnupg

In the next release will be introduced a parser to allow user to set the parameters described above.
