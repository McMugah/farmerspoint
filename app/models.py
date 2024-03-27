from datetime import timedelta,datetime
from . import db, login_manager,bcrypt,jwt
from flask_login import UserMixin
from flask_jwt_extended import create_access_token
from .exceptions import ValidationError
from flask import url_for


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    user_type = db.Column(db.String(50))

    # Added to differentiate user types
    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def generate_token(self, expiration=3600):
        token = create_access_token(identity=self.id, expires_delta=timedelta(seconds=expiration))
        return token


    @staticmethod
    def verify_token(token):
        """Verify the access token."""
        try:
            decoded_token = jwt.decode_token(token)
            user_id = decoded_token.get("sub")
            return user_id
        except Exception as e:
            return None


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


# class Farmer(User):
#     __tablename__ = 'farmers'
#     id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
#     farm_name = db.Column(db.String(100), nullable=False)
#     farmer_products = db.relationship('Product', backref='farmer', lazy=True)

#     __mapper_args__ = {
#         'polymorphic_identity': 'farmer',
#     }



class Customer(User):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'customer',
    }


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    image = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('user_products', lazy=True))
    farmer = db.relationship('Farmer', foreign_keys=[farmer_id], backref=db.backref('farmer_products', lazy=True))

    def __repr__(self):
        return f'<Product {self.name}>'

    def get_url(self):
        return url_for('api.get_product', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'quantity': self.quantity,
            'user_id': self.user_id,
            'farmer_id': self.farmer_id,
            'created_at': self.created_at.isoformat() + 'Z',
            'updated_at': self.updated_at.isoformat() + 'Z'
        }

    def import_data(self, data):
        try:
            self.name = data['name']
            self.price = data['price']
            self.description = data.get('description')
            self.quantity = data['quantity']
            self.user_id = data['user_id']
            self.farmer_id = data['farmer_id']
        except KeyError as e:
            raise ValidationError('Invalid product: missing ' + e.args[0])
        return self


class Farmer(User):
    __tablename__ = 'farmers'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    farm_name = db.Column(db.String(100), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'farmer',
    }
