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
import os
from locust import FastHttpUser, TaskSet, task

# [START locust_test_task]


class MetricsTaskSet(TaskSet):
    _deviceid = None
    token = None
    latitude = "40.7738794"
    longitude = "-73.975149"
    origin = "Flushing Ave and Vanderbilt Ave"
    destination = "Vernon Blvd and 47 Rd"

    def on_start(self):
        self._deviceid = str(uuid.uuid4())
        self.token = os.getenv("TOKEN", "NULL")

    @task
    def get_station(self):
        self.client.get(
            "/station",
            name="/station",
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
            name="/routes/station",
            headers={
                "accept": "application/json",
            },
        )

    @task
    def get_route(self):
        station_origin = self.origin
        station_destination = self.destination
        self.client.get(
            f"/routes?origin={station_origin}&destination={station_destination}",
            name="/routes",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {self.token}",
            },
        )

    @task
    def get_history(self):
        self.client.get(
            "/get_history",
            name="/get_history",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {self.token}",
            },
        )


class MetricsLocust(FastHttpUser):
    tasks = {MetricsTaskSet}


# [END locust_test_task]
