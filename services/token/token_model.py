

class Token:

    def __init__(self, user_id, token=None, update_time=None):
        self.user_id = user_id
        self.token = token
        self.update_time = update_time

    def to_json(self):
        return {
            'user_id': self.user_id,
            'token': self.token,
            'update_time': self.update_time
        }
