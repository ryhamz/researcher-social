"""
This module contains example code for Flask usage.
Feel free to modify this file in any way.
"""
import json
from flask import Flask, request, Response

from db import initialize_db, get_num_projects
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
    response_dict = {
            "message": "Post Projects"
    }
    print(json.loads(r.data)['project_name'])
    return Response(json.dumps(response_dict), status=200,
                        mimetype='application/json')

def project_get(r):
    response_dict = {
            "message": "Get Projects"
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
