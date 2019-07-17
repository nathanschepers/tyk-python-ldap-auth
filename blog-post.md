Custom Authentication using Python
=====

Tyk has a very full featured and extensible plugin architecture, allowing for great flexibility in deployment. It supports
Python, JavaScript, Lua, and [Native GO Plugins](https://tyk.io/blog/native-go-plugins/). 
It even supports [gRPC plugins](https://tyk.io/features/extend-tyk/with-grpc/)!

Plugins can be added to Tyk's middleware chain to allow for highly customizable request and authorization logic.

By writing custom authorization logic, we can target arbitrary identity providers, such as LDAP. While Tyk doesn't have
a dedicated LDAP auth mechanism, it's very easy to use Python to integrate against it using native Python modules.

I spent a little time this week working on a [Python plugin for LDAP auth](https://github.com/nathanschepers/tyk-python-ldap-auth). 
Please take a look at the README file for technical details.
