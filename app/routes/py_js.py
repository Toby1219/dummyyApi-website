import json
from flask import Blueprint, jsonify, request
from ..utils.routehandlers import query_api_only
from ..extension import reader
from flask_login import current_user

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/load-data', methods=['GET'])
def load_html():
    pramargs = request.args.get('q')
    datas = json.loads(query_api_only(pramargs))
    result = []
    for data in datas:
        for _, v in data.items():
            result.append(v)
    return result

@admin_bp.route('/message', methods=["GET"])
def mesg():
    v = reader('./instance/message.json')
    return jsonify(v)

@admin_bp.route('/tokens', methods=["GET"])
def getToken():
    if not current_user.is_authenticated:
        return jsonify({"Message":"Login or signup to get token"})
    token = current_user.token
    refresh_token = current_user.refresh_token
    return jsonify({"token":token, "refresh_token":refresh_token})
    
