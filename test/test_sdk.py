#!/usr/bin/env python
# coding: utf8
import unittest

import responses
import pytz

from xee.exceptions import APIException
from xee.sdk import Xee
from datetime import datetime

xee = Xee('toto', 'tata', 'tut')
host = xee.host
compat_host = xee.compat_host


class TestAuthFromAuthorizationCode(unittest.TestCase):
    @responses.activate
    def test_access_token_from_authorization_code_ok(self):
        # Mock https://github.com/xee-lab/xee-api-docs/blob/master/api/api/v3/auth/access_token.md
        responses.add(responses.POST, host + "/auth/access_token",
                      json={
                          "access_token": "22fe0c13e995da4a44a63a7ff549badb5d337a42bf80f17424482e35d4cca91a",
                          "expires_at": 1382962374,
                          "expires_in": 3600,
                          "refresh_token": "8eb667707535655f2d9e14fc6491a59f6e06f2e73170761259907d8de186b6a1",
                          "token_type": "bearer"
                      },
                      status=200)
        token, err = xee.get_token_from_code("fake_code")
        self.assertEqual(token.access_token,
                         '22fe0c13e995da4a44a63a7ff549badb5d337a42bf80f17424482e35d4cca91a')
        self.assertEqual(token.refresh_token,
                         '8eb667707535655f2d9e14fc6491a59f6e06f2e73170761259907d8de186b6a1')


class TestAuthFromRefreshToken(unittest.TestCase):
    @responses.activate
    def test_access_token_from_refresh_token_ok(self):
        # Mock https://github.com/xee-lab/xee-api-docs/blob/master/api/api/v3/auth/access_token.md
        responses.add(responses.POST, host + "/auth/access_token",
                      json={
                          "access_token": "22fe0c13e995da4a44a63a7ff549badb5d337a42bf80f17424482e35d4cca91a",
                          "expires_at": 1382962374,
                          "expires_in": 3600,
                          "refresh_token": "8eb667707535655f2d9e14fc6491a59f6e06f2e73170761259907d8de186b6a1",
                          "token_type": "bearer"
                      },
                      status=200)
        token, err = xee.get_token_from_refresh_token("fake_refresh_token")
        self.assertEqual(token.access_token,
                         '22fe0c13e995da4a44a63a7ff549badb5d337a42bf80f17424482e35d4cca91a')
        self.assertEqual(token.refresh_token,
                         '8eb667707535655f2d9e14fc6491a59f6e06f2e73170761259907d8de186b6a1')


class TestUser(unittest.TestCase):
    @responses.activate
    def test_get_user_ok(self):
        # Mock https://github.com/xee-lab/xee-api-docs/blob/master/api/api/v3/users/me.md
        responses.add(responses.GET, host + "/users/me",
                      json={
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
                      },
                      status=200)
        user, err = xee.get_user("fake_access_token")
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

    @responses.activate
    def test_get_user_403(self):
        responses.add(responses.GET, host + "/users/me",
                      json=
                      [
                          {
                              'type': 'AUTHORIZATION_ERROR',
                              'message': "Token does not have the required scope",
                              'tip': "Add the users_read scope to your app scopes and reconnect the user"
                          }
                      ],
                      status=403)
        user, err = xee.get_user("oops")
        self.assertIsNone(user)
        self.assertEqual(err, APIException(
            'AUTHORIZATION_ERROR',
            "Token does not have the required scope",
            "Add the users_read scope to your app scopes and reconnect the user"))


