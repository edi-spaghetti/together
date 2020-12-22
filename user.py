from dummy_db import db


class User:

    def __init__(self, idx):
        self.id = idx

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @classmethod
    def get(cls, user_id):

        if not isinstance(user_id, str):
            print(f'User Id must be unicode - got {type(user_id)}')

        if user_id in db['user']:
            return User(user_id)
        else:
            print(f'Invalid user id {user_id}')
