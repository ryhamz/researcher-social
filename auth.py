"""
This module contains fixtures and helpers for interacting with the
Globus Auth API. You should not need to make any changes to this file.
"""
from globus_sdk import AuthClient, AccessTokenAuthorizer
from globus_sdk.exc import GlobusError

CLIENT_ID = "6b61a501-6102-47d9-9840-60abe24f0c02"
TEST_REFRESH_TOKEN_1 = ("AgN4ddO35NDJdodGvr5nmOrxE7P60Qkvdp04naaGxr99kdqnOVI5U"
                        "NOYv3qwm4pBjw4W60lo3QkzJxWJJok5JQwv1Wb9o")
TEST_REFRESH_TOKEN_2 = ("AgrqYxY9oQVo6wBzayE404EQNWwP817gm7GKqnBlzN54K551yas3U"
                        "04mE55y4dlOa9wKJQM88XNpXq8bjq2epMM6XBmwX")


def get_user_info(access_token):
    """
    Given an Access Token issued by the Globus Auth API introspects the token
    and returns a dict with user_id and username keys.
    Raises a ValueError if the token introspection fails
    """
    auth_client = AuthClient(authorizer=AccessTokenAuthorizer(access_token),
                             client_id=CLIENT_ID)

    try:
        userinfo_res = auth_client.oauth2_userinfo()
    except GlobusError as err:
        raise ValueError("Userinfo could not be gotten from token. "
                         "Failure on: {}".format(err))

    return {
        "user_id": userinfo_res.get("sub"),
        "username": userinfo_res.get("preferred_username")
    }


def get_test_access_tokens():
    """
    Uses hard-coded refresh tokens to get an Access Tokens for challengeuser1
    and challengeuser2
    """
    ac = AuthClient()

    form_data_1 = {"refresh_token": TEST_REFRESH_TOKEN_1,
                   "grant_type": 'refresh_token',
                   "client_id": CLIENT_ID}
    access_token_1 = ac.oauth2_token(form_data_1)["access_token"]

    form_data_2 = {"refresh_token": TEST_REFRESH_TOKEN_2,
                   "grant_type": 'refresh_token',
                   "client_id": CLIENT_ID}
    access_token_2 = ac.oauth2_token(form_data_2)["access_token"]

    return access_token_1, access_token_2
