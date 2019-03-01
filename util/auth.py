'''
验证用户登录的账户信息
'''


import hashlib


def hashed(text):
    """
    :param text:
    :return:
    """
    return hashlib.md5(text.encode('utf-8')).hexdigest()


USER_DATA = {
    'name': 'root',
    'password': hashed('root'),
}


def authenticate(username, password):
    """
    检查用户名和密码是否匹配
    :param username:
    :param password:
    :return: 是否登陆成功
    """
    if username and password:
        is_match = (username == USER_DATA['name']) and (hashed(password) == USER_DATA['password'])
        return is_match

    # 账号密码为空则返回错
    return False


if __name__ == '__main__':
    my_text = 'asdasdasasd'
    print(hashed(my_text))