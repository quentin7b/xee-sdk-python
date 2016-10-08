#!/usr/bin/env python
# coding: utf8
"""This script contains the parsers for the 3rd version of the API"""

import collections
import isodate

import xee.exceptions as xee_exceptions

# Class list

Token = collections.namedtuple(
    'Token',
    [
        'access_token',
        'refresh_token',
        'expires_in',
        'expires_at'
    ])
User = collections.namedtuple(
    'User',
    [
        'id',
        'last_name',
        'first_name',
        'nick_name',
        'gender',
        'birth_date',
        'licence_delivery_date',
        'role',
        'is_location_enabled'
    ])
Car = collections.namedtuple(
    'Car',
    [
        'id',
        'name',
        'make',
        'model',
        'year',
        'number_plate',
        'device_id',
        'cardb_id'
    ])
Signal = collections.namedtuple(
    'Signal',
    [
        'name',
        'value',
        'date'
    ])
Location = collections.namedtuple(
    'Location',
    [
        'latitude',
        'longitude',
        'altitude',
        'satellites',
        'heading',
        'date'
    ])
Accelerometer = collections.namedtuple(
    'Accelerometer',
    [
        'x',
        'y',
        'z',
        'date'
    ])
Status = collections.namedtuple(
    'Status',
    [
        'location',
        'accelerometer',
        'signals'
    ])
Trip = collections.namedtuple(
    'Trip',
    [
        'id',
        'begin_location',
        'end_location',
        'begin_date',
        'end_date'
    ])
UsedTimeStat = collections.namedtuple(
    'UsedTimeStat',
    [
        'begin_date',
        'end_date',
        'type',
        'value'
    ])
MileageStat = collections.namedtuple(
    'MileageStat',
    [
        'begin_date',
        'end_date',
        'type',
        'value'
    ])
TripStat = collections.namedtuple(
    'TripStat',
    [
        'type',
        'value'
    ])
SignalsAvailability = collections.namedtuple(
    'SignalsAvailability',
    [
        'available',
        'unavailable'
    ])
SignalAvailability = collections.namedtuple(
    'SignalAvailability',
    [
        'name',
        'reliability'
    ])

# Parsers

def parse_token(token):
    """
    Parse a Token from a dict representation.

    Parameters
    ----------
    token : dict
            The token as a dict.

    Returns
    -------
    tuple
        A namedtuple containing token info.
        The error is None if everything went fine.

    Raises
    ------
    ValueError
        If the dict does not contains the correct data.

    """
    try:
        return Token(
            token['access_token'],
            token['refresh_token'],
            token['expires_in'],
            token['expires_at']
        )
    except ValueError as err:
        raise xee_exceptions.ParseException(err)


def parse_user(user):
    """
    Parse a User from a dict representation.

    Parameters
    ----------
    user  : dict
            The user as a dict.

    Returns
    -------
    tuple
        A namedtuple containing user info.
        The error is None if everything went fine.

    Raises
    ------
    ValueError
        If the dict does not contains the correct data.

    """
    birth_date = None
    if user['birthDate']:
        birth_date = isodate.parse_datetime(user['birthDate'])
    licence_delivery_date = None
    if user['licenseDeliveryDate']:
        licence_delivery_date = isodate.parse_datetime(user['licenseDeliveryDate'])
    try:
        return User(
            user['id'],
            user['lastName'],
            user['firstName'],
            user['nickName'],
            user['gender'],
            birth_date,
            licence_delivery_date,
            user['role'],
            user['isLocationEnabled']
        )
    except ValueError as err:
        raise xee_exceptions.ParseException(err)


def parse_car(car):
    """
    Parse a Car from a dict representation.

    Parameters
    ----------
    car  :  dict
            The car as a json dict.

    Returns
    -------
    tuple
        A namedtuple containing car info.
        The error is None if everything went fine.

    Raises
    ------
    ValueError
        If the dict does not contains the correct data.

    """
    try:
        return Car(
            car['id'],
            car['name'],
            car['make'],
            car['model'],
            car['year'],
            car['numberPlate'],
            car['deviceId'],
            car['cardbId']
        )
    except ValueError as err:
        raise xee_exceptions.ParseException(err)


def parse_signal(signal):
    """
    Parse a Signal from a a dict representation.

    Parameters
    ----------
    signal  :   dict
                The signal as a dict.

    Returns
    -------
    tuple
        A namedtuple containing signal info.
        The error is None if everything went fine.

    Raises
    ------
    ValueError
        If the dict does not contains the correct data.

    """
    try:
        return Signal(
            signal['name'],
            signal['value'],
            isodate.parse_datetime(signal['date'])
        )
    except ValueError as err:
        raise xee_exceptions.ParseException(err)


def parse_location(location):
    """
    Parse a Location from a a dict representation.

    Parameters
    ----------
    location  : dict
                The signal as a dict.

    Returns
    -------
    tuple
        A namedtuple containing location info.
        The error is None if everything went fine.

    Raises
    ------
    ValueError
        If the dict does not contains the correct data.

    """
    try:
        return Location(
            location['latitude'],
            location['longitude'],
            location['altitude'],
            location['satellites'],
            location['heading'],
            isodate.parse_datetime(location['date'])
        )
    except ValueError as err:
        raise xee_exceptions.ParseException(err)


