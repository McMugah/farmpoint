from . import api


@api.route("/")
def get_user():
    return "Hello World!"
