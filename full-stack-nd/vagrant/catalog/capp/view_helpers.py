from models import session
from models import User


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
    return item
