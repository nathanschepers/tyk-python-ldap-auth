import base64

from tyk.decorators import *
from gateway import TykGateway as tyk

import ldap

# address of the ldap server
ldap_server = "172.17.0.2"

@Hook
def LDAPAuthMiddleware(request, session, metadata, spec):
    auth_header = request.get_header('Authorization')
    
    field, sep, value = auth_header.partition("Basic ")

    if not value:
        tyk.log_error("Incorrect auth header (no value)")
        # here we use return overrides
        return request, session, metadata

    # note the weirdness with bytes vs. strings because we're in python3
    value_bytes = bytes(value, 'ascii')
    decoded_value = base64.standard_b64decode(value_bytes).decode()
    username, password = decoded_value.split(":")

    if not (username and password):
        tyk.log_error("Incorrect auth header (no username, pw)")
        # here we use return overrides
        return request, session, metadata

    user_dn = "cn=" + username + ",dc=example,dc=org"

    try:
        # initialize ldap and authenticate user using bind
        ldap_object = ldap.initialize("ldap://" + ldap_server)
        ldap_object.bind_s(user_dn, password)
    except ldap.LDAPError as e:
        tyk.log_error("Could not authenticate against LDAP " + username)
        tyk.log_error(str(e))
        # here we use return overrides
        return request, session, metadata

    tyk.log_info("Authorized user: " + username)
    # here we need to set the token
    return request, session, metadata
