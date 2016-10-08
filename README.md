#  Xee SDK Python

[![Build Status](https://travis-ci.org/quentin7b/xee-sdk-python.svg?branch=master)](https://travis-ci.org/quentin7b/xee-sdk-python)
[![codecov](https://codecov.io/gh/quentin7b/xee-sdk-python/branch/master/graph/badge.svg)](https://codecov.io/gh/quentin7b/xee-sdk-python)
[![License Apache](https://img.shields.io/badge/License-Apache%202.0-green.svg?style=flat)](./LICENSE)
[![Version](https://img.shields.io/badge/Version-3.0.2-blue.svg?style=flat)](https://github.com/quentin7b/xee-sdk-python/releases/tag/3.0.2)

A utility library for [Xee API](https://dev.xee.com) with Python 3.

> Almost all the requests are done for you and the responses are returned as a **tuple**s.

## Install

* Clone and `python setup.py install` :) 

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
token, error = xee.get_token_from_code(authorization_code)
```

#### Getting a [token from an `refresh_token`](https://github.com/xee-lab/xee-api-docs/tree/master/api/api/v3/auth/access_token.md)

```python
token, error = xee.get_token_from_refresh_token(token.refresh_token)
```
### Requests

As simple as

```python
user, error = xee.get_user(token.access_token)
print(user.id)
```

Others examples:

```python
status, error = xee.get_status(carId, token.access_token)
print(status)
```

```python
signal, error = xee.get_signals(carId, token.access_token,names=['Odometer', 'FuelLevel'])
print(signal)
```

```python
trip_duration, error = xee.get_trip_duration(tripId, token.access_token)
print(trip_duration.value)
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
