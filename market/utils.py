import hashlib

from market.models import User

def get_user_by_id(user_id):
    return User.query.get(user_id)


def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        # bam mat khau de so sanh voi csdl

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()

