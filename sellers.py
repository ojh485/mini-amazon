from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask import render_template
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SubmitField, HiddenField
from wtforms.validators import DataRequired, NumberRange

from .models.sells import Inventory

from flask import Blueprint
bp = Blueprint('sellers', __name__)

#forms to be used in lower functions
class AddProduct(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    category = StringField('Category', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()], description= 'Enter a short description')
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    image = StringField('Product Image', validators=[DataRequired()], description= 'Enter URL link to product image')
    submit = SubmitField('Submit')

class ChangeQuantity(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')

class DeleteItem(FlaskForm):
    submit = SubmitField('Delete Product')

class SearchForm(FlaskForm):
    search = StringField('Search Orders', validators=[DataRequired()])
    submit = SubmitField('Submit')

class FulfillOrder(FlaskForm):
    submit = SubmitField('Fulfill')

#bps
@bp.route('/seller_home_page', methods = ['GET', 'POST'])
@bp.route('/seller_home_page/<int:purchaseID>', methods=['GET', 'POST'])
def seller_home_page(purchaseID=None):
    searchForm = SearchForm()
    fulfill = FulfillOrder()

    if current_user.is_authenticated:
        inventory = Inventory.get_seller_inventory(current_user.id)

        #pull and display orders from Purchases
        orders = Inventory.get_seller_orders(current_user.id)

        if searchForm.validate_on_submit():
            orders = Inventory.get_limited_seller_orders(current_user.id, searchForm.search.data)

    else:
        inventory = None
        orders = None
     
    if fulfill.validate_on_submit and purchaseID is not None:
        Inventory.fulfillorder(purchaseID)

    return render_template('inventorypage.html', inventory=inventory, orders=orders, searchForm=searchForm, fulfill=fulfill)


#function to edit and delete an inventory items
@bp.route('/editInventory/<int:id>', methods = ['GET', 'POST'])
def editInventory(id):
    #editing/delete methods
    form = ChangeQuantity()
    item = Inventory.get_item_by_id(current_user.id, id)
    deleteItem = DeleteItem()

    if form.validate_on_submit():
        Inventory.changequantity(id, form.quantity.data)
        return redirect(url_for('sellers.seller_home_page'))
    elif deleteItem.validate_on_submit():
        Inventory.deleteinventory(id)
        return redirect(url_for('sellers.seller_home_page'))
    
    #display form of inventory
    return render_template('editproduct.html', form=form, deleteItem=deleteItem, item=item)
    

#function to add a new product
@bp.route('/addproduct', methods = ['GET', 'POST'])
def addproduct():
    uid = current_user.id
    form = AddProduct()
    if form.validate_on_submit():
        #should check if item name already exists, ask if it's the same?
        if Inventory.add_item(uid, form.name.data, form.price.data, form.category.data,
                                form.description.data, form.quantity.data, form.image.data):
            return redirect(url_for('sellers.seller_home_page'))
    return render_template('addproduct.html', form=form)
