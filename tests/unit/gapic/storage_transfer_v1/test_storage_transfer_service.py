# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
import os

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock
except ImportError:
    import mock

import math

from google.api_core import (
    future,
    gapic_v1,
    grpc_helpers,
    grpc_helpers_async,
    operation,
    operations_v1,
    path_template,
)
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import operation_async  # type: ignore
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import date_pb2  # type: ignore
from google.type import timeofday_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest

from google.cloud.storage_transfer_v1.services.storage_transfer_service import (
    StorageTransferServiceAsyncClient,
    StorageTransferServiceClient,
    pagers,
    transports,
)
from google.cloud.storage_transfer_v1.types import transfer, transfer_types


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert StorageTransferServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        StorageTransferServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        StorageTransferServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        StorageTransferServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        StorageTransferServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        StorageTransferServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (StorageTransferServiceClient, "grpc"),
        (StorageTransferServiceAsyncClient, "grpc_asyncio"),
    ],
)
def test_storage_transfer_service_client_from_service_account_info(
    client_class, transport_name
):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == ("storagetransfer.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.StorageTransferServiceGrpcTransport, "grpc"),
        (transports.StorageTransferServiceGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_storage_transfer_service_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (StorageTransferServiceClient, "grpc"),
        (StorageTransferServiceAsyncClient, "grpc_asyncio"),
    ],
)
def test_storage_transfer_service_client_from_service_account_file(
    client_class, transport_name
):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == ("storagetransfer.googleapis.com:443")


def test_storage_transfer_service_client_get_transport_class():
    transport = StorageTransferServiceClient.get_transport_class()
    available_transports = [
        transports.StorageTransferServiceGrpcTransport,
    ]
    assert transport in available_transports

    transport = StorageTransferServiceClient.get_transport_class("grpc")
    assert transport == transports.StorageTransferServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            StorageTransferServiceClient,
            transports.StorageTransferServiceGrpcTransport,
            "grpc",
        ),
        (
            StorageTransferServiceAsyncClient,
            transports.StorageTransferServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    StorageTransferServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(StorageTransferServiceClient),
)
@mock.patch.object(
    StorageTransferServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(StorageTransferServiceAsyncClient),
)
def test_storage_transfer_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(StorageTransferServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(StorageTransferServiceClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class(transport=transport_name)

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class(transport=transport_name)

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(
        api_audience="https://language.googleapis.com"
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            StorageTransferServiceClient,
            transports.StorageTransferServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            StorageTransferServiceAsyncClient,
            transports.StorageTransferServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            StorageTransferServiceClient,
            transports.StorageTransferServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            StorageTransferServiceAsyncClient,
            transports.StorageTransferServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    StorageTransferServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(StorageTransferServiceClient),
)
@mock.patch.object(
    StorageTransferServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(StorageTransferServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_storage_transfer_service_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize(
    "client_class", [StorageTransferServiceClient, StorageTransferServiceAsyncClient]
)
@mock.patch.object(
    StorageTransferServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(StorageTransferServiceClient),
)
@mock.patch.object(
    StorageTransferServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(StorageTransferServiceAsyncClient),
)
def test_storage_transfer_service_client_get_mtls_endpoint_and_cert_source(
    client_class,
):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            StorageTransferServiceClient,
            transports.StorageTransferServiceGrpcTransport,
            "grpc",
        ),
        (
            StorageTransferServiceAsyncClient,
            transports.StorageTransferServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_storage_transfer_service_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            StorageTransferServiceClient,
            transports.StorageTransferServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            StorageTransferServiceAsyncClient,
            transports.StorageTransferServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_storage_transfer_service_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


def test_storage_transfer_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.storage_transfer_v1.services.storage_transfer_service.transports.StorageTransferServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = StorageTransferServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            StorageTransferServiceClient,
            transports.StorageTransferServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            StorageTransferServiceAsyncClient,
            transports.StorageTransferServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_storage_transfer_service_client_create_channel_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "storagetransfer.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="storagetransfer.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        transfer.GetGoogleServiceAccountRequest,
        dict,
    ],
)
def test_get_google_service_account(request_type, transport: str = "grpc"):
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_google_service_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = transfer_types.GoogleServiceAccount(
            account_email="account_email_value",
            subject_id="subject_id_value",
        )
        response = client.get_google_service_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.GetGoogleServiceAccountRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, transfer_types.GoogleServiceAccount)
    assert response.account_email == "account_email_value"
    assert response.subject_id == "subject_id_value"


def test_get_google_service_account_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_google_service_account), "__call__"
    ) as call:
        client.get_google_service_account()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.GetGoogleServiceAccountRequest()


