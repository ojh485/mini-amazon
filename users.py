from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
from .models.user import User
from .models.purchase import Purchase
from .models.rating import Rating
from .models.review import Review
import base64
from io import BytesIO
from matplotlib.figure import Figure
import datetime


from flask import Blueprint
bp = Blueprint('users', __name__)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data,
                         form.address.data, 0):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))

class UpdateForm(FlaskForm):
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    email = StringField('Email', validators=[Email()])
    address = StringField('Address')
    password = PasswordField('Password')
    submit = SubmitField('Save Changes')

class BalanceForm(FlaskForm):
    deposit = DecimalField('Deposit', validators=[NumberRange(min=0)])
    withdrawl = DecimalField('Withdrawl', validators=[NumberRange(min=0)])
    submit = SubmitField('Save Changes')

class PurchaseHistoryForm(FlaskForm):
    category = SelectField(label = 'Filter Category', choices=['All','Item','Delivered', 'Date'], validators=[DataRequired()])
    search = StringField('Filter Search')
    submit = SubmitField('Filter')

class ReviewForm(FlaskForm):
    review = StringField('Review')
    stars = IntegerField('Stars')
    submit = SubmitField('Save Changes')

class RatingForm(FlaskForm):
    rating = StringField('Rating')
    stars = IntegerField('Stars')
    submit = SubmitField('Save Changes')

class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')

class RatingDeleteForm(FlaskForm):
    submit = SubmitField('Delete')
    

@bp.route('/user_page', methods=['GET', 'POST'])
@bp.route('/user_page/<int:reviewUID>/<int:reviewPID>', methods=['GET', 'POST'])
@bp.route('/user_page/<int:ratingUID>/<int:ratingSID>', methods=['GET', 'POST'])
def updateAccount(reviewUID = None, reviewPID = None, ratingUID = None, ratingSID = None):
    sells = Purchase.get_seller_history(current_user.id)
    isSeller = User.isSeller(current_user.id)

    values = []
    dates = []
    val = 0
    profits = Purchase.getProfits(current_user.id)
    
    for p in profits:
        dates.append(p[1])
        val += p[0]
        values.append(val)

    print(values)

    fig = Figure()
    ax = fig.subplots()
    ax.plot(dates, values)
    ax.set_title('Sales vs Purchase Earnings Over Time')
    ax.set_xlabel('Time (Years)')
    ax.set_ylabel('Dollars ($)')
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    myImg = f"data:image/png;base64,{data}"

    form = UpdateForm()
    bal_form = BalanceForm()
    filter_form = PurchaseHistoryForm()
    delete = DeleteForm()
    deleteRating = RatingDeleteForm()

    if reviewUID is not None and reviewPID is not None:
        Review.delete_review(reviewUID, reviewPID)
        return redirect(url_for('users.updateAccount'))

    if ratingUID is not None and ratingSID is not None:
        Rating.delete_rating(ratingUID, ratingSID)
        return redirect(url_for('users.updateAccount'))

    category, search = 'All', ''
    
    if filter_form.submit.data:
        category = filter_form.category.data
        search = filter_form.search.data

    purchases = Purchase.get_purchase_history(current_user.id, category, search)
    reviews = Review.get_by_uid(current_user.id)
    ratings = Rating.get_by_uid(current_user.id)

    if form.validate_on_submit():
        User.userUpdate(current_user.id, form.firstname.data, form.lastname.data, form.email.data, form.address.data, form.password.data)
        return redirect(url_for('users.updateAccount'))

    if bal_form.validate_on_submit():
        print('balance')
        User.changeBalance(current_user.id, current_user.balance, bal_form.deposit.data, bal_form.withdrawl.data)
        return redirect(url_for('users.updateAccount'))

    print('check')
    return render_template('user_page.html', title='User Info', form=form, bal_form=bal_form, filter_form = filter_form, purchases=purchases, sells=sells, isSeller = isSeller, reviews = reviews, ratings = ratings, myImg = myImg, delete = delete, deleteRating = deleteRating)




#Show Public View
@bp.route('/public_view/<int:uid>', methods=['GET', 'POST'])
def showPublicView(uid):
    isSeller = User.isSeller(uid)
    user_view = User.get(uid)
    form = WriteRating()
    time_reviewed = datetime.datetime.now()
    feedback = Rating.get_seller_ratings(uid)
    average = Rating.get_seller_avg(uid)
    count = Rating.get_seller_count(uid)
    isSeller = User.isSeller(current_user.id)

    #See if the rating is submitted, check its validity, then check if it exists already, and either replace it or submit a new one
    if form.validate_on_submit() and current_user.is_authenticated:
        if Rating.check_purchase(current_user.id, uid) or form.stars.data > 5 or form.stars.data < 1:
            print('invalid')
        elif Rating.check_rating(current_user.id, uid):
            Rating.update_rating(current_user.id, uid, form.stars.data, form.rating.data, time_reviewed)
            return render_template('public_view.html', title='User Info', user_view = user_view, isSeller = isSeller, form = form, feedback = feedback, average = average, count = count)
        else:
            Rating.write_rating(current_user.id, uid, form.stars.data, form.rating.data, time_reviewed)
            return render_template('public_view.html', title='User Info', user_view = user_view, isSeller = isSeller, form = form, feedback = feedback, average = average, count = count)

    return render_template('public_view.html', title='User Info', user_view = user_view, isSeller = isSeller, form = form, feedback = feedback, average = average, count = count)

#Write a New Seller Rating
class WriteRating(FlaskForm):
    stars = IntegerField('Stars', validators=[DataRequired()])
    rating = StringField('Rating', validators=[DataRequired()])
    submit = SubmitField('Submit')
