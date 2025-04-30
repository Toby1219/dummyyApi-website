from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models.model import UserAccount, Product


class UserAccSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserAccount
        load_instance = True 


class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True


