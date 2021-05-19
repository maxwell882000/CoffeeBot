from application import app, db
from application.core.models import UserAdmin


@app.cli.command()
def createsuperuser():
    """Create superuser for administration panel"""
    email = input("Type user email: ")
    password = input("Type super user password (don't tell it anyone else): ")
    user_admin = UserAdmin(email=email)
    user_admin.set_password(password)
    db.session.add(user_admin)
    db.session.commit()
    print('Superuser {} created!'.format(email))
