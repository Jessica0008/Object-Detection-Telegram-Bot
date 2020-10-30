from webapp.user.user import User

def get_auth_user(db, user_id):
    user = db.auth_users.find_one({"id": user_id})
    if not user:
        return None
    result = User(user.username, user.role)
    result.set_password(user.password)
    return result