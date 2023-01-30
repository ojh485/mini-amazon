from flask import render_template
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import datetime

from .models.product import Product
from .models.sells import Inventory
from .models.cart import Cart
from .models.review import Review
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('reviews', __name__)

# Find Reviews and Summary Stats by Product ID
class FindSocialForm(FlaskForm):
    pid = StringField('Product ID', validators=[DataRequired()])
    submit = SubmitField('Search')

@bp.route('/review_page', methods = ['GET', 'POST'])
def feedback_home():
    return render_template('review.html')

@bp.route('/product_reviews', methods=['GET', 'POST'])
def findFeedback():
    form = FindSocialForm()
    if form.validate_on_submit():
        feedback = Review.get_product_reviews(form.pid.data)
        summary_stats = Review.get_product_avg(form.pid.data)
        count = Review.get_product_count(form.pid.data)
        return render_template('reviewsubpage.html', title='Product Reviews', form=form, feedback=feedback, summary_stats = summary_stats, count = count)
    else:
        return render_template('reviewsubpage.html', title='Product Reviews', form=form, feedback=[], summary_stats = [], count = [])
