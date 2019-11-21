import models
from flask import jsonify, request, Blueprint
from playhouse.shortcuts import model_to_dict

media = Blueprint('media', 'media')

@media.route('/', methods=['GET'])
def index():
    try:
        media_list = [model_to_dict(m) for m in models.Media.select()]
        return jsonify(
            data=media_list,
            status={
                "code": 200,
                "message": "Got all media. *evil laugh*"
            }
        )
    except Exception:
        return jsonify(
            data={},
            status={
                "code": 500,
                "message": "It looks like something went wrong. Our bad."
            }
        ), 500


@media.route('/', methods=['POST'])
def add_item():
    payload = request.get_json()
    try:
        models.Media.get(models.Media.external_id == payload['external_id'])
    except models.DoesNotExist:
        try:
            new_media = models.Media.create(**payload)
        except models.IntegrityError:
            return jsonify(
                data={},
                status={
                    "code": 422,
                    "message": "Cannot process media from before 1906, after 2020."
                }
            ), 422
        else:
            new_media_dict = model_to_dict(new_media)
            return jsonify(
                data=new_media_dict,
                status={
                    "code": 201,
                    "message": "Successfully added media item"
                }
            ), 201
    else:
        return jsonify(
            data={},
            status={
                "code": 422,
                "message": "Cannot add duplicate media item."
            }
        ), 422


@media.route('/<id>', methods=['GET'])
def show(id):
    try:
        media = models.Media.get_by_id(id)
        return jsonify(
            data=model_to_dict(media),
            status={
                "code": 200,
                "status": "Found requested item."
            }
        )
    except models.DoesNotExist:
        return jsonify(
            data={},
            status={
                "code": 404,
                "message": "Couldn't locate that media item."
            }
        ), 404