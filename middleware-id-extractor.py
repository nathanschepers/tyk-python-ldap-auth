import base64
import hashlib
import time

from tyk.decorators import *
from gateway import TykGateway as tyk

import ldap

# address of the ldap server
ldap_server = "172.17.0.2"

@Hook
def LDAPAuthMiddleware(request, session, metadata, spec):
    """
    Function to handle Authentication via LDAP.

    Please review the tutorial here:

        https://tyk.io/docs/customise-tyk/plugins/rich-plugins/python/custom-auth-python-tutorial/?origin_team=T0ATUMNSJ

    This middleware expects an 'Authorization' header in the request object. The header will have the format:

        'Basic AUTH_STRING'

    Where AUTH_STRING is a base64 encoded string of the format:

        'username:password'

    For this example, the username is expected to have a distinguished name of:

        "cn=" + username + ",dc=example,dc=org"

    Note that the ldap_server variable is set to the ip address of the LDAP server.
"""

    auth_header = request.get_header('Authorization')
    if not auth_header:
        # Log the error
        error_text = "No Auth header"
        tyk.log_error(error_text)
        # Set the return_overrides object to the appropriate error
        request.object.return_overrides.response_code = 400
        request.object.return_overrides.response_error = error_text
        return request, session, metadata


    tyk.log_error(auth_header) 
	 
    field, sep, value = auth_header.partition("Basic ")

    if not value:
        # Log the error
        error_text = "Incorrect auth header (no value)"
        tyk.log_error(error_text)
        # Set the return_overrides object to the appropriate error
        request.object.return_overrides.response_code = 400
        request.object.return_overrides.response_error = error_text
        return request, session, metadata

    # note the weirdness with bytes vs. strings because we're in python3
    value_bytes = bytes(value, 'ascii')
    decoded_value = base64.standard_b64decode(value_bytes).decode()
    username, password = decoded_value.split(":")

    if not (username and password):
        # Log the error
        error_text = "Incorrect auth header (no username, password)"
        tyk.log_error(error_text)
        # Set the return_overrides object to the appropriate error
        request.object.return_overrides.response_code = 400
        request.object.return_overrides.response_error = error_text
        return request, session, metadata

    user_dn = "cn=" + username + ",dc=example,dc=org"

    try:
        # initialize ldap and authenticate user using bind
        ldap_object = ldap.initialize("ldap://" + ldap_server)
        ldap_object.bind_s(user_dn, password)
    except ldap.LDAPError as e:
        # Log the error
        error_text = "Could not authenticate against LDAP with user " + username
        tyk.log_error(error_text)
        tyk.log_error(str(e))
        # Set the return_overrides object to the appropriate error
        request.object.return_overrides.response_code = 500
        request.object.return_overrides.response_error = error_text + ". -- " + str(e)
        return request, session, metadata

    # Setting metadata['token'] indicates to Tyk that the authorization was a success. In this case we are setting it
    # to the md5sum of the user_dn and the password.
    to_hash = user_dn + ":" + password
    metadata['token'] = hashlib.md5(to_hash.encode()).hexdigest()
    tyk.log("Authorized user: " + username, "info")

    # Update expiry time for id extractor (24 hours from now)
    # Note that this needs some clarification from @matias right now.
    expiry_time = time.time() + (24 * 60 * 60)
    session.id_extractor_deadline = expiry_time

    return request, session, metadata
