"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""


from flask import Flask, render_template, redirect, flash, session, request
import jinja2

import os

import melons, customers


app = Flask(__name__)

# A secret key is needed to use Flask sessioning features

app.secret_key = os.environ['SECRET_KEY']

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route('/')
def index():
    """Return homepage."""

    return render_template('homepage.html')


@app.route('/melons')
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template('all_melons.html',
                           melon_list=melon_list)


@app.route('/melon/<melon_id>')
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print melon
    return render_template('melon_details.html',
                           display_melon=melon)


@app.route('/cart')
def show_shopping_cart():
    """Display content of shopping cart."""

    cart = []
    cart_total = 0

    if 'cart' in session:
        for melon_id, quantity in session['cart'].iteritems():
            melon = melons.get_by_id(melon_id)
            melon.quantity = quantity
            melon.total = quantity * melon.price

            cart.append(melon)
            cart_total += melon.total
    else:
        flash('You have no items in your shopping cart!')

    return render_template('cart.html',
                           cart=cart,
                           cart_total=cart_total)


@app.route('/add_to_cart/<melon_id>')
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""

    if 'cart' in session:
        session['cart'][melon_id] = session['cart'].get(melon_id, 0) + 1
    else:
        session['cart'] = {melon_id: 1}

    flash('A {} was added to your cart!'.format(
        melons.get_by_id(melon_id).common_name
    ))

    return redirect('/cart')


@app.route('/login', methods=['GET'])
def show_login():
    """Show login form."""

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    email = request.form.get('email')
    password = request.form.get('password')

    try:
        customer = customers.get_by_email(email)
    except:
        flash('A user with that email does not exist. Try again.')
        return redirect('/login')

    if customer.is_hashed_password(password):
        session['user'] = email
        flash('Welcome, {}!'.format(customer.first_name))
        return redirect('/melons')
    else:
        flash('Invalid password for {}'.format(email))
        return redirect('/login')


@app.route('/logout')
def process_logout():
    """Log user out of site.

    Destroys session['user'].
    """

    del session['user']
    flash('You have logged out. Goodbye!')

    return redirect('/melons')


@app.route('/checkout')
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash('Sorry! Checkout will be implemented in a future version.')
    return redirect('/melons')


if __name__ == '__main__':
    app.run(debug=True)
