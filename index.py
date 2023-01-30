from email.policy import default
from flask import render_template
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FloatField, DecimalField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired, NumberRange
import datetime

from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/<category>/<int:pageNum>/<sort>/<float:minRating>/<float:maxPrice>', methods=['GET', 'POST'])
@bp.route('/<searchResult>/<category>/<int:pageNum>/<sort>/<float:minRating>/<float:maxPrice>', methods=['GET', 'POST'])
def index(searchResult = '', category = 'All', pageNum = 1, sort = 'pid', minRating = 0.0, maxPrice = 101):

    #to avoid crash due to negative numbers
    if pageNum <= 0:
        pageNum = 1


    # get all available products for sale:
    products = Product.get_all(True)
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0)
        )
        rec = Purchase.get_recommendations(current_user.id)
    else:
        purchases = None
        rec = []

    print(rec)
    #returning products user searched for by name
    searchForm = keywordForm()
    categoryForm = categorySelect()
    ratingForm = ratingFilter()
    next = nextPage()
    prev = prevPage()
    priceSort = sortPrice()
    ratingButton = sortRating()
    ratingSort = ratingFilter()
    filterPrice = priceFilter()

    if searchForm.validate_on_submit():
        # if a category is selected: filter by category
        searchResult = searchForm.search.data
    


    if categoryForm.category.data is not None:
        category = categoryForm.category.data

    if ratingForm.minRating.data is not None:
        minRating = ratingSort.minRating.data
    
    if filterPrice.maxPrice.data is not None:
        maxPrice = filterPrice.maxPrice.data
    
    products = Product.keySearch(searchResult, category, pageNum, sort, minRating, maxPrice)

    

    # render the page by adding information to the index.html file
    return render_template('index.html', avail_products=products, purchase_history=purchases, rec = rec, form=searchForm, searchResult = searchResult, category = category, categoryForm = categoryForm, pageNum = pageNum, nextPage = next, prevPage = prev,
    priceSort = priceSort, minRating = minRating, ratingSort = ratingSort, sort = sort, ratingButton = ratingButton, maxPrice = maxPrice, filterPrice = filterPrice)

#search function
class keywordForm(FlaskForm):
    search = StringField('Search Products by Name:', validators=[DataRequired()])
    submit = SubmitField('Search')

# 'choices' are taken from gen.py, with 'All' added
class categorySelect(FlaskForm):
    category = SelectField(label = 'Filter By Category:', choices=['All', 'Home & Kitchen', 'Beauty & Personal Care', 'Toys & Games', 'Clothing, Shoes & Jewelry',
'Health, Household & Baby Care', 'Sports & Outdoors', 'Arts, Crafts & Sewing', 'Books', 'Kitchen & Dining', 'Electronics']
, validators=[DataRequired()])
    submit = SubmitField('Filter')


#implementing pagination
class nextPage(FlaskForm):
    submit = SubmitField('Next')

class prevPage(FlaskForm):
    submit = SubmitField('Prev')

#implementing sort by price
class sortPrice(FlaskForm):
    submit = SubmitField('Price')

class sortRating(FlaskForm):
    submit = SubmitField('Average Rating')

class ratingFilter(FlaskForm):
    minRating = DecimalField('Minimum Product Rating:', validators=[NumberRange(min=0)])
    submit = SubmitField('Filter')

class priceFilter(FlaskForm):
    maxPrice = DecimalField('Maximum Price:', validators=[NumberRange(min=0)])
    submit = SubmitField('Filter')