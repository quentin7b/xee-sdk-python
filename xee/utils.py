#!/usr/bin/env python
# coding: utf8
"""This script contains the helpers for the 3rd version of the API"""

import requests

import xee.exceptions as xee_exceptions


def do_get_request(route, bearer):
    """
    Do a request to a route with a Authorization header.

    Parameters
    ----------
    route   :     str
                  The route to call (fully).
    bearer  :     str
                  The bearer to use for authentication.

    Returns
    -------
    dict
        The response (mostly JSON response) of the API.

    Raises
    ------
    APIException
        If the API responded with a known error (400, 401, 403, 404, 416, 500)

    Exception
        If the API responded with an "unknown" error

    """
    request = requests.get(route, headers={'Authorization': 'Bearer ' + bearer})
    response = request.json()
    if request.status_code == 200:
        return response
    else:
        first_error = response[0]
        if request.status_code in [400, 401, 403, 404, 416, 500]:
            raise xee_exceptions.APIException(str(first_error['type']), str(first_error['message']),
                                              str(first_error['tip']))
        else:
            raise Exception(response)
