#!/usr/bin/env python

# Copyright 2022 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid
from locust import FastHttpUser, TaskSet, task
import requests
import json

# [START locust_test_task]

url = "https://cn-fastapi.eu.auth0.com/oauth/token"
headers = {"content-type": "application/x-www-form-urlencoded"}
data = {
    "grant_type": "password",
    "username": "locust-testing@gmail.com",
    "password": "Locust123",
    "audience": "https://cn-fastapi.com",
    "scope": "openid profile email",
    "client_id": "mcB5TZfpzDxCmtX4KKMVQsq7V6Lt9gUD",
    "client_secret": "M9448pplh5s3DGCnCx8Yy3sCpuPFo5EWTxk0JeSKLdFnehdwlvMu5gem8RzMHIcI",
}

response = requests.post(url, headers=headers, data=data)

response_dict = json.loads(response.text)
access_token = response_dict["access_token"]


class MetricsTaskSet(TaskSet):
    _deviceid = None
    latitude = "40.7738794"
    longitude = "-73.975149"
    origin = "Flushing Ave and Vanderbilt Ave"
    destination = "Vernon Blvd and 47 Rd"

    def on_start(self):
        self._deviceid = str(uuid.uuid4())
        self.access_token = access_token

    @task
    def get_station(self):
        self.client.get(
            "/station",
            headers={
                "accept": "application/json",
            },
        )

    @task
    def get_routes_station(self):
        user_latitude = self.latitude
        user_longitude = self.longitude
        self.client.get(
            f"/routes/station?user_latitude={user_latitude}&user_longitude={user_longitude}",
            headers={
                "accept": "application/json",
            },
        )

    @task
    def get_route(self):
        station_origin = requests.utils.quote(self.origin)
        station_destination = requests.utils.quote(self.destination)
        self.client.get(
            f"/routes?origin={station_origin}&destination={station_destination}",
            headers={
                "authorization": f"Bearer {self.access_token}",
            },
            verify=False,
        )

    @task
    def get_history(self):
        self.client.get(
            "/get_history",
            headers={
                "authorization": f"Bearer {self.access_token}",
            },
            verify=False,
        )


class MetricsLocust(FastHttpUser):
    tasks = {MetricsTaskSet}


# [END locust_test_task]
