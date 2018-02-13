"""
This module contains example code for Flask usage.
Feel free to modify this file in any way.
"""
import json
import uuid
from flask import Flask, request, Response

from db import initialize_db, get_num_projects, add_project
from auth import get_user_info

app = Flask(__name__)
initialize_db()


@app.route("/", methods=["GET"])
def example():
    """
    Basic example of GET to / using Flask
    Does not handle missing or invalid Access Tokens
    """
    if request.method == "GET":
        # get bearer token from auth header
        auth_header = request.headers.get("authorization")
        access_token = auth_header[len("Bearer "):]

        # get username and num_projects to respond with
        user_info = get_user_info(access_token)
        username = user_info["username"]
        num_projects = get_num_projects()
        # respond
        response_dict = {
            "message": ("Hello {}, there are {} projects in the database!"
                        .format(username, num_projects))
        }
        return Response(json.dumps(response_dict), status=200,
                        mimetype='application/json')


def project_post(r):
    """
    POST request to projects.
    Reponse contains
    project_id: the project id of the submitted project
    owner_id: owner of the submitted project.
    owner_username: username of the owner
    project_name: name of the submitted project
    comments: Comments on the project, initialized to an empty list.
    """
    # get bearer token from auth header
    auth_header = request.headers.get("authorization")
    access_token = auth_header[len("Bearer "):]

    # get username and user id to respond with
    user_info = get_user_info(access_token)
    username = user_info["username"]
    user_id = user_info["user_id"]
    print("Posting user ID is {}.".format(user_id))

    data = json.loads(r.data)
    # Make a unique identifier for the new project
    project_id = str(uuid.uuid1())

    # Actually add the project to the database
    add_project(project_id, user_id)

    response_dict = {
            "message": "Post Projects",
            "project_id": project_id,
            "owner_id": user_id,
            "owner_username": username,
            "project_name": data['project_name'],
            "comments": []
    }
    return Response(json.dumps(response_dict), status=200,
                    mimetype='application/json')


def project_get(r):
    response_dict = {
            "message": "This method is not supported"
    }
    return Response(json.dumps(response_dict), status=405,
                    mimetype='application/json')


@app.route("/projects", methods=["GET", "POST"])
def projects():
    handler_table = {
                    "POST": project_post,
                    "GET": project_get}
    return handler_table[request.method](request)


if __name__ == "__main__":
    app.run()
