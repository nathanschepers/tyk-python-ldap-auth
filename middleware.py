import base64

from tyk.decorators import *
from gateway import TykGateway as tyk

import ldap

ldap_server = "172.17.0.2"

@Hook
def LDAPAuthMiddleware(request, session, metadata, spec):
    auth_header = request.get_header('Authorization')
    
    field, sep, value = auth_header.partition("Basic ")

    if not value:
        tyk.log_error("Incorrect auth header (no value)")
        return "ERROR"

    decoded_value = base64.b64decode(value)
    username, sep, password = decoded_value.partition(":")

    if not (username and password):
        tyk.log_error("Incorrect auth header (no username, pw)")
        return "ERROR"

    user_dn = "cn=" + username + ",dc=example,dc=org"

    try:
        # initialize ldap and authenticate user using bind
        ldap_object = ldap.initialize("ldap://" + ldap_server)
        ldap_object.bind_s(user_dn, password)
    except ldap.LDAPError as e:
        tyk.log_error("Could not authenticate against LDAP" + username)
        tyk.log(e)

    tyk.log("Authorized user: " + username)
    return request, session, metadata


    # if authorized == '12345':
    #     tyk.log("I'm logged!", "info")
    #     tyk.log("Request body" + request.object.body, "info")
    #     tyk.log("API config_data" + spec['config_data'], "info")
    #     session.rate = 1000.0
    #     session.per = 1.0
    #     metadata["token"] = "12345"

