import random
import string

from flask import Flask, request, jsonify

from reddit import Reddit


reddit = Reddit()


def _random_string(len):
    return "".join(random.choice(string.hexdigits) for _ in range(len))


app = Flask("reddit")
app.secret_key = _random_string(1024)


@app.route("/", methods=["GET", "POST"])
def test():
    return request.args


@app.route("/reddit/login", methods=["POST"])
def login():
    global reddit
    data = request.json
    if data is None:
        return jsonify({"error": "No data was received"}), 400
    if "username" in data and "password" in data:
        reddit.login(username=data["username"], password=data["password"])
    return "", 200


@app.route("/reddit/setPage", methods=["POST"])
def set_page():
    global reddit
    try:
        page_name = request.args["pageName"]
        reddit.set_page(page_name)
        return ""
    except KeyError:
        return jsonify({"error": "usage: /reddit/setPage?pageName=<value>"}), 400


@app.route("/reddit/firstPage")
def first_page():
    global reddit
    return jsonify([post.as_json() for post in reddit.first_page()])


@app.route("/reddit/nextPage")
def next_page():
    global reddit
    return jsonify([post.as_json() for post in reddit.next_page()])
