from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import datetime

from .models.cart import Cart
from .models.sells import Inventory
from .models.product import Product
from .models.purchase import Purchase
from .models.review import Review
from .models.user import User


from flask import Blueprint
bp = Blueprint('hw4', __name__)

# --------------------
# USERS:

class FindPurchaseForm(FlaskForm):
    uid = StringField('User ID', validators=[DataRequired()])
    submit = SubmitField('Find')

@bp.route('/hw4_users.html', methods=['GET', 'POST'])
def findPurchases():
    form = FindPurchaseForm()
    purchases = []
    if form.validate_on_submit():
        purchases = Purchase.get_by_uid(form.uid.data)
    return render_template('hw4_users.html', title='Find User Purchases', form=form, purchases=purchases)


# --------------------
# PRODUCTS:
class KMostExpensiveForm(FlaskForm):
    k = StringField('\'K Most Expensive Products\' (Enter an Integer K):', validators=[DataRequired()])
    submit = SubmitField('Search')

@bp.route('/hw4_products', methods=['GET', 'POST'])
def findKProducts():
    form = KMostExpensiveForm()
    kMost = []
    if form.validate_on_submit():
        kMost = Product.get_k_most_expensive(form.k.data)
    return render_template('hw4_products.html', title='Find K Most Expensive Products', form=form, kMostExpensive=kMost)



# --------------------
# CARTS:

class FindCartForm(FlaskForm):
    uid = StringField('User ID', validators=[DataRequired()])
    submit = SubmitField('Show')

@bp.route('/hw4_carts.html', methods=['GET', 'POST'])
def findCarts():
    form = FindCartForm()
    if form.validate_on_submit():
        carts = Cart.get_by_uid(form.uid.data)
        total = Cart.get_total(form.uid.data)
        return render_template('hw4_carts.html', title='My Cart', form=form, carts=carts, total = total)
    else:
        return render_template('hw4_carts.html', title='My Cart', form=form, carts=[], total = 0)

# --------------------
# SELLERS:

class FindSellerInventory(FlaskForm):
    uid = StringField('Seller ID', validators=[DataRequired()])
    submit = SubmitField('Find')

@bp.route('/hw4_sellers.html', methods=['GET', 'POST'])
def findInventory():
    form = FindSellerInventory()
    inventory = []
    if form.validate_on_submit():
        inventory = Inventory.get_by_uid(form.uid.data)
    else:
        inventory = []
    return render_template('hw4_sellers.html', title='Find Seller Inventory', form=form, inventory=inventory)


# --------------------
# SOCIAL:
class FindSocialForm(FlaskForm):
    pid = StringField('Product ID', validators=[DataRequired()])
    submit = SubmitField('Search')

@bp.route('/review.html', methods=['GET', 'POST'])
def findFeedback():
    form = FindSocialForm()
    if form.validate_on_submit():
        feedback = Review.get_product_reviews(form.pid.data)
        summary_stats = Review.get_product_avg(form.pid.data)
        return render_template('review.html', title='Find Feedback', form=form, feedback=feedback, summary_stats = summary_stats)
    else:
        return render_template('review.html', title='Find Feedback', form=form, feedback=[], summary_stats = [])
