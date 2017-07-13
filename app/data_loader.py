from app.models import User


def load_data(db):
    u = User(username='fulano')
    db.session.add(u)
    db.session.commit()
