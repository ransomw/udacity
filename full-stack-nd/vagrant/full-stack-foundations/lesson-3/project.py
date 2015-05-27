from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import redirect
from flask import flash
from flask import jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base
from database_setup import Restaurant
from database_setup import MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# valid types for url: int, string, path

@app.route('/')
@app.route('/hello')
def hello_world():
    return "Hiya!"

@app.route('/restaurants/<int:restaurant_id>/')
def menu_items(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(
        id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant.id)
    return render_template('menu.html',
                           restaurant=restaurant,
                           items=items)
    # return '\n'.join(
    #     [' : '.join([item.name,
    #                  item.price,
    #                  item.description]) +'<br>'
    #      for item in items])

@app.route('/restaurants/<int:restaurant_id>/new/',
           methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'],
                           restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New menu item created")
        return redirect(url_for('menu_items',
                                restaurant_id=restaurant_id))
    else:
        return render_template('new_menu_item.html',
                               restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/',
           methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(
        id=menu_id).one()
    if request.method == 'POST':
        item.name = request.form['name']
        session.add(item)
        session.commit()
        flash("Edited menu item")
        return redirect(url_for('menu_items',
                                restaurant_id=restaurant_id))
    else:
        return render_template('edit_menu_item.html',
                               restaurant_id=restaurant_id,
                               menu_item=item)



@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/',
           methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(
        id=menu_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Deleted menu item")
        return redirect(url_for('menu_items',
                                restaurant_id=restaurant_id))
    else:
        return render_template('delete_menu_item.html',
                               restaurant_id=restaurant_id,
                               menu_item=item)


@app.route('/restaurants/<int:restaurant_id>/JSON')
def menu_items_json(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(
        id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant.id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
