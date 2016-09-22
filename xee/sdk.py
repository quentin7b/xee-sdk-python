#!/usr/bin/env python
# coding: utf8
"""This script contains the Xee python SDK"""

try:
    import urllib.parse as url_parser
except ImportError:
    import urllib as url_parser

import isodate
import requests

import xee.entities as xee_entities
import xee.exceptions as xee_exceptions
import xee.utils as xee_utils


class Xee(object):
    """
        SDK for Xee platform v3.0
    """

    def __init__(self, client_id, client_secret, redirect_uri, env='cloud'):
        """
        Initialize a new Xee SDK.

        Parameters
        ----------
        client_id       :   str
                            The client id of your app.
        client_secret   :   str
                            The client secret of your app.
        redirect_uri    :   str
                            The redirect uri of your app.
        env             :   str, optional
                            The environment you want for the requests.
                            Can be 'cloud' or 'sandbox'.
                            Default is 'cloud'.

        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.host = 'https://{env}.xee.com/v3'.format(env=env)

    def get_authentication_url(self, state=None):
        """
        Generate and return the authentication url to call for the end user.

        Parameters
        ----------
        state : str, optional
                A state to pass to the authentication url.

        Returns
        -------
        str
            The url to call to display the authentication screen.

        """
        route = '{host}/auth/auth'.format(host=self.host)
        if state is None:
            query_params = url_parser.urlencode({'client_id': self.client_id})
        else:
            query_params = url_parser.urlencode({'client_id': self.client_id, 'state': state})
        return '{route}?{params}'.format(route=route, params=query_params)

    def get_token_from_code(self, code):
        """
        Fetch a new token from an authorization code.

        Parameters
        ----------
        code :  str
                he code to use to get the Bearer.

        Returns
        -------
        tuple
            A tuple containing the Token, Error.
            The error is None if everything went fine.

        """
        route = '{host}/auth/access_token'.format(host=self.host)
        payload = {'grant_type': 'authorization_code', 'code': code}
        request = requests.post(route, data=payload, auth=(self.client_id, self.client_secret))
        if request.status_code == 200:
            response = request.json()
            return xee_entities.parse_token(response), None
        else:
            return None, Exception(request.text)

    def get_token_from_refresh_token(self, refresh_token):
        """
        Fetch a new token from a refresh token.

        Parameters
        ----------
        refresh_token : str
                        the refresh token to use to get a new Token.

        Returns
        -------
        tuple
            A tuple containing the Token, Error.
            The error is None if everything went fine.

        """
        route = '{host}/auth/access_token'.format(host=self.host)
        payload = {'grant_type': 'refresh_token', 'refresh_token': refresh_token}
        request = requests.post(route, data=payload, auth=(self.client_id, self.client_secret))
        if request.status_code == 200:
            response = request.json()
            return xee_entities.parse_token(response), None
        else:
            return None, Exception(request.text)

    def get_user(self, access_token):
        """
        Fetch info about the connected user.

        Parameters
        ----------
        access_token :  str
                        the access token of the user.

        Returns
        -------
        tuple
            A tuple containing User, Error.
            The error is None if everything went fine.

        """
        route = '{host}/users/me'.format(host=self.host)
        try:
            response = xee_utils.do_get_request(route, access_token)
            return xee_entities.parse_user(response), None
        except (xee_exceptions.APIException, xee_exceptions.ParseException) as err:
            return None, err

    def get_cars(self, access_token):
        """
        Fetch the cars of the connected user.

        Parameters
        ----------
        access_token :  str
                        the access token of the user.

        Returns
        -------
        tuple
            A tuple containing [Car], Error.
            The error is None if everything went fine.

        """
        route = '{host}/users/me/cars'.format(host=self.host)
        try:
            response = xee_utils.do_get_request(route, access_token)
            return [xee_entities.parse_car(car) for car in response], None
        except ValueError:
            return [], None
        except (xee_exceptions.APIException, xee_exceptions.ParseException) as err:
            return None, err

    def get_car(self, car_id, access_token):
        """
        Fetch a specific car info.

        Parameters
        ----------
        car_id          :   str
                            the id of the car you are looking for.
        access_token    :   str
                            the access token of the user.

        Returns
        -------
        tuple
            A tuple containing Car, Error.
            The error is None if everything went fine.

        """
        route = '{host}/cars/{car_id}'.format(host=self.host, car_id=car_id)
        try:
            response = xee_utils.do_get_request(route, access_token)
            return xee_entities.parse_car(response), None
        except (xee_exceptions.APIException, xee_exceptions.ParseException) as err:
            return None, err

    def get_status(self, car_id, access_token):
        """
        Fetch the status of a car.

        Parameters
        ----------
        car_id          :   str
                            the id of the car you are looking for the status.
        access_token    :   str
                            the access token of the user.

        Returns
        -------
        tuple
            A tuple containing Status, Error.
            The error is None if everything went fine.

        """
        route = '{host}/cars/{car_id}/status'.format(host=self.host, car_id=car_id)
        try:
            response = xee_utils.do_get_request(route, access_token)
            return xee_entities.parse_status(response), None
        except (xee_exceptions.APIException, xee_exceptions.ParseException) as err:
            return None, err

    def get_signals(self, car_id, access_token, **options):
        """
        Fetch a list of signals for a specific car within a period.

        Parameters
        ----------
        car_id          :   str
                            the id of the car you are looking for the signals.
        access_token    :   str
                            the access token of the user.
        begin           :   datetime, optional
                            The first datetime of the interval you want the signals.
                            Default value is first day of month at 00:00:00.000.
        end             :   datetime, optional
                            The last datetime of the interval you want the signals.
                            Default value is current moment.
        limit           :   int, optional
                            The maximum number of values you want back.
                            Default value is no limit.
        names           :   list, optional
                            The list if signals names you want to filter the result.
                            For example ['Odometer', 'FuelLevel'].
                            Default value is all the signals available.

        Returns
        -------
        tuple
            A tuple containing [Signals], Error.
            The error is None if everything went fine.

        """
        route = '{host}/cars/{car_id}/signals'.format(host=self.host, car_id=car_id)
        params = {}
        o_limit = options.get('limit', None)
        if o_limit is not None:
            if o_limit > 0:
                params['limit'] = o_limit
            else:
                raise ValueError(
                    "limit must be a non 0 positive integer, " + str(o_limit) + " given")
        if options.get('begin', None) is not None:
            params['begin'] = isodate.datetime_isoformat(options['begin'])
        if options.get('end', None) is not None:
            params['end'] = isodate.datetime_isoformat(options['end'])
        if options.get('names', None) is not None:
            params['name'] = ','.join(options['names'])
        if bool(params):
            route = '?'.join([route, url_parser.urlencode(params)])
        try:
            response = xee_utils.do_get_request(route, access_token)
            return [xee_entities.parse_signal(signal) for signal in response], None
        except ValueError:
            # Happens when the signals list is empty
            return [], None
        except (xee_exceptions.APIException, xee_exceptions.ParseException) as err:
            return None, err

    def get_locations(self, car_id, access_token, **options):
        """
        Fetch a list of locations for a specific car within a period.

        Parameters
        ----------
        car_id          :   str
                            the id of the car you are looking for the locations.
        access_token    :   str
                            the access token of the user.
        begin           :   datetime, optional
                            The first datetime of the interval you want the locations.
                            Default value is first day of month at 00:00:00.000.
        end             :   datetime, optional
                            The last datetime of the interval you want the locations.
                            Default value is current moment.
        limit           :   int, optional
                            The maximum number of locations you want back.
                            Default value is no limit.

        Returns
        -------
        tuple
            A tuple containing [Locations], Error.
            The error is None if everything went fine.

        """
        route = '{host}/cars/{car_id}/locations'.format(host=self.host, car_id=car_id)
        params = {}
        if options.get('limit', None) is not None:
            params['limit'] = options['limit']
        if options.get('begin', None) is not None:
            params['begin'] = isodate.datetime_isoformat(options['begin'])
        if options.get('end', None) is not None:
            params['end'] = isodate.datetime_isoformat(options['end'])
        if bool(params):
            route = '?'.join([route, url_parser.urlencode(params)])
        try:
            response = xee_utils.do_get_request(route, access_token)
            return [xee_entities.parse_location(location) for location in response], None
        except ValueError:
            # Happens when the locations list is empty
            return [], None
        except (xee_exceptions.APIException, xee_exceptions.ParseException) as err:
            return None, err

    def get_trips(self, car_id, access_token, begin=None, end=None):
        """
        Fetch a list of trips for a specific car within a period.

        Parameters
        ----------
        car_id          :   str
                            the id of the car you are looking for the trips.
        access_token    :   str
                            the access token of the user.
        begin           :   datetime, optional
                            The first datetime of the interval you want the trips.
                            Default value is first day of month at 00:00:00.000.
        end             :   datetime, optional
                            The last datetime of the interval you want the trips.
                            Default value is current moment.

        Returns
        -------
        tuple
            A tuple containing [Trip], Error.
            The error is None if everything went fine.

        """
        route = '{host}/cars/{car_id}/trips'.format(host=self.host, car_id=car_id)
        params = {}
        if begin is not None:
            params['begin'] = isodate.datetime_isoformat(begin)
        if end is not None:
            params['end'] = isodate.datetime_isoformat(end)
        if bool(params):
            route = '?'.join([route, url_parser.urlencode(params)])
        try:
            response = xee_utils.do_get_request(route, access_token)
            return [xee_entities.parse_trip(trip) for trip in response], None
        except ValueError:
            # Happens when the trips list is empty
            return [], None
        except (xee_exceptions.APIException, xee_exceptions.ParseException) as err:
            return None, err

    def get_used_time(self, car_id, access_token, **options):
        """
        Fetch the used time value for a specific car within a period.

        Parameters
        ----------
        car_id          :   str
                            the id of the car you are looking for the used time.
        access_token    :   str
                            the access token of the user.
        begin           :   datetime, optional
                            The first datetime of the interval you want the used time.
                            Default value is first day of month at 00:00:00.000.
        end             :   datetime, optional
                            The last datetime of the interval you want the used time.
                            Default value is current moment.
        initial_value   :   int, optional
                            An offset for the used time (will be added to the new one).
                            Default value is 0.

        Returns
        -------
        tuple
            A tuple containing UsedTimeStat, Error.
            The error is None if everything went fine.

        """
        route = '{host}/cars/{car_id}/stats/usedtime'.format(host=self.host, car_id=car_id)
        params = {}
        if options.get('begin', None) is not None:
            params['begin'] = isodate.datetime_isoformat(options.get('begin'))
        if options.get('initial_value', None) is not None:
            params['end'] = isodate.datetime_isoformat(options.get('end'))
        if options.get('initial_value', None) is not None:
            params['initialValue'] = int(options.get('initial_value'))
        if bool(params):
            route = '?'.join([route, url_parser.urlencode(params)])
        try:
            response = xee_utils.do_get_request(route, access_token)
            return xee_entities.parse_used_time(response), None
        except (xee_exceptions.APIException, xee_exceptions.ParseException) as err:
            return None, err

    def get_mileage(self, car_id, access_token, **options):
        """
         Fetch the mileage value for a specific car within a period.

         Parameters
         ----------
         car_id          :   str
                             the id of the car you are looking for the mileage.
         access_token    :   str
                             the access token of the user.
         begin           :   datetime, optional
                             The first datetime of the interval you want the mileage.
                             Default value is first day of month at 00:00:00.000.
         end             :   datetime, optional
                             The last datetime of the interval you want the mileage.
                             Default value is current moment.
         initial_value   :   float, optional
                             An offset for the mileage (will be added to the new one).
                             Default value is 0.

         Returns
         -------
         tuple
             A tuple containing MileageStat, Error.
             The error is None if everything went fine.

         """
        route = '{host}/cars/{car_id}/stats/mileage'.format(host=self.host, car_id=car_id)
        params = {}
        if options.get('begin', None) is not None:
            params['begin'] = isodate.datetime_isoformat(options.get('begin'))
        if options.get('initial_value', None) is not None:
            params['end'] = isodate.datetime_isoformat(options.get('end'))
        if options.get('initial_value', None) is not None:
            params['initialValue'] = float(options.get('initial_value'))
        if bool(params):
            route = '?'.join([route, url_parser.urlencode(params)])
        try:
            response = xee_utils.do_get_request(route, access_token)
            return xee_entities.parse_mileage(response), None
        except (xee_exceptions.APIException, xee_exceptions.ParseException) as err:
            return None, err

    def get_trip(self, trip_id, access_token):
        """
        Fetch a specific trip from a car.

        Parameters
        ----------
        trip_id         :   str
                            the id of the trip you are looking for.
        access_token    :   str
                            the access token of the user.

        Returns
        -------
        tuple
            A tuple containing Trip, Error.
            The error is None if everything went fine.

        """
        route = '{host}/trips/{trip_id}'.format(host=self.host, trip_id=trip_id)
        try:
            response = xee_utils.do_get_request(route, access_token)
            return xee_entities.parse_trip(response), None
        except (xee_exceptions.APIException, xee_exceptions.ParseException) as err:
            return None, err

    def get_trip_signals(self, trip_id, access_token, names=None):
        """
        Fetch a list of signals for a specific car during a trip.

        Parameters
        ----------
        trip_id         :   str
                            the id of the trip you are looking for the signals.
        access_token    :   str
                            the access token of the user.
        names           :   list, optional
                            The list if signals names you want to filter the result.
                            For example ['Odometer', 'FuelLevel'].
                            Default value is all the signals available.

        Returns
        -------
        tuple
            A tuple containing [Signals], Error.
            The error is None if everything went fine.

        """
        route = '{host}/trips/{trip_id}/signals'.format(host=self.host, trip_id=trip_id)
        params = {}
        if names is not None:
            params['name'] = ','.join(names)
        if bool(params):
            route = '{route}?{params}'.format(route=route, params=url_parser.urlencode(params))
        try:
            response = xee_utils.do_get_request(route, access_token)
            signals = [xee_entities.parse_signal(signal) for signal in response]
            return signals, None
        except ValueError:
            # Happens when the signals list is empty
            return [], None
        except (xee_exceptions.APIException, xee_exceptions.ParseException) as err:
            return None, err

    def get_trip_locations(self, trip_id, access_token):
        """
        Fetch a list of locations for a specific car during a trip.

        Parameters
        ----------
        trip_id         :   str
                            the id of the trip you are looking for the signals.
        access_token    :   str
                            the access token of the user.

        Returns
        -------
        tuple
            A tuple containing [Locations], Error.
            The error is None if everything went fine.

        """
        route = '{host}/trips/{trip_id}/locations'.format(host=self.host, trip_id=trip_id)
        try:
            response = xee_utils.do_get_request(route, access_token)
            locations = [xee_entities.parse_location(location) for location in response]
            return locations, None
        except ValueError:
            # Happens when the locations list is empty
            return [], None
        except (xee_exceptions.APIException, xee_exceptions.ParseException) as err:
            return None, err

    def get_trip_stats(self, trip_id, access_token):
        """
        Fetch a list of stats for a specific trip.

        Parameters
        ----------
        trip_id         :   str
                            the id of the trip you are looking for the stats.
        access_token    :   str
                            the access token of the user.

        Returns
        -------
        tuple
            A tuple containing [TripStat], Error.
            The error is None if everything went fine.

        """
        route = '{host}/trips/{trip_id}/stats'.format(host=self.host, trip_id=trip_id)
        try:
            response = xee_utils.do_get_request(route, access_token)
            stats = [xee_entities.parse_trip_stat(stat) for stat in response]
            return stats, None
        except ValueError:
            # Happens when the stats list is empty
            return [], None
        except (xee_exceptions.APIException, xee_exceptions.ParseException) as err:
            return None, err

    def get_trip_mileage(self, trip_id, access_token):
        """
        Fetch trip mileage stat.

        Parameters
        ----------
        trip_id         :   str
                            the id of the trip you are looking for the mileage.
        access_token    :   str
                            the access token of the user.

        Returns
        -------
        tuple
            A tuple containing TripStat, Error.
            The error is None if everything went fine.

        """
        route = '{host}/trips/{trip_id}/stats/mileage'.format(host=self.host, trip_id=trip_id)
        try:
            response = xee_utils.do_get_request(route, access_token)
            mileage = xee_entities.parse_trip_stat(response)
            return mileage, None
        except (xee_exceptions.APIException, xee_exceptions.ParseException) as err:
            return None, err

    def get_trip_duration(self, trip_id, access_token):
        """
        Fetch trip duration stat.

        Parameters
        ----------
        trip_id         :   str
                            the id of the trip you are looking for the duration.
        access_token    :   str
                            the access token of the user.

        Returns
        -------
        tuple
            A tuple containing TripStat, Error.
            The error is None if everything went fine.

        """
        route = '{host}/trips/{trip_id}/stats/usedtime'.format(host=self.host, trip_id=trip_id)
        try:
            response = xee_utils.do_get_request(route, access_token)
            used_time = xee_entities.parse_trip_stat(response)
            return used_time, None
        except (xee_exceptions.APIException, xee_exceptions.ParseException) as err:
            return None, err
