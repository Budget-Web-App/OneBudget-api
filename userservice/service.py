from . import app

def create_app():
    """Flask application factory to create instances
    of the Userservice Flask App
    """

    return app


if __name__ == "__main__":
    # Create an instance of flask server when called directly
    USERSERVICE = create_app()
    USERSERVICE.run(debug=True, use_reloader=True)
