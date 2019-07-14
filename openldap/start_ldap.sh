#!/bin/bash -e
docker start ldap-service
docker start phpldapadmin-service

LDAP_IP=$(docker inspect -f "{{ .NetworkSettings.IPAddress }}" ldap-service)
PHPLDAP_IP=$(docker inspect -f "{{ .NetworkSettings.IPAddress }}" phpldapadmin-service)

echo "LDAP IP: $LDAP_IP"
echo "Go to: https://$PHPLDAP_IP"
echo "Login DN: cn=admin,dc=example,dc=org"
echo "Password: admin"
