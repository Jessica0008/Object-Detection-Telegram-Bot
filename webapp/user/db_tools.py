from webapp.user.user import User

def get_auth_user(db, user_id):
    print(user_id)
    user = db.auth_users.find_one({"id": user_id})
    if user is None:
        return None
    print(user)
    result = User(user['username'], user['role'])
    result.set_password(user['password'])
    return result