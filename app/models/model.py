from ..extension import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

class UserAccount(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(7), default="guest")
    token = db.Column(db.String())
    refresh_token = db.Column(db.String())
    token_created_at = db.Column(db.String(25), default=datetime.now())
    token_exp_at = db.Column(db.String(25), default="0")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        if not self.password_hash:
            raise ValueError("Password hash is not set for this user.")
        return check_password_hash(self.password_hash, password)
    
    def create_user(self):
        db.session.add(self)
        db.session.commit()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    price = db.Column(db.Float)
    discount_percentage = db.Column(db.Float)
    rating = db.Column(db.Float)
    stock = db.Column(db.Integer)
    sku = db.Column(db.String(50))
    weight = db.Column(db.Float)
    warranty_information = db.Column(db.String(200))
    shipping_information = db.Column(db.String(200))
    availability_status = db.Column(db.String(50))
    return_policy = db.Column(db.String(200))
    minimum_order_quantity = db.Column(db.Integer)
    thumbnail = db.Column(db.String(255))
    
    dimensions = db.relationship("Dimension", backref="product", uselist=False)
    meta = db.relationship("Meta", backref="product", uselist=False)
    reviews = db.relationship("Review", backref="product", lazy=True)
    images = db.relationship("Image", backref="product", lazy=True)
    tags = db.relationship("Tag", backref="product", lazy=True)

class Dimension(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    width = db.Column(db.Float)
    height = db.Column(db.Float)
    depth = db.Column(db.Float)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

class Meta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    createdAt = db.Column(db.String(100))
    updatedAt = db.Column(db.String(100))
    barcode = db.Column(db.String(50))
    qrCode = db.Column(db.String(255))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float)
    comment = db.Column(db.Text)
    date = db.Column(db.String(100))
    reviewerName = db.Column(db.String(100))
    reviewerEmail = db.Column(db.String(100))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))