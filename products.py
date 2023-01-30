from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DecimalField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import datetime


from .models.product import Product
from .models.sells import Inventory
from .models.cart import Cart
from .models.review import Review
from .models.purchase import Purchase



from flask import Blueprint
bp = Blueprint('products', __name__)

@bp.route('/product_page/<int:pid>', methods=['GET', 'POST'])
@bp.route('/product_page/<int:pid>/<int:sid>', methods=['GET', 'POST'])
def product_page(pid, sid = None):
    product = Product.get(pid)
    add = addToCart()
    sellers = Inventory.get_all_by_pid(pid)
    form = WriteReview()
    
    time_reviewed = datetime.datetime.now()
    feedback = Review.get_product_reviews(pid)
    average = Review.get_product_avg(pid)
    count = Review.get_product_count(pid)

    
    
    #if any item is being added to cart
    if add.validate_on_submit and sid is not None and current_user.is_authenticated:
        print("validated")
        uid = current_user.id
        Cart.add_to_cart(current_user.id, pid, sid, add.addQuantity.data)
        return redirect(url_for('products.product_page', pid = pid))

    else:
        #if user is writing review
        if form.validate_on_submit() and current_user.is_authenticated:
            uid = current_user.id
            if Review.check_purchase(uid, pid) or form.stars.data > 5 or form.stars.data < 1:
                print('invalid')
            elif Review.check_review(uid, pid):
                Review.update_review(uid, pid, form.stars.data, form.review.data, time_reviewed)
                return render_template('product.html', title='Product Page', product=product, addToCart = add, sellers = sellers, form = form, feedback = feedback, average = average, count = count)
            else:
                Review.write_review(uid, pid, form.stars.data, form.review.data, time_reviewed)
                return render_template('product.html', title='Product Page', product=product, addToCart = add, sellers = sellers, form = form, feedback = feedback, average = average, count = count)
                
    return render_template('product.html', title='Product Page', product=product, addToCart = add, sellers = sellers, form = form, feedback = feedback, average = average, count = count)

class addToCart(FlaskForm):
    addQuantity = IntegerField(validators=[DataRequired()])
    submit = SubmitField('Add to Cart')


# Write a New Product Review
class WriteReview(FlaskForm):
    stars = IntegerField('Stars', validators=[DataRequired()])
    review = StringField('Review', validators=[DataRequired()])
    submit = SubmitField('Submit')

