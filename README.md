#  Xee SDK Python

A utility library for [Xee API](https://dev.xee.com) with Python 3.

> Almost all the requests are done for you and the responses are returned as a **tuple**s.

## Install

* TODO: `pip install xee`
* CURRENT: Clone and setup install :) 

## Initializing the SDK

```python
from xee import Xee

xee = Xee(client_id="your_client_id", 
		client_secret="your_client_secret", 
		redirect_uri="your://redirect:uri")
```

## Using the SDK

### Authentication

#### Getting the [access code url](https://github.com/xee-lab/xee-api-docs/tree/master/api/api/v3/auth/auth.md)

```python
login_url = xee.get_authentication_url()
```

> Then show the webpage to the end user, once the process is complete, we'll redirect to `redirect_uri?code={authorization_code}`. Keep this code in mind

#### Getting a [token from an `authorization_code`](https://github.com/xee-lab/xee-api-docs/tree/master/api/api/v3/auth/access_token.md)

```python
token , error = xee.get_token_from_code(authorization_code)
```

### Requests

As simple as

```python
user , error = xee.get_user(token.access_token)
print(user.id)
```

See the [docs](https://github.com/quentin7b/xee-sdk-python/docs) for more about how to use it

## Contributing

I'm pretty new to *python*.

Tried to follow some "guidelines" I found:
- http://sametmax.com/planet-python-fr/
- https://github.com/kennethreitz/python-guide
- ...
 
But might be doing things in a wrong way so, feel free to **fork**, **issue**, **pr**, **everything** to improve this !

## Dependencies

To build this, I used some very useful libraries
- [isodate](https://pypi.python.org/pypi/isodate)
- [requests](https://pypi.python.org/pypi/requests)

And to test
- [responses](https://pypi.python.org/pypi/responses)
- [pytz](https://pypi.python.org/pypi/pytz)
