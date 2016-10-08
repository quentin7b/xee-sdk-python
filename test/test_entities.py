#!/usr/bin/env python
# coding: utf8
import unittest

from xee.exceptions import ParseException
import xee.entities as xee_entities
from datetime import datetime
import pytz

class TestTokenParser(unittest.TestCase):
    def test_parse_ok(self):
        token_dict = {
            "access_token"  : "22fe0c13e995da4a44a63a7ff549badb5d337a42bf80f17424482e35d4cca91a",
            "expires_at"    : 1382962374,
            "expires_in"    : 3600,
            "refresh_token" : "8eb667707535655f2d9e14fc6491a59f6e06f2e73170761259907d8de186b6a1",
            "token_type"    : "bearer"
        }
        token = xee_entities.parse_token(token_dict)
        self.assertEqual(token.access_token, "22fe0c13e995da4a44a63a7ff549badb5d337a42bf80f17424482e35d4cca91a")
        self.assertEqual(token.expires_at, 1382962374)
        self.assertEqual(token.expires_in, 3600)
        self.assertEqual(token.refresh_token, "8eb667707535655f2d9e14fc6491a59f6e06f2e73170761259907d8de186b6a1")

    def test_parse_wrong_field(self):
        token_dict = {
            "accessToken"  : "22fe0c13e995da4a44a63a7ff549badb5d337a42bf80f17424482e35d4cca91a",
            "expires_at"    : 1382962374,
            "expires_in"    : 3600,
            "refresh_token" : "8eb667707535655f2d9e14fc6491a59f6e06f2e73170761259907d8de186b6a1",
            "token_type"    : "bearer"
        }
        try:
            token = xee_entities.parse_token(token_dict)
        except ParseException as err:
            self.assertIsNotNone(err)

    def test_parse_missing_field(self):
        token_dict = {
            "expires_at"    : 1382962374,
            "expires_in"    : 3600,
            "refresh_token" : "8eb667707535655f2d9e14fc6491a59f6e06f2e73170761259907d8de186b6a1",
            "token_type"    : "bearer"
        }
        try:
            token = xee_entities.parse_token(token_dict)
        except ParseException as err:
            self.assertIsNotNone(err)

class TestUserParser(unittest.TestCase):
    def test_parse_ok(self):
        user_dict = {
            "id": 42,
            "lastName": "Doe",
            "firstName": "John",
            "nickName": "Johny",
            "gender": "MALE",
            "birthDate": "2016-01-11T00:00:00+00:00",
            "licenseDeliveryDate": "2014-08-13T00:00:00+00:00",
            "role": "dev",
            "isLocationEnabled": True,
            "creationDate": "2014-08-13T15:20:58+00:00",
            "lastUpdateDate": "2016-02-12T09:07:47+00:00",
        }
        user = xee_entities.parse_user(user_dict)
        self.assertEqual(user.id, 42)
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.nick_name, 'Johny')
        self.assertEqual(user.gender, 'MALE')
        self.assertEqual(user.birth_date, datetime(2016, 1, 11, 0, 0, 0, tzinfo=pytz.utc))
        self.assertEqual(user.licence_delivery_date,
                         datetime(2014, 8, 13, 0, 0, 0, tzinfo=pytz.utc))
        self.assertEqual(user.role, 'dev')
        self.assertEqual(user.is_location_enabled, True)

    def test_parse_wrong_field(self):
        user_dict = {
            "id": 42,
            "lastName": "Doe",
            "firstName": "John",
            "nickname": "Johny",
            "gender": "MALE",
            "birthDate": "2016-01-11T00:00:00+00:00",
            "licenseDeliveryDate": "2014-08-13T00:00:00+00:00",
            "role": "dev",
            "isLocationEnabled": True,
            "creationDate": "2014-08-13T15:20:58+00:00",
            "lastUpdateDate": "2016-02-12T09:07:47+00:00",
        }
        try:
            user = xee_entities.parse_user(user_dict)
        except ParseException as err:
            self.assertIsNotNone(err)

    def test_parse_missing_field(self):
        user_dict = {
            "lastName": "Doe",
            "firstName": "John",
            "nickname": "Johny",
            "gender": "MALE",
            "birthDate": "2016-01-11T00:00:00+00:00",
            "licenseDeliveryDate": "2014-08-13T00:00:00+00:00",
            "role": "dev",
            "isLocationEnabled": True,
            "creationDate": "2014-08-13T15:20:58+00:00",
            "lastUpdateDate": "2016-02-12T09:07:47+00:00",
        }
        try:
            user = xee_entities.parse_user(user_dict)
        except ParseException as err:
            self.assertIsNotNone(err)

