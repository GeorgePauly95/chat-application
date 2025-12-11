def check_user(username, UserAccount, connection):
    registerd_users = [user[0] for user in UserAccount.showall_users(connection)]
    if username in registerd_users:
        return True
    return False
