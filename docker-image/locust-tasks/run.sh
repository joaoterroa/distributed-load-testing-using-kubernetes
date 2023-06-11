#!/bin/bash

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


LOCUST="/usr/local/bin/locust"
LOCUS_OPTS="-f /locust-tasks/tasks.py --host=$TARGET_HOST"
LOCUST_MODE=${LOCUST_MODE:-standalone}
sudo apt update
sudo apt install jq -y
ACCESS_TOKEN=$(curl --request POST \
    --url 'https://cn-fastapi.eu.auth0.com/oauth/token' \
    --header 'content-type: application/x-www-form-urlencoded' \
    --data grant_type=password \
    --data username=locust-testing@gmail.com \
    --data 'password=Locust123' \
    --data audience=https://cn-fastapi.com \
    --data 'scope=openid profile email' \
    --data 'client_id=mcB5TZfpzDxCmtX4KKMVQsq7V6Lt9gUD' \
    --data client_secret=M9448pplh5s3DGCnCx8Yy3sCpuPFo5EWTxk0JeSKLdFnehdwlvMu5gem8RzMHIcI | jq -r '.access_token'
)
export TOKEN="$ACCESS_TOKEN"

if [[ "$LOCUST_MODE" = "master" ]]; then
    LOCUS_OPTS="$LOCUS_OPTS --master"
elif [[ "$LOCUST_MODE" = "worker" ]]; then
    LOCUS_OPTS="$LOCUS_OPTS --slave --master-host=$LOCUST_MASTER"
fi

echo "$LOCUST $LOCUS_OPTS"

$LOCUST $LOCUS_OPTS