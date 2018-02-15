"""
This module contains an example of a requests based test for the example app.
Feel free to modify this file in any way.
"""
import requests
import json

from auth import get_test_access_tokens
from db import delete_project, add_project, get_comments_for_project
from db import add_comment


# testing constants and tokens
# tokens_1 and 2 are for challengeuser1 and challenguser2 respectively
BASE_URL = "http://127.0.0.1:5000"
ACCESS_TOKEN_1, ACCESS_TOKEN_2 = get_test_access_tokens()
USERNAME_1 = "challengeuser1@globusid.org"
USERNAME_2 = "challengeuser2@globusid.org"
USER_ID_1 = "8bde3e84-a964-479c-9c7b-4d7991717a1b"
USER_ID_2 = "45e3c49a-c699-405b-a8b2-f5407bb1a133"


def example_test():
    """
    Example of using requests to make a test call to the example Flask app
    """
    path = BASE_URL + "/"

    for access_token, username in [(ACCESS_TOKEN_1, USERNAME_1),
                                   (ACCESS_TOKEN_2, USERNAME_2)]:
        headers = {"Accept": "application/json",
                   "Content-Type": "application/json",
                   "Authorization": "Bearer " + access_token}

        r = requests.get(path, headers=headers)
        message = r.json()["message"]
        print(message)
        assert("Hello {}".format(username) in message)
        assert("0 projects" in message)

def post_project_test():
    """
    Tests users 1 and 2 adding a project
    """
    path = BASE_URL + "/projects"

    for access_token, username in [(ACCESS_TOKEN_1, USERNAME_1),
                                   (ACCESS_TOKEN_2, USERNAME_2)]:
        headers = {"Accept": "application/json",
                   "Content-Type": "application/json",
                   "Authorization": "Bearer " + access_token}

        r = requests.post(path, headers=headers,  data = json.dumps({"project_name": 'My Test Project'}))
        data = r.json()
        for k in data:
            print k, data[k]
        delete_project(data['project_id'])


def project_methods_not_allowed():
    """
    Uses all unallowed methods on the /projects endpoint.
    """
    results = []
    r = requests.get(BASE_URL + '/projects')
    results.append(r.status_code)
    r = requests.put(BASE_URL + '/projects')
    results.append(r.status_code)
    r = requests.delete(BASE_URL + '/projects')
    results.append(r.status_code)
    for code in results:
        assert(code == 405)


def project_bad_request():
    """
    Sumbits request to /projects without a project name.
    """
    path = BASE_URL + "/projects"
    headers = {"Accept": "application/json",
               "Content-Type": "application/json",
               "Authorization": "Bearer " + ACCESS_TOKEN_1}

    r = requests.post(path, headers=headers,  data = json.dumps({"name": 'My Test Project'}))
    assert(r.status_code == 400)

def project_no_auth():
    """
    Submits a request to /projects without a valid bearer.
    """
    path = BASE_URL + "/projects"
    headers = {"Accept": "application/json",
               "Content-Type": "application/json",
               "Authorization": "Bearer " + "zzz"}

    r = requests.post(path, headers=headers,  data = json.dumps({"name": 'My Test Project'}))
    assert(r.status_code == 403)

def get_project_test():
    """
    Tests get method on /projects/<id> endpoint.
    """
    add_project("111", "Test Project", "challengeuser1@globusid.org", "8bde3e84-a964-479c-9c7b-4d7991717a1b")
    add_comment("0", "55555", "fake user", "fake user's message", "111")
    add_comment("1", "55555", "fake user", "fake user's second message", "111")
    add_comment("2", "55555", "fake user", "fake user's last message", "111")
    path = BASE_URL + "/projects/111"

    for access_token, username in [(ACCESS_TOKEN_1, USERNAME_1),
                                   (ACCESS_TOKEN_2, USERNAME_2)]:
        headers = {"Accept": "application/json",
                   "Content-Type": "application/json",
                   "Authorization": "Bearer " + access_token}

        r = requests.get(path, headers=headers)
        data = r.json()
        for k in data:
            print k, data[k]
    delete_project("111")

def make_comment_test():
    """
    Tests /project/<id>/comments endpoint, with a valid request.
    """
    add_project("111", "Test Project", "challengeuser1@globusid.org", "8bde3e84-a964-479c-9c7b-4d7991717a1b")
    path = BASE_URL + "/projects/111/comments"

    for access_token, username in [(ACCESS_TOKEN_1, USERNAME_1),
                                   (ACCESS_TOKEN_2, USERNAME_2)]:
        headers = {"Accept": "application/json",
                   "Content-Type": "application/json",
                   "Authorization": "Bearer " + access_token}

        r = requests.post(path, headers=headers, data=json.dumps({"message": 'Comments are great ' + username}))
        data = r.json()
        for k in data:
            print k, data[k]
    print("here are the comments:")
    print(get_comments_for_project("111"))
    delete_project("111")

def delete_project_test():
    add_project("111", "Test Project", "challengeuser1@globusid.org", "8bde3e84-a964-479c-9c7b-4d7991717a1b")
    add_comment("0", "55555", "fake user", "fake user's message", "111")
    add_comment("1", "55555", "fake user", "fake user's second message", "111")
    add_comment("2", "55555", "fake user", "fake user's last message", "111")
    path = BASE_URL + "/projects/111"

    headers = {"Accept": "application/json",
               "Content-Type": "application/json",
               "Authorization": "Bearer " + ACCESS_TOKEN_1}

    r = requests.delete(path, headers=headers)
    data = r.json()
    for k in data:
        print k, data[k]

if __name__ == "__main__":
    example_test()
    post_project_test()
    project_methods_not_allowed()
    project_bad_request()
    project_no_auth()
    get_project_test()
    make_comment_test()
    delete_project_test()