class TestCarParser(unittest.TestCase):
    def test_parse_ok(self):
        car_dict = {
            "id": 1337,
            "name": "Mark-42",
            "make": "Mark",
            "model": "42",
            "year": 2014,
            "numberPlate": "M-42-TS",
            "deviceId": "E133742015",
            "cardbId": 210,
            "creationDate": "2014-09-23T12:49:48+00:00",
            "lastUpdateDate": "2016-02-19T08:41:58+00:00"
        }
        car = xee_entities.parse_car(car_dict)
        self.assertEqual(car.id, 1337)
        self.assertEqual(car.name, 'Mark-42')
        self.assertEqual(car.make, 'Mark')
        self.assertEqual(car.model, '42')
        self.assertEqual(car.year, 2014)
        self.assertEqual(car.number_plate, 'M-42-TS')
        self.assertEqual(car.device_id, 'E133742015')
        self.assertEqual(car.cardb_id, 210)

    def test_parse_wrong_field(self):
        car_dict = {
            "ID": 1337,
            "name": "Mark-42",
            "make": "Mark",
            "model": "42",
            "year": 2014,
            "numberPlate": "M-42-TS",
            "deviceId": "E133742015",
            "cardbId": 210,
            "creationDate": "2014-09-23T12:49:48+00:00",
            "lastUpdateDate": "2016-02-19T08:41:58+00:00"
        }
        try:
            car = xee_entities.parse_car(car_dict)
        except ParseException as err:
            self.assertIsNotNone(err)

    def test_parse_missing_field(self):
        car_dict = {
            "name": "Mark-42",
            "make": "Mark",
            "model": "42",
            "year": 2014,
            "numberPlate": "M-42-TS",
            "deviceId": "E133742015",
            "cardbId": 210,
            "creationDate": "2014-09-23T12:49:48+00:00",
            "lastUpdateDate": "2016-02-19T08:41:58+00:00"
        }
        try:
            car = xee_entities.parse_car(car_dict)
        except ParseException as err:
            self.assertIsNotNone(err)

class TestSignalParser(unittest.TestCase):
    def test_parse_ok(self):
        signal_dict = {
            "name": "LockSts",
            "value": 0,
            "date": "2016-03-01T02:24:24.000000+00:00"
        }
        signal = xee_entities.parse_signal(signal_dict)
        self.assertEqual(signal.name, 'LockSts')
        self.assertEqual(signal.value, 0.0)
        self.assertEqual(signal.date, datetime(2016, 3, 1, 2, 24, 24, 0, tzinfo=pytz.utc))

    def test_parse_wrong_field(self):
        signal_dict = {
            "name": "Locksts",
            "value": 0,
            "date": "2016-03-01T02:24:24.000000+00:00"
        }
        try:
            signal = xee_entities.parse_signal(signal_dict)
        except ParseException as err:
            self.assertIsNotNone(err)

    def test_parse_missing_field(self):
        signal_dict = {
            "value": 0,
            "date": "2016-03-01T02:24:24.000000+00:00"
        }
        try:
            signal = xee_entities.parse_signal(signal_dict)
        except ParseException as err:
            self.assertIsNotNone(err)

