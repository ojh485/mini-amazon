from flask import render_template
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import datetime

from .models.rating import Rating

from flask import Blueprint
bp = Blueprint('ratings', __name__)

# Find Ratings and Summary Stats by Seller ID
class FindSocialForm(FlaskForm):
    sid = StringField('Seller ID', validators=[DataRequired()])
    submit = SubmitField('Search')

@bp.route('/review_page', methods = ['GET', 'POST'])
def feedback_home():
    return render_template('review.html')

@bp.route('/seller_ratings', methods=['GET', 'POST'])
def findFeedback():
    form = FindSocialForm()
    if form.validate_on_submit():
        feedback = Rating.get_seller_ratings(form.sid.data)
        summary_stats = Rating.get_seller_avg(form.sid.data)
        count = Rating.get_seller_count(form.sid.data)
        return render_template('ratingsubpage.html', title='Seller Ratings', form=form, feedback=feedback, summary_stats = summary_stats, count = count)
    else:
        return render_template('ratingsubpage.html', title='Seller Ratings', form=form, feedback=[], summary_stats = [], count = [])