@pytest.mark.asyncio
async def test_get_google_service_account_async(
    transport: str = "grpc_asyncio",
    request_type=transfer.GetGoogleServiceAccountRequest,
):
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_google_service_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transfer_types.GoogleServiceAccount(
                account_email="account_email_value",
                subject_id="subject_id_value",
            )
        )
        response = await client.get_google_service_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.GetGoogleServiceAccountRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, transfer_types.GoogleServiceAccount)
    assert response.account_email == "account_email_value"
    assert response.subject_id == "subject_id_value"


@pytest.mark.asyncio
async def test_get_google_service_account_async_from_dict():
    await test_get_google_service_account_async(request_type=dict)


def test_get_google_service_account_field_headers():
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transfer.GetGoogleServiceAccountRequest()

    request.project_id = "project_id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_google_service_account), "__call__"
    ) as call:
        call.return_value = transfer_types.GoogleServiceAccount()
        client.get_google_service_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_google_service_account_field_headers_async():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transfer.GetGoogleServiceAccountRequest()

    request.project_id = "project_id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_google_service_account), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transfer_types.GoogleServiceAccount()
        )
        await client.get_google_service_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        transfer.CreateTransferJobRequest,
        dict,
    ],
)
def test_create_transfer_job(request_type, transport: str = "grpc"):
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_transfer_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = transfer_types.TransferJob(
            name="name_value",
            description="description_value",
            project_id="project_id_value",
            status=transfer_types.TransferJob.Status.ENABLED,
            latest_operation_name="latest_operation_name_value",
        )
        response = client.create_transfer_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.CreateTransferJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, transfer_types.TransferJob)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.project_id == "project_id_value"
    assert response.status == transfer_types.TransferJob.Status.ENABLED
    assert response.latest_operation_name == "latest_operation_name_value"


def test_create_transfer_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_transfer_job), "__call__"
    ) as call:
        client.create_transfer_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.CreateTransferJobRequest()


@pytest.mark.asyncio
async def test_create_transfer_job_async(
    transport: str = "grpc_asyncio", request_type=transfer.CreateTransferJobRequest
):
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_transfer_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transfer_types.TransferJob(
                name="name_value",
                description="description_value",
                project_id="project_id_value",
                status=transfer_types.TransferJob.Status.ENABLED,
                latest_operation_name="latest_operation_name_value",
            )
        )
        response = await client.create_transfer_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.CreateTransferJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, transfer_types.TransferJob)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.project_id == "project_id_value"
    assert response.status == transfer_types.TransferJob.Status.ENABLED
    assert response.latest_operation_name == "latest_operation_name_value"


@pytest.mark.asyncio
async def test_create_transfer_job_async_from_dict():
    await test_create_transfer_job_async(request_type=dict)


@pytest.mark.parametrize(
    "request_type",
    [
        transfer.UpdateTransferJobRequest,
        dict,
    ],
)
def test_update_transfer_job(request_type, transport: str = "grpc"):
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_transfer_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = transfer_types.TransferJob(
            name="name_value",
            description="description_value",
            project_id="project_id_value",
            status=transfer_types.TransferJob.Status.ENABLED,
            latest_operation_name="latest_operation_name_value",
        )
        response = client.update_transfer_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.UpdateTransferJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, transfer_types.TransferJob)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.project_id == "project_id_value"
    assert response.status == transfer_types.TransferJob.Status.ENABLED
    assert response.latest_operation_name == "latest_operation_name_value"


def test_update_transfer_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_transfer_job), "__call__"
    ) as call:
        client.update_transfer_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.UpdateTransferJobRequest()


@pytest.mark.asyncio
async def test_update_transfer_job_async(
    transport: str = "grpc_asyncio", request_type=transfer.UpdateTransferJobRequest
):
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_transfer_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transfer_types.TransferJob(
                name="name_value",
                description="description_value",
                project_id="project_id_value",
                status=transfer_types.TransferJob.Status.ENABLED,
                latest_operation_name="latest_operation_name_value",
            )
        )
        response = await client.update_transfer_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.UpdateTransferJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, transfer_types.TransferJob)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.project_id == "project_id_value"
    assert response.status == transfer_types.TransferJob.Status.ENABLED
    assert response.latest_operation_name == "latest_operation_name_value"


@pytest.mark.asyncio
async def test_update_transfer_job_async_from_dict():
    await test_update_transfer_job_async(request_type=dict)


