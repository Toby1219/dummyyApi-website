from ..schemas.schema import ProductSchema
from ..models.model import Product
from ..extension import message_handler
from flask import flash
import json
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt
from functools import wraps

def query_api_only(val):
    prods = Product.query.all()
    prod_sku = ProductSchema(many=True, only=[val])
    product_sku = json.dumps(prod_sku.dump(prods), indent=4)
    return product_sku

def query_api_many()->list[dict]:
    prods = Product.query.all()
    prod_ = ProductSchema(many=True, exclude=["id"])
    product_ = json.loads(json.dumps(prod_.dump(prods), indent=4))
    output_dict = []
    for prods in product_:
        output_dict.append(prods)
    return output_dict

def pagnation_handler(_page=1, _per_page=5):
    pagination = Product.query.paginate(
        page=_page,
        per_page=_per_page
    )
    prod_ = ProductSchema(many=True)
    products = prod_.dump(pagination.items)

    return products


def search_handler(*args):
    prod = query_api_many()
    s = None
    try:
        if "%" in args[1]:
            s = args[1].replace("%", " ")
            print(args[1])
        else:
            s = args[1]
        result = [p for p in prod if p[args[0]].lower() == s.lower()]
        return result
    except:
        s = args[0]
        result = [p for p in prod for k, v in p.items() if k in ['title', 'sku', "category"] and str(v).lower() == s.lower()]
        if len(result) == 0:
            message_handler([f"No results for '{s}' "])
            return [{"Message":f"No results for '{s}' "}]        
        return result

def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") not in roles:
                return flash(f"Access denied: {claims.get("role")}", "error"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper


def func_wraper_handler(bp, method="GET", route_="/", sec="2"):
    def decorator(f):
        @wraps(f)
        @bp.route(route_, methods=[method])
        #@limiter.limit(f"{sec} per seconds")
        @role_required('user', 'admin')  # Restrict access to users with 'user' or 'admin' roles.
        @jwt_required()  # Require JWT authentication for the route.
        def wraped(*args, **kwargs):
            return f(*args, **kwargs)
        return wraped

    return decorator

def token_times(payload):
    from datetime import datetime
    claims = payload()
    issued_at = datetime.fromtimestamp(claims["iat"]).strftime("%Y-%m-%d %H:%M:%S")
    exp_time = datetime.fromtimestamp(claims["exp"]).strftime("%Y-%m-%d %H:%M:%S")
    return issued_at, exp_time