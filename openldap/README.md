OpenLDAP & phpldapadmin Docker Containers
=====

These scripts get & start Docker Containers for OpenLDAP (1.1.8) and phpldapadmin (0.8.0).

They will output the following information:

 - OpenLDAP IP address
 - phpldapadmin IP address
 - admin dn
 - admin password
 
The IP address should be copied into `middleware.py` before bundling.

Improvements
-----

This could benefit from using `docker-compose`.
