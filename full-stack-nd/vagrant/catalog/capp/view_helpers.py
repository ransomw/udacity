from pdb import set_trace as st

import os
import imghdr

from wtforms.ext.sqlalchemy.orm import model_form
from wtforms.validators import ValidationError

from models import session
from models import User
from models import Item

from capp import app

def get_create_user(name, email):
    """ get or create user record """
    try:
        user = session.query(User).filter_by(
            email=email).one()
    # todo: catch specific sqlalchemy exception
    except:
        new_user = User(name=name,
                        email=email)
        session.add(new_user)
        session.commit()
        user = session.query(User).filter_by(
            email=email).one()
    return user.id


def item_from_form(item, form, user_id=None,
                   save=True):
    item.title = form['title']
    item.description = form['description']
    item.category_id = form['category']
    if user_id is not None:
        item.user_id = user_id
    if save:
        session.add(item)
        session.commit()
    # query in order to have id set
    return session.query(Item).filter_by(
        title=form['title']).one()


def get_item_image_filepath(item_id):
    return os.path.join(
        app.config['ITEM_IMG_DIR'], str(item_id))


def get_item_image_info(item_id):
    filepath = get_item_image_filepath(item_id)
    if not os.path.isfile(filepath):
        return None
    img_type = imghdr.what(filepath)
    return {
        'path': filepath,
        'type': img_type
    }

class NotBlank(object):
    """ Custom wtforms validator to make sure text fields
    are non-empty """
    def __init__(self):
        pass

    def __call__(self, form, field):
        if (field.data is not None and
            field.data.strip() == ''):
            raise ValidationError((
                "{label} may not be blank"
                ).format(label=field.label.text))

ItemForm = model_form(
    Item,
    db_session=session,
    only=[
        'title',
        'description',
        'category',
    ],
    # ??? duplicate validation ok?
    field_args={
        'description': {'validators': [NotBlank(),],},
    })