def parse_status(status):
    """
    Parse a Status from a a dict representation.

    Parameters
    ----------
    status  :   dict
                The status as a dict.

    Returns
    -------
    tuple
        A namedtuple containing status info.
        The error is None if everything went fine.

    Raises
    ------
    ValueError
        If the dict does not contains the correct data.

    """
    try:
        accelerometer = None
        if 'accelerometer' in status:
            accelerometer_dict = status['accelerometer']
            if accelerometer_dict:
                accelerometer = Accelerometer(accelerometer_dict['x'], accelerometer_dict['y'],
                                              accelerometer_dict['z'],
                                              isodate.parse_datetime(accelerometer_dict['date']))
        location = None
        if 'location' in status:
            location_dict = status['location']
            if location_dict:
                location = parse_location(location_dict)
        return Status(
            location,
            accelerometer,
            [parse_signal(signal) for signal in status['signals']]
        )
    except ValueError as err:
        raise xee_exceptions.ParseException(err)


def parse_used_time(used_time):
    """
    Parse a UsedTimeStat from a a dict representation.

    Parameters
    ----------
    used_time  :    dict
                    The used time as a dict.

    Returns
    -------
    tuple
        A namedtuple containing used time stat info.
        The error is None if everything went fine.

    Raises
    ------
    ValueError
        If the dict does not contains the correct data.

    """
    try:
        return UsedTimeStat(
            isodate.parse_datetime(used_time['beginDate']),
            isodate.parse_datetime(used_time['endDate']),
            used_time['type'],
            used_time['value'],
        )
    except ValueError as err:
        raise xee_exceptions.ParseException(err)


def parse_mileage(mileage):
    """
    Parse a MileageStat from a a dict representation.

    Parameters
    ----------
    mileage  :  dict
                The mileage as a dict.

    Returns
    -------
    tuple
        A namedtuple containing mileage stat info.
        The error is None if everything went fine.

    Raises
    ------
    ValueError
        If the dict does not contains the correct data.

    """
    try:
        return MileageStat(
            isodate.parse_datetime(mileage['beginDate']),
            isodate.parse_datetime(mileage['endDate']),
            mileage['type'],
            mileage['value'],
        )
    except ValueError as err:
        raise xee_exceptions.ParseException(err)


def parse_trip(trip):
    """
    Parse a trip from a a dict representation.

    Parameters
    ----------
    trip  : dict
            The trip as a dict.

    Returns
    -------
    tuple
        A namedtuple containing trip info.
        The error is None if everything went fine.

    Raises
    ------
    ValueError
        If the dict does not contains the correct data.

    """
    try:
        return Trip(
            trip['id'],
            parse_location(trip['beginLocation']),
            parse_location(trip['endLocation']),
            isodate.parse_datetime(trip['beginDate']),
            isodate.parse_datetime(trip['endDate'])
        )
    except ValueError as err:
        raise xee_exceptions.ParseException(err)


def parse_trip_stat(trip_stat):
    """
    Parse a trip stat from a a dict representation.

    Parameters
    ----------
    trip_stat  : dict
                 The trip stat as a dict.

    Returns
    -------
    tuple
        A namedtuple containing trip stat info.
        The error is None if everything went fine.

    Raises
    ------
    ValueError
        If the dict does not contains the correct data.

    """
    try:
        return TripStat(
            trip_stat['type'],
            trip_stat['value']
        )
    except ValueError as err:
        raise xee_exceptions.ParseException(err)

def parse_availability(availability):
    """
    Parse an availability from a a dict representation.

    Parameters
    ----------
    availability  : dict
                    The availability as a dict.

    Returns
    -------
    tuple
        A namedtuple containing availability info.
        The error is None if everything went fine.

    Raises
    ------
    ValueError
        If the dict does not contains the correct data.

    """
    try:
        available_signals_dict = availability['signalsAvailable']
        unavailable_signals_dict = availability['signalsUnavailable']
        return SignalsAvailability(
            [parse_signal_availability(signal_availability)
             for signal_availability in available_signals_dict],
            [parse_signal_availability(signal_availability)
             for signal_availability in unavailable_signals_dict])
    except ValueError as err:
        raise xee_exceptions.ParseException(err)

def parse_signal_availability(signal_availability):
    """
    Parse a signal availability from a a dict representation.

    Parameters
    ----------
    availability  : dict
                    The signal availability as a dict.

    Returns
    -------
    tuple
        A namedtuple containing signal availability info.
        The error is None if everything went fine.

    Raises
    ------
    ValueError
        If the dict does not contains the correct data.

    """
    try:
        return SignalAvailability(
            signal_availability['name'],
            signal_availability['reliability']
        )
    except ValueError as err:
        raise xee_exceptions.ParseException(err)