def test_update_transfer_job_field_headers():
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transfer.UpdateTransferJobRequest()

    request.job_name = "job_name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_transfer_job), "__call__"
    ) as call:
        call.return_value = transfer_types.TransferJob()
        client.update_transfer_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "job_name=job_name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_transfer_job_field_headers_async():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transfer.UpdateTransferJobRequest()

    request.job_name = "job_name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_transfer_job), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transfer_types.TransferJob()
        )
        await client.update_transfer_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "job_name=job_name_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        transfer.GetTransferJobRequest,
        dict,
    ],
)
def test_get_transfer_job(request_type, transport: str = "grpc"):
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_transfer_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = transfer_types.TransferJob(
            name="name_value",
            description="description_value",
            project_id="project_id_value",
            status=transfer_types.TransferJob.Status.ENABLED,
            latest_operation_name="latest_operation_name_value",
        )
        response = client.get_transfer_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.GetTransferJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, transfer_types.TransferJob)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.project_id == "project_id_value"
    assert response.status == transfer_types.TransferJob.Status.ENABLED
    assert response.latest_operation_name == "latest_operation_name_value"


def test_get_transfer_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_transfer_job), "__call__") as call:
        client.get_transfer_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.GetTransferJobRequest()


@pytest.mark.asyncio
async def test_get_transfer_job_async(
    transport: str = "grpc_asyncio", request_type=transfer.GetTransferJobRequest
):
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_transfer_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transfer_types.TransferJob(
                name="name_value",
                description="description_value",
                project_id="project_id_value",
                status=transfer_types.TransferJob.Status.ENABLED,
                latest_operation_name="latest_operation_name_value",
            )
        )
        response = await client.get_transfer_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.GetTransferJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, transfer_types.TransferJob)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.project_id == "project_id_value"
    assert response.status == transfer_types.TransferJob.Status.ENABLED
    assert response.latest_operation_name == "latest_operation_name_value"


@pytest.mark.asyncio
async def test_get_transfer_job_async_from_dict():
    await test_get_transfer_job_async(request_type=dict)


def test_get_transfer_job_field_headers():
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transfer.GetTransferJobRequest()

    request.job_name = "job_name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_transfer_job), "__call__") as call:
        call.return_value = transfer_types.TransferJob()
        client.get_transfer_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "job_name=job_name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_transfer_job_field_headers_async():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transfer.GetTransferJobRequest()

    request.job_name = "job_name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_transfer_job), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transfer_types.TransferJob()
        )
        await client.get_transfer_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "job_name=job_name_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        transfer.ListTransferJobsRequest,
        dict,
    ],
)
def test_list_transfer_jobs(request_type, transport: str = "grpc"):
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_transfer_jobs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = transfer.ListTransferJobsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_transfer_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.ListTransferJobsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTransferJobsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_transfer_jobs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_transfer_jobs), "__call__"
    ) as call:
        client.list_transfer_jobs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.ListTransferJobsRequest()


@pytest.mark.asyncio
async def test_list_transfer_jobs_async(
    transport: str = "grpc_asyncio", request_type=transfer.ListTransferJobsRequest
):
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_transfer_jobs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transfer.ListTransferJobsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_transfer_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.ListTransferJobsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTransferJobsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_transfer_jobs_async_from_dict():
    await test_list_transfer_jobs_async(request_type=dict)