class TestLocationParser(unittest.TestCase):
    def test_parse_ok(self):
        location_dict = {
            "latitude": 50.67815,
            "longitude": 3.208155,
            "altitude": 31.8,
            "satellites": 4,
            "heading": 167,
            "date": "2016-03-01T02:24:20.000000+00:00"
        }
        location = xee_entities.parse_location(location_dict)
        self.assertEqual(location.latitude, 50.67815)
        self.assertEqual(location.longitude, 3.208155)
        self.assertEqual(location.altitude, 31.8)
        self.assertEqual(location.satellites, 4)
        self.assertEqual(location.heading, 167)
        self.assertEqual(location.date, datetime(2016, 3, 1, 2, 24, 20, 0, tzinfo=pytz.utc))

    def test_parse_wrong_field(self):
        location_dict = {
            "ltt": 50.67815,
            "longitude": 3.208155,
            "altitude": 31.8,
            "satellites": 4,
            "heading": 167,
            "date": "2016-03-01T02:24:20.000000+00:00"
        }
        try:
            location = xee_entities.parse_location(location_dict)
        except ParseException as err:
            self.assertIsNotNone(err)

    def test_parse_missing_field(self):
        location_dict = {
            "longitude": 3.208155,
            "altitude": 31.8,
            "satellites": 4,
            "heading": 167,
            "date": "2016-03-01T02:24:20.000000+00:00"
        }
        try:
            location = xee_entities.parse_location(location_dict)
        except ParseException as err:
            self.assertIsNotNone(err)

class TestStatusParser(unittest.TestCase):
    def test_parse_ok(self):
        status_dict = {
            "accelerometer": {
                "x": -768,
                "y": 240,
                "z": 4032,
                "date": "2016-03-01T02:24:20.000000+00:00"
                },
            "location": {
                "latitude": 50.67815,
                "longitude": 3.208155,
                "altitude": 31.8,
                "satellites": 4,
                "heading": 167,
                "date": "2016-03-01T02:24:20.000000+00:00"
            },
            "signals": [
                {
                    "name": "LockSts",
                    "value": 0,
                    "date": "2016-03-01T02:24:24.000000+00:00"
                },
                {
                    "name": "Odometer",
                    "value": 34512.1,
                    "date": "2016-03-01T02:24:27.116000+00:00"
                }
            ]
        }
        status = xee_entities.parse_status(status_dict)
        self.assertEqual(status.accelerometer.x, -768)
        self.assertEqual(status.accelerometer.y, 240)
        self.assertEqual(status.accelerometer.z, 4032)
        self.assertEqual(status.accelerometer.date, datetime(2016, 3, 1, 2, 24, 20, 0, tzinfo=pytz.utc))

        self.assertEqual(status.location.latitude, 50.67815)
        self.assertEqual(status.location.longitude, 3.208155)
        self.assertEqual(status.location.altitude, 31.8)
        self.assertEqual(status.location.satellites, 4)
        self.assertEqual(status.location.heading, 167)
        self.assertEqual(status.location.date, datetime(2016, 3, 1, 2, 24, 20, 0, tzinfo=pytz.utc))

        self.assertEqual(len(status.signals), 2)
        self.assertEqual(status.signals[0].name, 'LockSts')
        self.assertEqual(status.signals[0].value, 0)
        self.assertEqual(status.signals[0].date, datetime(2016, 3, 1, 2, 24, 24, 0, tzinfo=pytz.utc))
        self.assertEqual(status.signals[1].name, 'Odometer')
        self.assertEqual(status.signals[1].value, 34512.1)
        self.assertEqual(status.signals[1].date, datetime(2016, 3, 1, 2, 24, 27, 116000, tzinfo=pytz.utc))

    def test_parse_ok_no_accelerometer(self):
        status_dict = {
            "accelerometer": None,
            "location": {
                "latitude": 50.67815,
                "longitude": 3.208155,
                "altitude": 31.8,
                "satellites": 4,
                "heading": 167,
                "date": "2016-03-01T02:24:20.000000+00:00"
            },
            "signals": [
                {
                    "name": "LockSts",
                    "value": 0,
                    "date": "2016-03-01T02:24:24.000000+00:00"
                },
                {
                    "name": "Odometer",
                    "value": 34512.1,
                    "date": "2016-03-01T02:24:27.116000+00:00"
                }
            ]
        }
        status = xee_entities.parse_status(status_dict)
        self.assertIsNone(status.accelerometer)

        self.assertEqual(status.location.latitude, 50.67815)
        self.assertEqual(status.location.longitude, 3.208155)
        self.assertEqual(status.location.altitude, 31.8)
        self.assertEqual(status.location.satellites, 4)
        self.assertEqual(status.location.heading, 167)
        self.assertEqual(status.location.date, datetime(2016, 3, 1, 2, 24, 20, 0, tzinfo=pytz.utc))

        self.assertEqual(len(status.signals), 2)
        self.assertEqual(status.signals[0].name, 'LockSts')
        self.assertEqual(status.signals[0].value, 0)
        self.assertEqual(status.signals[0].date, datetime(2016, 3, 1, 2, 24, 24, 0, tzinfo=pytz.utc))
        self.assertEqual(status.signals[1].name, 'Odometer')
        self.assertEqual(status.signals[1].value, 34512.1)
        self.assertEqual(status.signals[1].date, datetime(2016, 3, 1, 2, 24, 27, 116000, tzinfo=pytz.utc))

    def test_parse_ok_no_location(self):
        status_dict = {
            "accelerometer": None,
            "location": None,
            "signals": [
                {
                    "name": "LockSts",
                    "value": 0,
                    "date": "2016-03-01T02:24:24.000000+00:00"
                },
                {
                    "name": "Odometer",
                    "value": 34512.1,
                    "date": "2016-03-01T02:24:27.116000+00:00"
                }
            ]
        }
        status = xee_entities.parse_status(status_dict)
        self.assertIsNone(status.accelerometer)

        self.assertIsNone(status.location)

        self.assertEqual(len(status.signals), 2)
        self.assertEqual(status.signals[0].name, 'LockSts')
        self.assertEqual(status.signals[0].value, 0)
        self.assertEqual(status.signals[0].date, datetime(2016, 3, 1, 2, 24, 24, 0, tzinfo=pytz.utc))
        self.assertEqual(status.signals[1].name, 'Odometer')
        self.assertEqual(status.signals[1].value, 34512.1)
        self.assertEqual(status.signals[1].date, datetime(2016, 3, 1, 2, 24, 27, 116000, tzinfo=pytz.utc))

    def test_parse_wrong_field(self):
        status_dict = {
            "acc": None,
            "location": None,
            "sig": [
                {
                    "name": "LockSts",
                    "value": 0,
                    "date": "2016-03-01T02:24:24.000000+00:00"
                },
                {
                    "name": "Odometer",
                    "value": 34512.1,
                    "date": "2016-03-01T02:24:27.116000+00:00"
                }
            ]
        }
        try:
            status = xee_entities.parse_status(status_dict)
        except ParseException as err:
            self.assertIsNotNone(err)

    def test_parse_missing_field(self):
        status_dict = {
            "location": None,
        }
        try:
            status = xee_entities.parse_status(status_dict)
        except ParseException as err:
            self.assertIsNotNone(err)

