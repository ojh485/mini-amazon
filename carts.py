from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import datetime

from .models.cart import Cart, Order

from flask import Blueprint
bp = Blueprint('carts', __name__)


class QuantForm(FlaskForm):
    product = StringField('Product Name', validators=[DataRequired()])
    quantity = IntegerField('New Quantity', validators=[DataRequired()])
    submit = SubmitField('Update')

class RemoveForm(FlaskForm):
    product = StringField('Product Name', validators=[DataRequired()])
    submit = SubmitField('Remove')

@bp.route('/cart.html', methods=['GET', 'POST'])
def findCart():
    if current_user.is_authenticated:
        u = current_user.id   
        carts = Cart.get_by_uid(u)
        purchases = Order.get_orders_by_uid(u)
        total = Cart.get_total(u)
    else:
        carts = []
        purchases = []
        total = 0

    rem_form = RemoveForm()
    quant_form = QuantForm()

    if quant_form.validate_on_submit():
        print('2')
        Cart.changeQuantity(quant_form.product.data, quant_form.quantity.data, current_user.id)
        return redirect(url_for('carts.findCart'))
    elif rem_form.validate_on_submit():
        print('1')
        Cart.deleteItem(rem_form.product.data, current_user.id)
        return redirect(url_for('carts.findCart'))
    
    return render_template('cart.html', title='My Cart', carts=carts, total=total, quant_form=quant_form, rem_form=rem_form, purchases=purchases)


@bp.route('/orderCart')
def orderCart():
    Cart.placeOrder(current_user.id  )
    return redirect(url_for('carts.findCart'))

@bp.route('/order_page/<int:uid>/<time>', methods=['GET', 'POST'])
def order_page(uid=None, time=None):
    order = Order.get_order(uid, time)
    return render_template('order_page.html', title='Order Page', order=order, date=time.split()[0], tod=time.split()[1])