def test_list_transfer_jobs_pager(transport_name: str = "grpc"):
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_transfer_jobs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            transfer.ListTransferJobsResponse(
                transfer_jobs=[
                    transfer_types.TransferJob(),
                    transfer_types.TransferJob(),
                    transfer_types.TransferJob(),
                ],
                next_page_token="abc",
            ),
            transfer.ListTransferJobsResponse(
                transfer_jobs=[],
                next_page_token="def",
            ),
            transfer.ListTransferJobsResponse(
                transfer_jobs=[
                    transfer_types.TransferJob(),
                ],
                next_page_token="ghi",
            ),
            transfer.ListTransferJobsResponse(
                transfer_jobs=[
                    transfer_types.TransferJob(),
                    transfer_types.TransferJob(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_transfer_jobs(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, transfer_types.TransferJob) for i in results)


def test_list_transfer_jobs_pages(transport_name: str = "grpc"):
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_transfer_jobs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            transfer.ListTransferJobsResponse(
                transfer_jobs=[
                    transfer_types.TransferJob(),
                    transfer_types.TransferJob(),
                    transfer_types.TransferJob(),
                ],
                next_page_token="abc",
            ),
            transfer.ListTransferJobsResponse(
                transfer_jobs=[],
                next_page_token="def",
            ),
            transfer.ListTransferJobsResponse(
                transfer_jobs=[
                    transfer_types.TransferJob(),
                ],
                next_page_token="ghi",
            ),
            transfer.ListTransferJobsResponse(
                transfer_jobs=[
                    transfer_types.TransferJob(),
                    transfer_types.TransferJob(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_transfer_jobs(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_transfer_jobs_async_pager():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_transfer_jobs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            transfer.ListTransferJobsResponse(
                transfer_jobs=[
                    transfer_types.TransferJob(),
                    transfer_types.TransferJob(),
                    transfer_types.TransferJob(),
                ],
                next_page_token="abc",
            ),
            transfer.ListTransferJobsResponse(
                transfer_jobs=[],
                next_page_token="def",
            ),
            transfer.ListTransferJobsResponse(
                transfer_jobs=[
                    transfer_types.TransferJob(),
                ],
                next_page_token="ghi",
            ),
            transfer.ListTransferJobsResponse(
                transfer_jobs=[
                    transfer_types.TransferJob(),
                    transfer_types.TransferJob(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_transfer_jobs(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, transfer_types.TransferJob) for i in responses)


@pytest.mark.asyncio
async def test_list_transfer_jobs_async_pages():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_transfer_jobs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            transfer.ListTransferJobsResponse(
                transfer_jobs=[
                    transfer_types.TransferJob(),
                    transfer_types.TransferJob(),
                    transfer_types.TransferJob(),
                ],
                next_page_token="abc",
            ),
            transfer.ListTransferJobsResponse(
                transfer_jobs=[],
                next_page_token="def",
            ),
            transfer.ListTransferJobsResponse(
                transfer_jobs=[
                    transfer_types.TransferJob(),
                ],
                next_page_token="ghi",
            ),
            transfer.ListTransferJobsResponse(
                transfer_jobs=[
                    transfer_types.TransferJob(),
                    transfer_types.TransferJob(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_transfer_jobs(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        transfer.PauseTransferOperationRequest,
        dict,
    ],
)
def test_pause_transfer_operation(request_type, transport: str = "grpc"):
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.pause_transfer_operation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.pause_transfer_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.PauseTransferOperationRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_pause_transfer_operation_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.pause_transfer_operation), "__call__"
    ) as call:
        client.pause_transfer_operation()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.PauseTransferOperationRequest()


@pytest.mark.asyncio
async def test_pause_transfer_operation_async(
    transport: str = "grpc_asyncio", request_type=transfer.PauseTransferOperationRequest
):
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.pause_transfer_operation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.pause_transfer_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.PauseTransferOperationRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_pause_transfer_operation_async_from_dict():
    await test_pause_transfer_operation_async(request_type=dict)


def test_pause_transfer_operation_field_headers():
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transfer.PauseTransferOperationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.pause_transfer_operation), "__call__"
    ) as call:
        call.return_value = None
        client.pause_transfer_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_pause_transfer_operation_field_headers_async():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transfer.PauseTransferOperationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.pause_transfer_operation), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.pause_transfer_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        transfer.ResumeTransferOperationRequest,
        dict,
    ],
)
def test_resume_transfer_operation(request_type, transport: str = "grpc"):
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.resume_transfer_operation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.resume_transfer_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.ResumeTransferOperationRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_resume_transfer_operation_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.resume_transfer_operation), "__call__"
    ) as call:
        client.resume_transfer_operation()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.ResumeTransferOperationRequest()


@pytest.mark.asyncio
async def test_resume_transfer_operation_async(
    transport: str = "grpc_asyncio",
    request_type=transfer.ResumeTransferOperationRequest,
):
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.resume_transfer_operation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.resume_transfer_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.ResumeTransferOperationRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_resume_transfer_operation_async_from_dict():
    await test_resume_transfer_operation_async(request_type=dict)


def test_resume_transfer_operation_field_headers():
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transfer.ResumeTransferOperationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.resume_transfer_operation), "__call__"
    ) as call:
        call.return_value = None
        client.resume_transfer_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_resume_transfer_operation_field_headers_async():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transfer.ResumeTransferOperationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.resume_transfer_operation), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.resume_transfer_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        transfer.RunTransferJobRequest,
        dict,
    ],
)
def test_run_transfer_job(request_type, transport: str = "grpc"):
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_transfer_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.run_transfer_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.RunTransferJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_run_transfer_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_transfer_job), "__call__") as call:
        client.run_transfer_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.RunTransferJobRequest()


@pytest.mark.asyncio
async def test_run_transfer_job_async(
    transport: str = "grpc_asyncio", request_type=transfer.RunTransferJobRequest
):
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_transfer_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.run_transfer_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.RunTransferJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_run_transfer_job_async_from_dict():
    await test_run_transfer_job_async(request_type=dict)


def test_run_transfer_job_field_headers():
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transfer.RunTransferJobRequest()

    request.job_name = "job_name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_transfer_job), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.run_transfer_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "job_name=job_name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_run_transfer_job_field_headers_async():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transfer.RunTransferJobRequest()

    request.job_name = "job_name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_transfer_job), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.run_transfer_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "job_name=job_name_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        transfer.CreateAgentPoolRequest,
        dict,
    ],
)
def test_create_agent_pool(request_type, transport: str = "grpc"):
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_agent_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = transfer_types.AgentPool(
            name="name_value",
            display_name="display_name_value",
            state=transfer_types.AgentPool.State.CREATING,
        )
        response = client.create_agent_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.CreateAgentPoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, transfer_types.AgentPool)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == transfer_types.AgentPool.State.CREATING


