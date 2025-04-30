from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from sqlalchemy.orm import Session

db = SQLAlchemy()
jwt = JWTManager()
login_manager = LoginManager()

def session_handler() -> Session:
    with db.session() as session:
        return session


def write_jsons(v, path):
    import json
    with open(f"{path}", "w") as f:
        json.dump(v, f, indent=2)

def reader(path):
    import json
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            
        return data
    except:
        return None

def update_jsons(v):
    datas = reader()
    datas['data']['token'] = v
    write_jsons(datas)


def message_handler(msg, path='./instance/message.json', ok:bool=True, write=True)->dict:
    response = {
        "status":"sucess" if ok else "Error",
        "message": msg,
    }
    if write:
        write_jsons(response, path)
    return response