class TestTripParser(unittest.TestCase):
    def test_parse_ok(self):
        trip_dict = {
            "id": "56b43a4f051f29071f14218d",
            "beginLocation": {
                "latitude": 50.6817,
                "longitude": 3.08202,
                "altitude": 2,
                "heading": 0,
                "satellites": 1,
                "date": "2016-01-29T18:36:17Z"
            },
            "endLocation": {
                "latitude": 50.6817,
                "longitude": 3.08202,
                "altitude": 3,
                "heading": 4,
                "satellites": 1,
                "date": "2016-01-29T18:36:17Z"
            },
            "beginDate": "2016-01-29T18:39:17Z",
            "endDate": "2016-01-29T19:15:15Z",
            "creationDate": "2016-01-29T18:39:17Z",
            "lastUpdateDate": "2016-01-29T19:15:15Z"
        }
        trip = xee_entities.parse_trip(trip_dict)

        self.assertEqual(trip.begin_location.latitude, 50.6817)
        self.assertEqual(trip.begin_location.longitude, 3.08202)
        self.assertEqual(trip.begin_location.altitude, 2)
        self.assertEqual(trip.begin_location.satellites, 1)
        self.assertEqual(trip.begin_location.heading, 0)
        self.assertEqual(trip.begin_location.date, datetime(2016, 1, 29, 18, 36, 17, 0, tzinfo=pytz.utc))

        self.assertEqual(trip.end_location.latitude, 50.6817)
        self.assertEqual(trip.end_location.longitude, 3.08202)
        self.assertEqual(trip.end_location.altitude, 3)
        self.assertEqual(trip.end_location.satellites, 1)
        self.assertEqual(trip.end_location.heading, 4)
        self.assertEqual(trip.end_location.date, datetime(2016, 1, 29, 18, 36, 17, 0, tzinfo=pytz.utc))

        self.assertEqual(trip.begin_date, datetime(2016, 1, 29, 18, 39, 17, 0, tzinfo=pytz.utc))
        self.assertEqual(trip.end_date, datetime(2016, 1, 29, 19, 15, 15, 0, tzinfo=pytz.utc))

    def test_parse_wrong_field(self):
        trip_dict = {
            "ID": "56b43a4f051f29071f14218d",
            "beginLocation": {
                "latitude": 50.6817,
                "longitude": 3.08202,
                "altitude": 2,
                "heading": 0,
                "satellites": 1,
                "date": "2016-01-29T18:36:17Z"
            },
            "endLocation": {
                "latitude": 50.6817,
                "longitude": 3.08202,
                "altitude": 2,
                "heading": 0,
                "satellites": 1,
                "date": "2016-01-29T18:36:17Z"
            },
            "beginDate": "2016-01-29T18:39:17Z",
            "endDate": "2016-01-29T19:15:15Z",
            "creationDate": "2016-01-29T18:39:17Z",
            "lastUpdateDate": "2016-01-29T19:15:15Z"
        }
        try:
            trip = xee_entities.parse_trip(trip_dict)
        except ParseException as err:
            self.assertIsNotNone(err)

    def test_parse_missing_field(self):
        trip_dict = {
            "beginLocation": {
                "latitude": 50.6817,
                "longitude": 3.08202,
                "altitude": 2,
                "heading": 0,
                "satellites": 1,
                "date": "2016-01-29T18:36:17Z"
            },
            "endLocation": {
                "latitude": 50.6817,
                "longitude": 3.08202,
                "altitude": 2,
                "heading": 0,
                "satellites": 1,
                "date": "2016-01-29T18:36:17Z"
            },
            "beginDate": "2016-01-29T18:39:17Z",
            "endDate": "2016-01-29T19:15:15Z",
            "creationDate": "2016-01-29T18:39:17Z",
            "lastUpdateDate": "2016-01-29T19:15:15Z"
        }
        try:
            trip = xee_entities.parse_trip(trip_dict)
        except ParseException as err:
            self.assertIsNotNone(err)