def test_create_agent_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_agent_pool), "__call__"
    ) as call:
        client.create_agent_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.CreateAgentPoolRequest()


@pytest.mark.asyncio
async def test_create_agent_pool_async(
    transport: str = "grpc_asyncio", request_type=transfer.CreateAgentPoolRequest
):
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_agent_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transfer_types.AgentPool(
                name="name_value",
                display_name="display_name_value",
                state=transfer_types.AgentPool.State.CREATING,
            )
        )
        response = await client.create_agent_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.CreateAgentPoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, transfer_types.AgentPool)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == transfer_types.AgentPool.State.CREATING


@pytest.mark.asyncio
async def test_create_agent_pool_async_from_dict():
    await test_create_agent_pool_async(request_type=dict)


def test_create_agent_pool_field_headers():
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transfer.CreateAgentPoolRequest()

    request.project_id = "project_id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_agent_pool), "__call__"
    ) as call:
        call.return_value = transfer_types.AgentPool()
        client.create_agent_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_agent_pool_field_headers_async():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transfer.CreateAgentPoolRequest()

    request.project_id = "project_id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_agent_pool), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transfer_types.AgentPool()
        )
        await client.create_agent_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value",
    ) in kw["metadata"]


def test_create_agent_pool_flattened():
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_agent_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = transfer_types.AgentPool()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_agent_pool(
            project_id="project_id_value",
            agent_pool=transfer_types.AgentPool(name="name_value"),
            agent_pool_id="agent_pool_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].agent_pool
        mock_val = transfer_types.AgentPool(name="name_value")
        assert arg == mock_val
        arg = args[0].agent_pool_id
        mock_val = "agent_pool_id_value"
        assert arg == mock_val


def test_create_agent_pool_flattened_error():
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_agent_pool(
            transfer.CreateAgentPoolRequest(),
            project_id="project_id_value",
            agent_pool=transfer_types.AgentPool(name="name_value"),
            agent_pool_id="agent_pool_id_value",
        )


@pytest.mark.asyncio
async def test_create_agent_pool_flattened_async():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_agent_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = transfer_types.AgentPool()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transfer_types.AgentPool()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_agent_pool(
            project_id="project_id_value",
            agent_pool=transfer_types.AgentPool(name="name_value"),
            agent_pool_id="agent_pool_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].agent_pool
        mock_val = transfer_types.AgentPool(name="name_value")
        assert arg == mock_val
        arg = args[0].agent_pool_id
        mock_val = "agent_pool_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_agent_pool_flattened_error_async():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_agent_pool(
            transfer.CreateAgentPoolRequest(),
            project_id="project_id_value",
            agent_pool=transfer_types.AgentPool(name="name_value"),
            agent_pool_id="agent_pool_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        transfer.UpdateAgentPoolRequest,
        dict,
    ],
)
def test_update_agent_pool(request_type, transport: str = "grpc"):
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_agent_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = transfer_types.AgentPool(
            name="name_value",
            display_name="display_name_value",
            state=transfer_types.AgentPool.State.CREATING,
        )
        response = client.update_agent_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.UpdateAgentPoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, transfer_types.AgentPool)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == transfer_types.AgentPool.State.CREATING


def test_update_agent_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_agent_pool), "__call__"
    ) as call:
        client.update_agent_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.UpdateAgentPoolRequest()


@pytest.mark.asyncio
async def test_update_agent_pool_async(
    transport: str = "grpc_asyncio", request_type=transfer.UpdateAgentPoolRequest
):
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_agent_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transfer_types.AgentPool(
                name="name_value",
                display_name="display_name_value",
                state=transfer_types.AgentPool.State.CREATING,
            )
        )
        response = await client.update_agent_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.UpdateAgentPoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, transfer_types.AgentPool)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == transfer_types.AgentPool.State.CREATING


@pytest.mark.asyncio
async def test_update_agent_pool_async_from_dict():
    await test_update_agent_pool_async(request_type=dict)


def test_update_agent_pool_field_headers():
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transfer.UpdateAgentPoolRequest()

    request.agent_pool.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_agent_pool), "__call__"
    ) as call:
        call.return_value = transfer_types.AgentPool()
        client.update_agent_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "agent_pool.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_agent_pool_field_headers_async():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transfer.UpdateAgentPoolRequest()

    request.agent_pool.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_agent_pool), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transfer_types.AgentPool()
        )
        await client.update_agent_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "agent_pool.name=name_value",
    ) in kw["metadata"]


