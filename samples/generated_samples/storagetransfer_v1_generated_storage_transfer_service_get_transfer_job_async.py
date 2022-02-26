# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
#
# Generated code. DO NOT EDIT!
#
# Snippet for GetTransferJob
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-storage-transfer


# [START storagetransfer_v1_generated_StorageTransferService_GetTransferJob_async]
from google.cloud import storage_transfer_v1


async def sample_get_transfer_job():
    # Create a client
    client = storage_transfer_v1.StorageTransferServiceAsyncClient()

    # Initialize request argument(s)
    request = storage_transfer_v1.GetTransferJobRequest(
        job_name="job_name_value",
        project_id="project_id_value",
    )

    # Make the request
    response = await client.get_transfer_job(request=request)

    # Handle the response
    print(response)

# [END storagetransfer_v1_generated_StorageTransferService_GetTransferJob_async]