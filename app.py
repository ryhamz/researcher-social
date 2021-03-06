"""
This module contains example code for Flask usage.
Feel free to modify this file in any way.
"""
import json
import uuid
from flask import Flask, request, Response

from db import initialize_db, get_num_projects, add_project
from db import get_project_by_id, add_comment, get_comments_for_project
from db import delete_owners_project
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


def bad_request():
    """
    Returns a response with status code 400.
    Use for invalid json
    """
    response_dict = {
            "message": "Incorrect JSON provided."
    }
    return Response(json.dumps(response_dict), status=400,
                    mimetype='application/json')

def bad_auth():
    """
    Returns a response with status code 403.
    Use for invalid authentication/
    """
    response_dict = {
            "message": "Userinfo could not be gotten from token."
    }
    return Response(json.dumps(response_dict), status=403,
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
    try:
        user_info = get_user_info(access_token)
    except ValueError:
        return bad_auth()

    username = user_info["username"]
    user_id = user_info["user_id"]
    print("Posting user ID is {}.".format(user_id))

    data = json.loads(r.data)
    # Make a unique identifier for the new project
    project_id = str(uuid.uuid1())
    if 'project_name' not in data:
        return bad_request()
    project_name = data['project_name']

    # Actually add the project to the database
    add_project(project_id, project_name, username, user_id)

    response_dict = {
            "message": "Post Projects",
            "project_id": project_id,
            "owner_id": user_id,
            "owner_username": username,
            "project_name": project_name,
            "comments": []
    }
    return Response(json.dumps(response_dict), status=200,
                    mimetype='application/json')


def retrieve_project(r, project_id):
    project = get_project_by_id(project_id)
    # get bearer token from auth header
    auth_header = request.headers.get("authorization")
    access_token = auth_header[len("Bearer "):]

    comments = get_comments_for_project(project_id)

    response_dict = {
            "message": "Get project",
            "project_id": project_id,
            "owner_id": project['owner_id'],
            "owner_username": project['owner_username'],
            "project_name": project['project_name'],
            "comments": [dict(c) for c in comments]
    }
    return Response(json.dumps(response_dict), status=200,
                    mimetype='application/json')


def delete_project(r, project_id):
    project = get_project_by_id(project_id)
    # get bearer token from auth header
    auth_header = request.headers.get("authorization")
    access_token = auth_header[len("Bearer "):]

    # get user id to compare against owner id.
    user_info = get_user_info(access_token)
    user_id = user_info["user_id"]

    comments = get_comments_for_project(project_id)
    delete_check = delete_owners_project(project_id, user_id)

    if delete_check:
        status_code = 200
        response_dict = {
                "project_id": project_id,
                "owner_id": project['owner_id'],
                "owner_username": project['owner_username'],
                "project_name": project['project_name'],
                "comments": [dict(c) for c in comments]
        }
    else:
        status_code = 403
        response_dict = {"message": "You are not the owner\
                          of project " + project_id}
    return Response(json.dumps(response_dict), status=status_code,
                    mimetype='application/json')


def create_comment(r, project_id):
    # get bearer token from auth header
    auth_header = request.headers.get("authorization")
    access_token = auth_header[len("Bearer "):]

    # get username and user id to respond with
    user_info = get_user_info(access_token)
    username = user_info["username"]
    user_id = user_info["user_id"]

    data = json.loads(r.data)

    # Create the comment id.
    comment_id = str(uuid.uuid1())

    # Insert the comment
    add_comment(comment_id, user_id, username, data['message'], project_id)

    response_dict = {
            "comment_id": comment_id,
            "commenter_id": user_id,
            "commenter_username": username,
            "message": data['message']
    }
    return Response(json.dumps(response_dict), status=200,
                    mimetype='application/json')


@app.route("/projects", methods=["POST"])
def projects():
    handler_table = {
                    "POST": project_post}
    return handler_table[request.method](request)


@app.route("/projects/<project_id>", methods=["GET", "DELETE"])
def project(project_id):
    handler_table = {
                    "DELETE": delete_project,
                    "GET": retrieve_project}
    return handler_table[request.method](request, project_id)


@app.route("/projects/<project_id>/comments", methods=["POST"])
def comment(project_id):
    handler_table = {
                    "POST": create_comment}
    return handler_table[request.method](request, project_id)


if __name__ == "__main__":
    app.run()