class TestUsedTimeParser(unittest.TestCase):
    def test_parse_ok(self):
        used_time_dict = {
            "beginDate": "2016-07-01T00:00:00Z",
            "endDate": "2016-07-15T12:34:30.447653Z",
            "type": "USED_TIME",
            "value": 4200
        }
        used_time = xee_entities.parse_used_time(used_time_dict)

        self.assertEqual(used_time.begin_date, datetime(2016, 7, 1, 0, 0, 0, 0, tzinfo=pytz.utc))
        self.assertEqual(used_time.end_date, datetime(2016, 7, 15, 12, 34, 30, 447653, tzinfo=pytz.utc))
        self.assertEqual(used_time.type, 'USED_TIME')
        self.assertEqual(used_time.value, 4200)

    def test_parse_wrong_field(self):
        used_time_dict = {
            "abc": "2016-07-01T00:00:00Z",
            "endDate": "2016-07-15T12:34:30.447653Z",
            "type": "USED_TIME",
            "value": 4200
        }
        try:
            used_time = xee_entities.parse_used_time(used_time_dict)
        except ParseException as err:
            self.assertIsNotNone(err)

    def test_parse_missing_field(self):
        used_time_dict = {
            "endDate": "2016-07-15T12:34:30.447653Z",
            "type": "USED_TIME",
            "value": 4200
        }
        try:
            used_time = xee_entities.parse_used_time(used_time_dict)
        except ParseException as err:
            self.assertIsNotNone(err)