class TestCars(unittest.TestCase):
    @responses.activate
    def test_get_cars_list_ok(self):
        # Mock https://github.com/xee-lab/xee-api-docs/blob/master/api/api/v3/users/me.md
        responses.add(responses.GET, host + "/users/me/cars",
                      json=[
                          {
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
                      ],
                      status=200)
        cars, err = xee.get_cars("fake_access_token")
        self.assertEqual(len(cars), 1)
        self.assertEqual(cars[0].id, 1337)
        self.assertEqual(cars[0].name, 'Mark-42')
        self.assertEqual(cars[0].make, 'Mark')
        self.assertEqual(cars[0].model, '42')
        self.assertEqual(cars[0].year, 2014)
        self.assertEqual(cars[0].number_plate, 'M-42-TS')
        self.assertEqual(cars[0].device_id, 'E133742015')
        self.assertEqual(cars[0].cardb_id, 210)

    @responses.activate
    def test_get_cars_list_empty(self):
        # Mock https://github.com/xee-lab/xee-api-docs/blob/master/api/api/v3/users/me/cars.md
        responses.add(responses.GET, host + "/users/me/cars",
                      json=[],
                      status=200)
        cars, err = xee.get_cars("fake_access_token")
        expected = []
        self.assertListEqual(cars, expected)

    @responses.activate
    def test_get_car(self):
        # Mock https://github.com/xee-lab/xee-api-docs/blob/master/api/api/v3/cars/car_id.md
        responses.add(responses.GET, host + "/cars/1337",
                      json={
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
                      },
                      status=200)
        car, err = xee.get_car(1337, "fake_access_token")
        self.assertEqual(car.id, 1337)
        self.assertEqual(car.name, 'Mark-42')
        self.assertEqual(car.make, 'Mark')
        self.assertEqual(car.model, '42')
        self.assertEqual(car.year, 2014)
        self.assertEqual(car.number_plate, 'M-42-TS')
        self.assertEqual(car.device_id, 'E133742015')
        self.assertEqual(car.cardb_id, 210)

    @responses.activate
    def test_get_cars_scope_403(self):
        responses.add(responses.GET, host + "/users/me/cars",
                      json=
                      [
                          {
                              'type': 'AUTHORIZATION_ERROR',
                              'message': "Token does not have the required scope",
                              'tip': "Add the cars_read scope to your app scopes and reconnect the user"
                          }
                      ],
                      status=403)
        cars, err = xee.get_cars("oops")
        self.assertIsNone(cars)
        self.assertEqual(err, APIException(
            'AUTHORIZATION_ERROR',
            "Token does not have the required scope",
            "Add the cars_read scope to your app scopes and reconnect the user"))

    @responses.activate
    def test_get_cars_access_403(self):
        responses.add(responses.GET, host + "/users/me/cars",
                      json=
                      [
                          {
                              'type': 'AUTHORIZATION_ERROR',
                              'message': "Token can't access this user",
                              'tip': "Make sure the trip belongs to the user you asked for"
                          }
                      ],
                      status=403)
        cars, err = xee.get_cars("oops")
        self.assertIsNone(cars)
        self.assertEqual(err, APIException(
            'AUTHORIZATION_ERROR',
            "Token can't access this user",
            "Make sure the trip belongs to the user you asked for"))

    @responses.activate
    def test_get_cars_404(self):
        responses.add(responses.GET, host + "/users/me/cars",
                      json=
                      [
                          {
                              'type': 'PARAMETERS_ERROR',
                              'message': "User not found",
                              'tip': "Please check that the user exists, looks like it does not"
                          }
                      ],
                      status=404)
        cars, err = xee.get_cars("oops")
        self.assertIsNone(cars)
        self.assertEqual(err, APIException(
            'PARAMETERS_ERROR',
            "User not found",
            "Please check that the user exists, looks like it does not"))


class TestStats(unittest.TestCase):
    @responses.activate
    def test_get_used_time_no_params(self):
        # Mock https://github.com/xee-lab/xee-api-docs/blob/master/api/api/v3/cars/stats/usedtime.md
        responses.add(responses.GET, host + "/cars/1337/stats/usedtime",
                      json={
                          "beginDate": "2016-07-01T00:00:00Z",
                          "endDate": "2016-07-15T12:34:30.854Z",
                          "type": "USED_TIME",
                          "value": 4200
                      },
                      status=200)
        stat, err = xee.get_used_time(1337, "fake_access_token")
        self.assertEqual(stat.begin_date, datetime(2016, 7, 1, 0, 0, 0, 0, tzinfo=pytz.utc))
        self.assertEqual(stat.end_date,
                         datetime(2016, 7, 15, 12, 34, 30, 854000, tzinfo=pytz.utc))
        self.assertEqual(stat.type, "USED_TIME")
        self.assertEqual(stat.value, 4200)

    @responses.activate
    def test_get_mileage_no_params(self):
        # Mock https://github.com/xee-lab/xee-api-docs/blob/master/api/api/v3/cars/stats/mileage.md
        responses.add(responses.GET, host + "/cars/1337/stats/mileage",
                      json={
                          "beginDate": "2016-07-01T00:00:00Z",
                          "endDate": "2016-07-15T12:34:30.854Z",
                          "type": "MILEAGE",
                          "value": 17.50
                      },
                      status=200)
        stat, err = xee.get_mileage(1337, "fake_access_token")
        self.assertEqual(stat.begin_date, datetime(2016, 7, 1, 0, 0, 0, 0, tzinfo=pytz.utc))
        self.assertEqual(stat.end_date,
                         datetime(2016, 7, 15, 12, 34, 30, 854000, tzinfo=pytz.utc))
        self.assertEqual(stat.type, "MILEAGE")
        self.assertEqual(stat.value, 17.50)


class TestSignals(unittest.TestCase):
    @responses.activate
    def test_get_signals_no_params(self):
        # Mock https://github.com/xee-lab/xee-api-docs/blob/master/api/api/v3/cars/signals.md
        responses.add(responses.GET, host + "/cars/1337/signals",
                      json=[
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
                      ],
                      status=200)
        signals, err = xee.get_signals(1337, "fake_access_token")
        self.assertEqual(len(signals), 2)
        self.assertEqual(signals[0].name, 'LockSts')
        self.assertEqual(signals[0].value, 0.0)
        self.assertEqual(signals[0].date, datetime(2016, 3, 1, 2, 24, 24, 0, tzinfo=pytz.utc))
        self.assertEqual(signals[1].name, 'Odometer')
        self.assertEqual(signals[1].value, 34512.1)
        self.assertEqual(signals[1].date, datetime(2016, 3, 1, 2, 24, 27, 116000, tzinfo=pytz.utc))

    @responses.activate
    def test_get_signals_empty(self):
        # Mock https://github.com/xee-lab/xee-api-docs/blob/master/api/api/v3/cars/signals.md
        responses.add(responses.GET, host + "/cars/1337/signals",
                      json=[],
                      status=200)
        signals, err = xee.get_signals(1337, "fake_access_token")
        expected = []
        self.assertListEqual(signals, expected)


class TestLocations(unittest.TestCase):
    @responses.activate
    def test_get_locations_no_params(self):
        # Mock https://github.com/xee-lab/xee-api-docs/blob/master/api/api/v3/cars/locations.md
        responses.add(responses.GET, host + "/cars/1337/locations",
                      json=[
                          {
                              "latitude": 50.67815,
                              "longitude": 3.208155,
                              "altitude": 31.8,
                              "satellites": 4,
                              "heading": 167,
                              "date": "2016-03-01T02:24:20.000000+00:00"
                          }
                      ],
                      status=200)
        locations, err = xee.get_locations(1337, "fake_access_token")
        self.assertEqual(len(locations), 1)
        self.assertEqual(locations[0].latitude, 50.67815)
        self.assertEqual(locations[0].longitude, 3.208155)
        self.assertEqual(locations[0].altitude, 31.8)
        self.assertEqual(locations[0].satellites, 4)
        self.assertEqual(locations[0].heading, 167)
        self.assertEqual(locations[0].date, datetime(2016, 3, 1, 2, 24, 20, 0, tzinfo=pytz.utc))

    @responses.activate
    def test_get_locations_empty(self):
        # Mock https://github.com/xee-lab/xee-api-docs/blob/master/api/api/v3/cars/locations.md
        responses.add(responses.GET, host + "/cars/1337/locations",
                      json=[],
                      status=200)
        locations, err = xee.get_locations(1337, "fake_access_token")
        expected = []
        self.assertListEqual(locations, expected)


class TestTrips(unittest.TestCase):
    @responses.activate
    def test_get_trips_no_params(self):
        # Mock https://github.com/xee-lab/xee-api-docs/blob/master/api/api/v3/cars/trips.md
        responses.add(responses.GET, host + "/cars/1337/trips",
                      json=[
                          {
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
                      ],
                      status=200)
        trips, err = xee.get_trips(1337, "fake_access_token")
        self.assertEqual(len(trips), 1)
        self.assertEqual(trips[0].id, '56b43a4f051f29071f14218d')
        self.assertDictEqual(trips[0].begin_location._asdict(), {
            "latitude": 50.6817,
            "longitude": 3.08202,
            "altitude": 2,
            "heading": 0,
            "satellites": 1,
            "date": datetime(2016, 1, 29, 18, 36, 17, tzinfo=pytz.utc),
        })
        self.assertDictEqual(trips[0].end_location._asdict(), {
            "latitude": 50.6817,
            "longitude": 3.08202,
            "altitude": 2,
            "heading": 0,
            "satellites": 1,
            "date": datetime(2016, 1, 29, 18, 36, 17, tzinfo=pytz.utc),
        })
        self.assertEqual(trips[0].begin_date, datetime(2016, 1, 29, 18, 39, 17, tzinfo=pytz.utc))
        self.assertEqual(trips[0].end_date, datetime(2016, 1, 29, 19, 15, 15, tzinfo=pytz.utc))

    @responses.activate
    def test_get_trips_empty(self):
        # Mock in https://github.com/xee-lab/xee-api-docs/blob/master/api/api/v3/cars/trips.md
        responses.add(responses.GET, host + "/cars/1337/trips",
                      json=[],
                      status=200)
        trips, err = xee.get_trips(1337, "fake_access_token")
        expected = []
        self.assertListEqual(trips, expected)


class TestTripLocations(unittest.TestCase):
    @responses.activate
    def test_get_locations(self):
        # Mock https://github.com/xee-lab/xee-api-docs/blob/master/api/v3/trips
        # /56b43a4f051f29071f14218d/locations.md
        responses.add(responses.GET, host + "/trips/56b43a4f051f29071f14218d/locations",
                      json=[
                          {
                              "latitude": 50.67815,
                              "longitude": 3.208155,
                              "altitude": 31.8,
                              "satellites": 4,
                              "heading": 167,
                              "date": "2016-03-01T02:24:20.000000+00:00"
                          }
                      ],
                      status=200)
        locations, err = xee.get_trip_locations("56b43a4f051f29071f14218d", "fake_access_token")
        self.assertEqual(len(locations), 1)
        self.assertEqual(locations[0].latitude, 50.67815)
        self.assertEqual(locations[0].longitude, 3.208155)
        self.assertEqual(locations[0].altitude, 31.8)
        self.assertEqual(locations[0].satellites, 4)
        self.assertEqual(locations[0].heading, 167)
        self.assertEqual(locations[0].date, datetime(2016, 3, 1, 2, 24, 20, 0, tzinfo=pytz.utc))

    @responses.activate
    def test_get_locations_empty(self):
        # Mock https://github.com/xee-lab/xee-api-docs/blob/master/api/api/v3/cars/locations.md
        responses.add(responses.GET, host + "/trips/56b43a4f051f29071f14218d/locations",
                      json=[],
                      status=200)
        locations, err = xee.get_trip_locations("56b43a4f051f29071f14218d", "fake_access_token")
        expected = []
        self.assertListEqual(locations, expected)


class TestTripSignals(unittest.TestCase):
    @responses.activate
    def test_get_signals(self):
        # Mock https://github.com/xee-lab/xee-api-docs/blob/master/api/v3/trips
        # /56b43a4f051f29071f14218d/signals.md
        responses.add(responses.GET, host + "/trips/56b43a4f051f29071f14218d/signals",
                      json=[
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
                      ],
                      status=200)
        signals, err = xee.get_trip_signals("56b43a4f051f29071f14218d", "fake_access_token")
        self.assertEqual(len(signals), 2)
        self.assertEqual(signals[0].name, 'LockSts')
        self.assertEqual(signals[0].value, 0.0)
        self.assertEqual(signals[0].date, datetime(2016, 3, 1, 2, 24, 24, 0, tzinfo=pytz.utc))
        self.assertEqual(signals[1].name, 'Odometer')
        self.assertEqual(signals[1].value, 34512.1)
        self.assertEqual(signals[1].date, datetime(2016, 3, 1, 2, 24, 27, 116000, tzinfo=pytz.utc))

    @responses.activate
    def test_get_signals_empty(self):
        # Mock https://github.com/xee-lab/xee-api-docs/blob/master/api/v3/trips
        # /56b43a4f051f29071f14218d/signals.md
        responses.add(responses.GET, host + "/trips/56b43a4f051f29071f14218d/signals",
                      json=[],
                      status=200)
        locations, err = xee.get_trip_signals("56b43a4f051f29071f14218d", "fake_access_token")
        expected = []
        self.assertListEqual(locations, expected)


class TestTripStats(unittest.TestCase):
    @responses.activate
    def test_get_stats(self):
        # Mock https://github.com/xee-lab/xee-api-docs/blob/master/api/api/v3/trips/trip_id/stats.md
        responses.add(responses.GET, host + "/trips/56b43a4f051f29071f14218d/stats",
                      json=[
                          {
                              "type": "MILEAGE",
                              "value": 5.800642496450446
                          },
                          {
                              "type": "USED_TIME",
                              "value": 980
                          }
                      ],
                      status=200)
        stats, err = xee.get_trip_stats("56b43a4f051f29071f14218d", "fake_access_token")
        self.assertEqual(len(stats), 2)
        self.assertEqual(stats[0].type, 'MILEAGE')
        self.assertEqual(stats[0].value, 5.800642496450446)
        self.assertEqual(stats[1].type, 'USED_TIME')
        self.assertEqual(stats[1].value, 980)

    @responses.activate
    def test_get_stats_empty(self):
        # Mock https://github.com/xee-lab/xee-api-docs/blob/master/api/v3/trips
        # /56b43a4f051f29071f14218d/signals.md
        responses.add(responses.GET, host + "/trips/56b43a4f051f29071f14218d/stats",
                      json=[],
                      status=200)
        stats, err = xee.get_trip_stats("56b43a4f051f29071f14218d", "fake_access_token")
        expected = []
        self.assertListEqual(stats, expected)

    @responses.activate
    def test_get_stats_trip_does_not_exists(self):
        # Mock https://github.com/xee-lab/xee-api-docs/blob/master/api/v3/trips
        # /56b43a4f051f29071f14218d/signals.md
        responses.add(responses.GET, host + "/trips/56b43a4f051f29071f14218d/stats",
                      json=[
                          {
                              "type": "PARAMETERS_ERROR",
                              "message": "Trip not found",
                              "tip": "Please check that the trip exists, looks like it does not"
                          }
                      ],
                      status=404)
        stats, err = xee.get_trip_stats("56b43a4f051f29071f14218d", "fake_access_token")
        self.assertIsNotNone(err)
        self.assertEqual(err.type, 'PARAMETERS_ERROR')
        self.assertEqual(err.message, "Trip not found")
        self.assertEqual(err.tip, "Please check that the trip exists, looks like it does not")


class TestTripMileage(unittest.TestCase):
    @responses.activate
    def test_get_mileage(self):
        # Mock https://github.com/xee-lab/xee-api-docs/blob/master/api/api/v3/trips/trip_id/stats
        # /mileage.md
        responses.add(responses.GET, host + "/trips/56b43a4f051f29071f14218d/stats/mileage",
                      json={
                          "type": "MILEAGE",
                          "value": 5.800642496450446
                      },
                      status=200)
        mileage, err = xee.get_trip_mileage("56b43a4f051f29071f14218d", "fake_access_token")
        self.assertEqual(mileage.type, 'MILEAGE')
        self.assertEqual(mileage.value, 5.800642496450446)

    @responses.activate
    def test_get_mileage_not_exists(self):
        responses.add(responses.GET, host + "/trips/56b43a4f051f29071f14218d/stats/mileage",
                      json=[
                          {
                              "type": "PARAMETERS_ERROR",
                              "message": "Statistics not found",
                              "tip": "Please check that the trip exists and data are present, " +
                                     "looks like it does not"
                          }
                      ],
                      status=404)
        mileage, err = xee.get_trip_mileage("56b43a4f051f29071f14218d", "fake_access_token")
        self.assertIsNotNone(err)
        self.assertEqual(err.type, 'PARAMETERS_ERROR')
        self.assertEqual(err.message, "Statistics not found")
        self.assertEqual(err.tip, "Please check that the trip exists and data are present, " +
                         "looks like it does not")

    @responses.activate
    def test_get_mileage_trip_does_not_exists(self):
        responses.add(responses.GET, host + "/trips/56b43a4f051f29071f14218d/stats/mileage",
                      json=[
                          {
                              "type": "PARAMETERS_ERROR",
                              "message": "Trip not found",
                              "tip": "Please check that the trip exists, looks like it does not"
                          }
                      ],
                      status=404)
        stats, err = xee.get_trip_mileage("56b43a4f051f29071f14218d", "fake_access_token")
        self.assertIsNotNone(err)
        self.assertEqual(err.type, 'PARAMETERS_ERROR')
        self.assertEqual(err.message, "Trip not found")
        self.assertEqual(err.tip, "Please check that the trip exists, looks like it does not")


class TestTripDuration(unittest.TestCase):
    @responses.activate
    def test_get_duration(self):
        # Mock https://github.com/xee-lab/xee-api-docs/blob/master/api/api/v3/trips/trip_id/stats
        # /usedtime.md
        responses.add(responses.GET, host + "/trips/56b43a4f051f29071f14218d/stats/usedtime",
                      json={
                          "type": "USED_TIME",
                          "value": 1271
                      },
                      status=200)
        duration, err = xee.get_trip_duration("56b43a4f051f29071f14218d", "fake_access_token")
        self.assertEqual(duration.type, 'USED_TIME')
        self.assertEqual(duration.value, 1271)

    @responses.activate
    def test_get_duration_not_exists(self):
        responses.add(responses.GET, host + "/trips/56b43a4f051f29071f14218d/stats/usedtime",
                      json=[
                          {
                              "type": "PARAMETERS_ERROR",
                              "message": "Statistics not found",
                              "tip": "Please check that the trip exists and data are present, " +
                                     "looks like it does not"
                          }
                      ],
                      status=404)
        mileage, err = xee.get_trip_duration("56b43a4f051f29071f14218d", "fake_access_token")
        self.assertIsNotNone(err)
        self.assertEqual(err.type, 'PARAMETERS_ERROR')
        self.assertEqual(err.message, "Statistics not found")
        self.assertEqual(err.tip, "Please check that the trip exists and data are present, " +
                         "looks like it does not")

    @responses.activate
    def test_get_duration_trip_does_not_exists(self):
        responses.add(responses.GET, host + "/trips/56b43a4f051f29071f14218d/stats/usedtime",
                      json=[
                          {
                              "type": "PARAMETERS_ERROR",
                              "message": "Trip not found",
                              "tip": "Please check that the trip exists, looks like it does not"
                          }
                      ],
                      status=404)
        stats, err = xee.get_trip_duration("56b43a4f051f29071f14218d", "fake_access_token")
        self.assertIsNotNone(err)
        self.assertEqual(err.type, 'PARAMETERS_ERROR')
        self.assertEqual(err.message, "Trip not found")
        self.assertEqual(err.tip, "Please check that the trip exists, looks like it does not")


class TestCarCompat(unittest.TestCase):
    @responses.activate
    def test_get_compat(self):
        # Mock https://github.com/xee-lab/xee-api-docs/blob/master/api/compat/v1/cardb/cardbId.md
        responses.add(responses.GET, compat_host + "/cardb/123",
                      json={
                            "signalsAvailable": 
                            [
                                {
                                    "name": "Odometer",
                                    "reliability": None
                                },
                                {
                                    "name": "FuelLevel",
                                    "reliability": "incremental"
                                }
                            ],
                            "signalsUnavailable": 
                            [
                                {
                                    "name": "VehiculeSpeed",
                                    "reliability": None
                                },
                                {
                                    "name": "EngineSpeed",
                                    "reliability": None
                                }
                            ]
                        },
                      status=200)
        compat, err = xee.get_car_compat("123")
        self.assertEqual(len(compat.available), 2)
        self.assertEqual(compat.available[0].name, 'Odometer')
        self.assertEqual(compat.available[0].reliability, None)
        self.assertEqual(compat.available[1].name, 'FuelLevel')
        self.assertEqual(compat.available[1].reliability, 'incremental')
        self.assertEqual(len(compat.unavailable), 2)
        self.assertEqual(compat.unavailable[0].name, 'VehiculeSpeed')
        self.assertEqual(compat.unavailable[0].reliability, None)
        self.assertEqual(compat.unavailable[1].name, 'EngineSpeed')
        self.assertEqual(compat.unavailable[1].reliability, None)

    @responses.activate
    def test_cardb_not_correct(self):
        responses.add(responses.GET, compat_host + "/cardb/123",
                      json=[
                          {
                              "type": "PARAMETERS_ERROR",
                              "message": "Unable to parse cardb parameter",
                              "tip": "Please check if carDb parameter you have set is a int"
                          }
                      ],
                      status=400)
        compat, err = xee.get_car_compat("123")
        self.assertIsNotNone(err)
        self.assertEqual(err.type, 'PARAMETERS_ERROR')
        self.assertEqual(err.message, "Unable to parse cardb parameter")
        self.assertEqual(err.tip, "Please check if carDb parameter you have set is a int")

    @responses.activate
    def test_cardb_not_found(self):
        responses.add(responses.GET, compat_host + "/cardb/123",
                      json=[
                          {
                              "type": "NOT_FOUND",
                              "message": "CarDb not found",
                              "tip": "The carDb associated with KType doesn't exist. Please try with an other KType."
                          }
                      ],
                      status=404)
        compat, err = xee.get_car_compat("123")
        self.assertIsNotNone(err)
        self.assertEqual(err.type, 'NOT_FOUND')
        self.assertEqual(err.message, "CarDb not found")
        self.assertEqual(err.tip, "The carDb associated with KType doesn't exist. Please try with an other KType.")


class TestErrors(unittest.TestCase):
    @responses.activate
    def test_400(self):
        return

    def test_401(self):
        return

    def test_403(self):
        return

    def test_404(self):
        return

    def test_416(self):
        return