def test_update_agent_pool_flattened():
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_agent_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = transfer_types.AgentPool()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_agent_pool(
            agent_pool=transfer_types.AgentPool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].agent_pool
        mock_val = transfer_types.AgentPool(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_agent_pool_flattened_error():
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_agent_pool(
            transfer.UpdateAgentPoolRequest(),
            agent_pool=transfer_types.AgentPool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_agent_pool_flattened_async():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_agent_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = transfer_types.AgentPool()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transfer_types.AgentPool()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_agent_pool(
            agent_pool=transfer_types.AgentPool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].agent_pool
        mock_val = transfer_types.AgentPool(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_agent_pool_flattened_error_async():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_agent_pool(
            transfer.UpdateAgentPoolRequest(),
            agent_pool=transfer_types.AgentPool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        transfer.GetAgentPoolRequest,
        dict,
    ],
)
def test_get_agent_pool(request_type, transport: str = "grpc"):
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_agent_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = transfer_types.AgentPool(
            name="name_value",
            display_name="display_name_value",
            state=transfer_types.AgentPool.State.CREATING,
        )
        response = client.get_agent_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.GetAgentPoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, transfer_types.AgentPool)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == transfer_types.AgentPool.State.CREATING


def test_get_agent_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_agent_pool), "__call__") as call:
        client.get_agent_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.GetAgentPoolRequest()


@pytest.mark.asyncio
async def test_get_agent_pool_async(
    transport: str = "grpc_asyncio", request_type=transfer.GetAgentPoolRequest
):
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_agent_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transfer_types.AgentPool(
                name="name_value",
                display_name="display_name_value",
                state=transfer_types.AgentPool.State.CREATING,
            )
        )
        response = await client.get_agent_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.GetAgentPoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, transfer_types.AgentPool)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == transfer_types.AgentPool.State.CREATING


@pytest.mark.asyncio
async def test_get_agent_pool_async_from_dict():
    await test_get_agent_pool_async(request_type=dict)


def test_get_agent_pool_field_headers():
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transfer.GetAgentPoolRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_agent_pool), "__call__") as call:
        call.return_value = transfer_types.AgentPool()
        client.get_agent_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_agent_pool_field_headers_async():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transfer.GetAgentPoolRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_agent_pool), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transfer_types.AgentPool()
        )
        await client.get_agent_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_agent_pool_flattened():
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_agent_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = transfer_types.AgentPool()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_agent_pool(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_agent_pool_flattened_error():
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_agent_pool(
            transfer.GetAgentPoolRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_agent_pool_flattened_async():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_agent_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = transfer_types.AgentPool()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transfer_types.AgentPool()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_agent_pool(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_agent_pool_flattened_error_async():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_agent_pool(
            transfer.GetAgentPoolRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        transfer.ListAgentPoolsRequest,
        dict,
    ],
)
def test_list_agent_pools(request_type, transport: str = "grpc"):
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_agent_pools), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = transfer.ListAgentPoolsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_agent_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.ListAgentPoolsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAgentPoolsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_agent_pools_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_agent_pools), "__call__") as call:
        client.list_agent_pools()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.ListAgentPoolsRequest()


@pytest.mark.asyncio
async def test_list_agent_pools_async(
    transport: str = "grpc_asyncio", request_type=transfer.ListAgentPoolsRequest
):
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_agent_pools), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transfer.ListAgentPoolsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_agent_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.ListAgentPoolsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAgentPoolsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_agent_pools_async_from_dict():
    await test_list_agent_pools_async(request_type=dict)


def test_list_agent_pools_field_headers():
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transfer.ListAgentPoolsRequest()

    request.project_id = "project_id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_agent_pools), "__call__") as call:
        call.return_value = transfer.ListAgentPoolsResponse()
        client.list_agent_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_agent_pools_field_headers_async():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transfer.ListAgentPoolsRequest()

    request.project_id = "project_id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_agent_pools), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transfer.ListAgentPoolsResponse()
        )
        await client.list_agent_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value",
    ) in kw["metadata"]


def test_list_agent_pools_flattened():
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_agent_pools), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = transfer.ListAgentPoolsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_agent_pools(
            project_id="project_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val


def test_list_agent_pools_flattened_error():
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_agent_pools(
            transfer.ListAgentPoolsRequest(),
            project_id="project_id_value",
        )


@pytest.mark.asyncio
async def test_list_agent_pools_flattened_async():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_agent_pools), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = transfer.ListAgentPoolsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transfer.ListAgentPoolsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_agent_pools(
            project_id="project_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_agent_pools_flattened_error_async():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_agent_pools(
            transfer.ListAgentPoolsRequest(),
            project_id="project_id_value",
        )