class TestMileageParser(unittest.TestCase):
    def test_parse_ok(self):
        mileage_dict = {
            "beginDate": "2016-07-01T00:00:00Z",
            "endDate": "2016-07-15T12:34:30.447653Z",
            "type": "MILEAGE",
            "value": 7.65
        }
        mileage = xee_entities.parse_mileage(mileage_dict)

        self.assertEqual(mileage.begin_date, datetime(2016, 7, 1, 0, 0, 0, 0, tzinfo=pytz.utc))
        self.assertEqual(mileage.end_date, datetime(2016, 7, 15, 12, 34, 30, 447653, tzinfo=pytz.utc))
        self.assertEqual(mileage.type, 'MILEAGE')
        self.assertEqual(mileage.value, 7.65)

    def test_parse_wrong_field(self):
        mileage_dict = {
            "abc": "2016-07-01T00:00:00Z",
            "endDate": "2016-07-15T12:34:30.447653Z",
            "type": "MILEAGE",
            "value": 7.65
        }
        try:
            mileage = xee_entities.parse_mileage(mileage_dict)
        except ParseException as err:
            self.assertIsNotNone(err)

    def test_parse_missing_field(self):
        mileage_dict = {
            "endDate": "2016-07-15T12:34:30.447653Z",
            "type": "MILEAGE",
            "value": 7.65
        }
        try:
            mileage = xee_entities.parse_mileage(mileage_dict)
        except ParseException as err:
            self.assertIsNotNone(err)

class TestTripStatParser(unittest.TestCase):
    def test_parse_ok(self):
        stat_dict = {
            "type": "MILEAGE",
            "value": 7.65
        }
        stat = xee_entities.parse_trip_stat(stat_dict)

        self.assertEqual(stat.type, 'MILEAGE')
        self.assertEqual(stat.value, 7.65)

    def test_parse_wrong_field(self):
        stat_dict = {
            "ktype": "USED_TIME",
            "value": 7.65
        }
        try:
            stat = xee_entities.parse_trip_stat(stat_dict)
        except ParseException as err:
            self.assertIsNotNone(err)

    def test_parse_missing_field(self):
        stat_dict = {
            "value": 7.65
        }
        try:
            stat = xee_entities.parse_trip_stat(stat_dict)
        except ParseException as err:
            self.assertIsNotNone(err)

class TestCompatParser(unittest.TestCase):
    def test_parse_ok(self):
        compat_dict = {
            "signalsAvailable": [
                {
                    "name": "Odometer",
                    "reliability": None
                },
                {
                    "name": "FuelLevel",
                    "reliability": "incremental"
                }
            ],
            "signalsUnavailable": [
                {
                    "name": "VehiculeSpeed",
                    "reliability": None
                },
                {
                    "name": "EngineSpeed",
                    "reliability": None
                }
            ]
        }
        compat = xee_entities.parse_availability(compat_dict)

        self.assertEqual(len(compat.available), 2)
        self.assertEqual(len(compat.unavailable), 2)

    def test_parse_wrong_field(self):
        compat_dict = {
            "abd": [
                {
                    "name": "Odometer",
                    "reliability": None
                },
                {
                    "name": "FuelLevel",
                    "reliability": "incremental"
                }
            ],
            "signalsUnavailable": [
                {
                    "name": "VehiculeSpeed",
                    "reliability": None
                },
                {
                    "name": "EngineSpeed",
                    "reliability": None
                }
            ]
        }
        try:
            compat = xee_entities.parse_availability(compat_dict)
        except ParseException as err:
            self.assertIsNotNone(err)

    def test_parse_wrong_field_within_dict(self):
        compat_dict = {
            "signalsAvailable": [
                {
                    "a": "Odometer",
                    "adbcs": None
                },
                {
                    "name": "FuelLevel",
                    "reliability": "incremental"
                }
            ],
            "signalsUnavailable": [
                {
                    "name": "VehiculeSpeed",
                },
                {
                    "name": "EngineSpeed",
                    "reliability": None
                }
            ]
        }
        try:
            compat = xee_entities.parse_availability(compat_dict)
        except ParseException as err:
            self.assertIsNotNone(err)

    def test_parse_missing_field(self):
        compat_dict = {
            "signalsUnavailable": [
                {
                    "name": "VehiculeSpeed",
                    "reliability": None
                },
                {
                    "name": "EngineSpeed",
                    "reliability": None
                }
            ]
        }
        try:
            compat = xee_entities.parse_availability(compat_dict)
        except ParseException as err:
            self.assertIsNotNone(err)