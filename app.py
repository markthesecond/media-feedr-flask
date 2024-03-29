from flask import Flask, jsonify, g
from flask_login import LoginManager
from flask_cors import CORS
from resources.users import user
from resources.media import media
from resources.viewership import viewership
from resources.reviews import review
import os
import models

app = Flask('media-api')
app.secret_key = os.environ.get(
    'SECRET_KEY', 'notreallyasecretbutsureyoudoyoudude'
)
login_manager = LoginManager()
login_manager.init_app(app)


@app.before_request
def before_request():
    print("connected to db")
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(res):
    print("disconnected from db")
    g.db.close()
    return res


@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get_by_id(user_id)
    except models.DoesNotExist:
        return None


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify(
        data={
            "error": "Unauthenticated use of this resource is not allowed"
        },
        status={
            "code": 401,
            "message": "You must be logged in to do that."
        }
    ), 401


CORS(
    user,
    origins=['http://localhost:3000'],
    supports_credentials=True
)
CORS(
    media,
    origins=['http://localhost:3000'],
    supports_credentials=True
)
CORS(
    viewership,
    origins=['http://localhost:3000'],
    supports_credentials=True
)
CORS(
    review,
    origins=['http://localhost:3000'],
    supports_credentials=True
)


app.register_blueprint(user, url_prefix='/api/v1/user')
app.register_blueprint(media, url_prefix='/api/v1/media')
app.register_blueprint(viewership, url_prefix='/api/v1/viewership')
app.register_blueprint(review, url_prefix='/api/v1/reviews')


if __name__ == '__main__':
    models.initialize()
    app.run(
        debug=os.environ.get('DEBUG', True),
        port=os.environ.get('PORT', 8000)
    )