def test_list_agent_pools_pager(transport_name: str = "grpc"):
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_agent_pools), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            transfer.ListAgentPoolsResponse(
                agent_pools=[
                    transfer_types.AgentPool(),
                    transfer_types.AgentPool(),
                    transfer_types.AgentPool(),
                ],
                next_page_token="abc",
            ),
            transfer.ListAgentPoolsResponse(
                agent_pools=[],
                next_page_token="def",
            ),
            transfer.ListAgentPoolsResponse(
                agent_pools=[
                    transfer_types.AgentPool(),
                ],
                next_page_token="ghi",
            ),
            transfer.ListAgentPoolsResponse(
                agent_pools=[
                    transfer_types.AgentPool(),
                    transfer_types.AgentPool(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("project_id", ""),)),
        )
        pager = client.list_agent_pools(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, transfer_types.AgentPool) for i in results)


def test_list_agent_pools_pages(transport_name: str = "grpc"):
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_agent_pools), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            transfer.ListAgentPoolsResponse(
                agent_pools=[
                    transfer_types.AgentPool(),
                    transfer_types.AgentPool(),
                    transfer_types.AgentPool(),
                ],
                next_page_token="abc",
            ),
            transfer.ListAgentPoolsResponse(
                agent_pools=[],
                next_page_token="def",
            ),
            transfer.ListAgentPoolsResponse(
                agent_pools=[
                    transfer_types.AgentPool(),
                ],
                next_page_token="ghi",
            ),
            transfer.ListAgentPoolsResponse(
                agent_pools=[
                    transfer_types.AgentPool(),
                    transfer_types.AgentPool(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_agent_pools(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_agent_pools_async_pager():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_agent_pools), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            transfer.ListAgentPoolsResponse(
                agent_pools=[
                    transfer_types.AgentPool(),
                    transfer_types.AgentPool(),
                    transfer_types.AgentPool(),
                ],
                next_page_token="abc",
            ),
            transfer.ListAgentPoolsResponse(
                agent_pools=[],
                next_page_token="def",
            ),
            transfer.ListAgentPoolsResponse(
                agent_pools=[
                    transfer_types.AgentPool(),
                ],
                next_page_token="ghi",
            ),
            transfer.ListAgentPoolsResponse(
                agent_pools=[
                    transfer_types.AgentPool(),
                    transfer_types.AgentPool(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_agent_pools(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, transfer_types.AgentPool) for i in responses)


@pytest.mark.asyncio
async def test_list_agent_pools_async_pages():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_agent_pools), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            transfer.ListAgentPoolsResponse(
                agent_pools=[
                    transfer_types.AgentPool(),
                    transfer_types.AgentPool(),
                    transfer_types.AgentPool(),
                ],
                next_page_token="abc",
            ),
            transfer.ListAgentPoolsResponse(
                agent_pools=[],
                next_page_token="def",
            ),
            transfer.ListAgentPoolsResponse(
                agent_pools=[
                    transfer_types.AgentPool(),
                ],
                next_page_token="ghi",
            ),
            transfer.ListAgentPoolsResponse(
                agent_pools=[
                    transfer_types.AgentPool(),
                    transfer_types.AgentPool(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_agent_pools(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        transfer.DeleteAgentPoolRequest,
        dict,
    ],
)
def test_delete_agent_pool(request_type, transport: str = "grpc"):
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_agent_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_agent_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.DeleteAgentPoolRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_agent_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_agent_pool), "__call__"
    ) as call:
        client.delete_agent_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.DeleteAgentPoolRequest()


@pytest.mark.asyncio
async def test_delete_agent_pool_async(
    transport: str = "grpc_asyncio", request_type=transfer.DeleteAgentPoolRequest
):
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_agent_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_agent_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == transfer.DeleteAgentPoolRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_agent_pool_async_from_dict():
    await test_delete_agent_pool_async(request_type=dict)


def test_delete_agent_pool_field_headers():
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transfer.DeleteAgentPoolRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_agent_pool), "__call__"
    ) as call:
        call.return_value = None
        client.delete_agent_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_agent_pool_field_headers_async():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transfer.DeleteAgentPoolRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_agent_pool), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_agent_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_agent_pool_flattened():
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_agent_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_agent_pool(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_agent_pool_flattened_error():
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_agent_pool(
            transfer.DeleteAgentPoolRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_agent_pool_flattened_async():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_agent_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_agent_pool(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_agent_pool_flattened_error_async():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_agent_pool(
            transfer.DeleteAgentPoolRequest(),
            name="name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.StorageTransferServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = StorageTransferServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.StorageTransferServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = StorageTransferServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.StorageTransferServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = StorageTransferServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = StorageTransferServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.StorageTransferServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = StorageTransferServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.StorageTransferServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = StorageTransferServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.StorageTransferServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.StorageTransferServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.StorageTransferServiceGrpcTransport,
        transports.StorageTransferServiceGrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
    ],
)
def test_transport_kind(transport_name):
    transport = StorageTransferServiceClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.StorageTransferServiceGrpcTransport,
    )


def test_storage_transfer_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.StorageTransferServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_storage_transfer_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.storage_transfer_v1.services.storage_transfer_service.transports.StorageTransferServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.StorageTransferServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "get_google_service_account",
        "create_transfer_job",
        "update_transfer_job",
        "get_transfer_job",
        "list_transfer_jobs",
        "pause_transfer_operation",
        "resume_transfer_operation",
        "run_transfer_job",
        "create_agent_pool",
        "update_agent_pool",
        "get_agent_pool",
        "list_agent_pools",
        "delete_agent_pool",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_storage_transfer_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.storage_transfer_v1.services.storage_transfer_service.transports.StorageTransferServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.StorageTransferServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_storage_transfer_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.storage_transfer_v1.services.storage_transfer_service.transports.StorageTransferServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.StorageTransferServiceTransport()
        adc.assert_called_once()


def test_storage_transfer_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        StorageTransferServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.StorageTransferServiceGrpcTransport,
        transports.StorageTransferServiceGrpcAsyncIOTransport,
    ],
)
def test_storage_transfer_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.StorageTransferServiceGrpcTransport,
        transports.StorageTransferServiceGrpcAsyncIOTransport,
    ],
)
def test_storage_transfer_service_transport_auth_gdch_credentials(transport_class):
    host = "https://language.com"
    api_audience_tests = [None, "https://language2.com"]
    api_audience_expect = [host, "https://language2.com"]
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, "default", autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(
                return_value=gdch_mock
            )
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(e)


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.StorageTransferServiceGrpcTransport, grpc_helpers),
        (transports.StorageTransferServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_storage_transfer_service_transport_create_channel(
    transport_class, grpc_helpers
):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "storagetransfer.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="storagetransfer.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.StorageTransferServiceGrpcTransport,
        transports.StorageTransferServiceGrpcAsyncIOTransport,
    ],
)
def test_storage_transfer_service_grpc_transport_client_cert_source_for_mtls(
    transport_class,
):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_storage_transfer_service_host_no_port(transport_name):
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="storagetransfer.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("storagetransfer.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_storage_transfer_service_host_with_port(transport_name):
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="storagetransfer.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("storagetransfer.googleapis.com:8000")


