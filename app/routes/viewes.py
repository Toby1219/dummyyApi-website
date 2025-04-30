from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from ..utils.routehandlers import query_api_many, pagnation_handler, search_handler, func_wraper_handler
from ..extension import message_handler
from flask_login import current_user

view_bp = Blueprint("view_bp", __name__)

@view_bp.route('/home')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.logIn'))
    message_handler(f"Welcome {current_user.username} this is the Home view")
    return render_template("index.html", signup_success=True, name=current_user.username), 200

@func_wraper_handler(view_bp, route_="/product/price")
def product_price():
    parm = request.args.get("sort", default='true', type=str)
    result = query_api_many()
    if parm != None and parm in ["true", "asec"]:      
        sort_data = sorted([k for k in result], key=lambda x: x['price'], reverse=False)
        message_handler("Price sorted Lowest to the Hightest")
        return jsonify(sort_data)
    elif parm !=  None and parm in ["false", "desec"]:
        sort_data = sorted([k for k in result], key=lambda x: x['price'], reverse=True)
        message_handler("Price sorted Hightest to the Lowest")
        return jsonify(sort_data)

@view_bp.route("/product/all")
def search_():
  pram = request.args.get('page', default='all')
  if pram == "all":
    result = pagnation_handler()
    message_handler("Showing all product data")
    return jsonify(result), 200
    #return render_template('index.html', data=result)
  else:
    result = pagnation_handler(int(pram))
    message_handler(f"Showing all product data. page {pram}")

    return jsonify(result), 200

@func_wraper_handler(view_bp, route_="/product/search_<string:val>=<string:val2>")
def search_query(val, val2):
    if val in 'title':
        val = 'title'
        result = search_handler(val, val2)
        message_handler(f"Showing product {val2} ")
        return jsonify(result), 200
    elif val in 'sku':
        val = 'sku'
        result = search_handler(val, val2)
        message_handler(f"Showing product sku {val2} ")
        return jsonify(result), 200
    elif val in 'category':
        val = 'category'
        result = search_handler(val, val2)
        message_handler(f"Showing product with category {val2} ")
        return jsonify(result), 200

@func_wraper_handler(view_bp, route_="/product/s=<string:squery>")
def searcher(squery):
    print(squery)
    result = search_handler(squery)
    return jsonify(result)

