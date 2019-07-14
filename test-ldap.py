#!/usr/bin/python3
# Test LDAP authentication
#
# to be able to import ldap run: 
#
# $ sudo apt-get install -y python-dev libldap2-dev libsasl2-dev libssl-dev
# $ sudo pip3 install python-ldap

import ldap

if __name__ == "__main__":
    print("foo")
    ldap_server = "172.17.0.2"

    # note that here we know the user_dn and password.
    # in the real world we may need to search the directory for this user
    user_dn = "cn=Test User,dc=example,dc=org"
    password = "test123"


    try:
        # if authentication successful, get the full user data
        print("Initializing LDAP....")
        ldap_object = ldap.initialize("ldap://" + ldap_server)

        print("binding to ldap")
        ldap_object.bind_s(user_dn, password)

    except ldap.LDAPError as e:
        print("authentication error")
        print(e)
