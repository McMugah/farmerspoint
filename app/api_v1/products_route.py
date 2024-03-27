
from flask import render_template ,redirect, url_for,current_app
from flask_login import current_user
from . import  api
from flask import request
from . import api
from .. import db
from ..models import Product
from ..forms.products_form import ProductForm
from flask_login import current_user
from werkzeug.utils import secure_filename
import os


@api.route('/create_product', methods=['GET', 'POST'])
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        # Handle image upload
        image_file = form.image.data
        if image_file:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
        else:
            image_path = None
        product = Product(
            name=form.name.data,
            price=form.price.data,
            description=form.description.data,
            quantity=form.quantity.data,
            user_id=current_user.id,  # Assuming you're using Flask-Login for user management
            farmer_id=current_user.farmer.id,  # Assuming current_user is a Farmer instance
            image=image_path  # Save the image path to the database
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('product_list'))
    return render_template('create_product.html', form=form)


@api.route('/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    return render_template('products.html', products=products)
