Tyk - Authorization with LDAP (a tutorial)
=====

While Tyk does not support LDAP as an API authorization method out of the box,
it is possible to use LDAP to validate access to APIs through the use of
a [custom authentication plugin](https://tyk.io/docs/customise-tyk/plugins/rich-plugins/python/custom-auth-python-tutorial/).

Tyk supports custom plugins written in Python, Lua, and Javascript, and most recently
added support for custom plugins written in *any* language that supports gRPC.

In this example, we will implement a plugin in Python that supports authorization via LDAP. In addition
to supporting LDAP, we will use Tyk's [ID Extractor](https://tyk.io/docs/customise-tyk/plugins/rich-plugins/id-extractor/) feature to cache authorization data.

Configuration and Prerequisites
-----

This example was developed and tested in the following environment:

 - Tyk Gateway v.2.8.3
 - Ubuntu 19.04 (and tested on Ubuntu 18.04)
 - Python 3.7.3
 - grpcio and protopbufs modules from PyPi
 - python-ldap module from PyPi
 - OpenLDAP 1.1.8
 - phpldapadmin 0.8.0
 
NOTE: the above PyPi modules should be installed at the system level on your Tyk gateway machine(s).
 
OpenLDAP and phpldapadmin
-----

For this example, we are using the docker containers for OpenLDAP and phpldapadmin provided by 
[osixia](http://www.osixia.net/docker/images/). The `openldap` directory contains scripts for getting and starting these containers.
These scripts will output all relevant details for the installation (ip addresses, admin username & password).

See the `README.md` in the `openldap/` directory for further details.

Once the containers are running, you will want to set up a test user for authorization purposes. To do this:

 - Log in to phpldap admin using the api address and admin username/password provided by `start_ldap.sh`
 - Create a new posix group
 - Create a new user, adding them to the group and specifying a password

There is an ordered list of images in the `./pics` directory that demonstrate
this process.

Custom Middleware
-----

Two versions of the custom middleware are provided. Both perform endpoint authorization
based on the HTTP `Authentication` header. The middlewares expect the header to be formatted
as follows:

`Basic BASE64_AUTH_DATA`

Where `BASE64_AUTH_DATA` is a base64 encoded string of the form:

`user_dn:password`

`user_dn` is the LDAP 'distinguished name' of the user we will authorize. `password` is that user's password.

The middleware will perform an LDAP 'bind' call to the LDAP server specified in the `middlware.py` file, checking
that the password is correct before authorizing access to the API.

ID Extractor
-----

A second custom middleware is supplied here as well, called `middleware-id-extractor.py`.
It can be used in the case that we want to benefit from Tyk's [ID Extractor](https://tyk.io/docs/customise-tyk/plugins/rich-plugins/id-extractor/).

This version of the middleware sets a cache expiry time of 24hrs in the future for every
successfully authorized request.

If you wish to use this middleware, you will need to edit `manifest.json` to select the
correct file to bundle.

You will also need to update the API definition's `custom_middleware` section to use 
the ID Extractor, as follows:

```json
   "custom_middleware": {
     "pre": [],
     "post": [],
     "post_key_auth": [],
     "auth_check": {
       "name": "",
       "path": "",
       "require_session": false
     },
     "response": [],
     "driver": "",
     "id_extractor": {
       "extract_from": "header",
       "extract_with": "value",
       "extractor_config": {
           "header_name": "Authorization"
       }
     }
```


Using the Custom Middlewares
-----

[This tutorial](https://tyk.io/docs/customise-tyk/plugins/rich-plugins/python/custom-auth-python-tutorial/)
provides basic instructions for setting up a custom Python middleware. Note that `manifest.json` in
this directory should be used as it supplies the correct function name for the python middleware.

Once Tyk and the API are configured and the bundles are being served, the Tyk gateway
should be restarted. This will cause the bundle.zip to be loaded.

Once this is done, requests can be made to the API and will be authenticated appropriately.

See docstrings and comments in `middleware*.py` for more details.

Sample Configurations
-----

The `./tyk-config` directory provides sample `tyk.conf` and `api.conf` files. The `api.conf` is a Tyk raw API definition. 
You will need to update them to reflect your configuration.