def test_storage_transfer_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.StorageTransferServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_storage_transfer_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.StorageTransferServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.StorageTransferServiceGrpcTransport,
        transports.StorageTransferServiceGrpcAsyncIOTransport,
    ],
)
def test_storage_transfer_service_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.StorageTransferServiceGrpcTransport,
        transports.StorageTransferServiceGrpcAsyncIOTransport,
    ],
)
def test_storage_transfer_service_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_storage_transfer_service_grpc_lro_client():
    client = StorageTransferServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_storage_transfer_service_grpc_lro_async_client():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsAsyncClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_agent_pools_path():
    project_id = "squid"
    agent_pool_id = "clam"
    expected = "projects/{project_id}/agentPools/{agent_pool_id}".format(
        project_id=project_id,
        agent_pool_id=agent_pool_id,
    )
    actual = StorageTransferServiceClient.agent_pools_path(project_id, agent_pool_id)
    assert expected == actual


def test_parse_agent_pools_path():
    expected = {
        "project_id": "whelk",
        "agent_pool_id": "octopus",
    }
    path = StorageTransferServiceClient.agent_pools_path(**expected)

    # Check that the path construction is reversible.
    actual = StorageTransferServiceClient.parse_agent_pools_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "oyster"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = StorageTransferServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nudibranch",
    }
    path = StorageTransferServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = StorageTransferServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "cuttlefish"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = StorageTransferServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "mussel",
    }
    path = StorageTransferServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = StorageTransferServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "winkle"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = StorageTransferServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nautilus",
    }
    path = StorageTransferServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = StorageTransferServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "scallop"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = StorageTransferServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "abalone",
    }
    path = StorageTransferServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = StorageTransferServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "squid"
    location = "clam"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = StorageTransferServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
    }
    path = StorageTransferServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = StorageTransferServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.StorageTransferServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = StorageTransferServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.StorageTransferServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = StorageTransferServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = StorageTransferServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close():
    transports = {
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = StorageTransferServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        with mock.patch.object(
            type(getattr(client.transport, close_name)), "close"
        ) as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()


def test_client_ctx():
    transports = [
        "grpc",
    ]
    for transport in transports:
        client = StorageTransferServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (StorageTransferServiceClient, transports.StorageTransferServiceGrpcTransport),
        (
            StorageTransferServiceAsyncClient,
            transports.StorageTransferServiceGrpcAsyncIOTransport,
        ),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
