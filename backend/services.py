def get_user_details(username, UserAccount, connection):
    user_details = UserAccount.get_user_details(username, connection)
    if user_details is None:
        return False
    user_id, username = user_details[2:4]
    return {"user_id": user_id, "username": username}
