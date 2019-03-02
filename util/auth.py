'''
管理用户账户信息的模块
'''

import hashlib

from data.account import User



# 密码加密函数
def hashed(text):
    """
    :param text:
    :return: 加密的text
    """
    return hashlib.md5(text.encode('utf-8')).hexdigest()



# 检查用户登录的teleph one和password是否对应
def authenticate(telephone, raw_password):
    """
    检查用户名和密码是否匹配
    :param raw_password: 未加密的密码
    :param telephone: 电话
    :return: 是否登陆成功的bool
    """
    if telephone and raw_password:
        return User.check_password(telephone=telephone, hashed_password=hashed(raw_password))

    return False


#  注册信息正确后，把新注册的账户加入到数据库中
def regist(username, telephone, raw_password):
    if not User.is_exists(telephone=telephone):
        User.add_user(username=username, telephone=telephone, hashed_password=hashed(raw_password))
        return {'msg': 'ok'}
    else:
        return {'msg': 'This number has been registered.'}


# bool值  检查是否存在该用户
def is_exsist_user(telephone):
    if User.get_username_by_telephone(telephone=telephone):
        return True
    else:
        return False




if __name__ == '__main__':

    regist(telephone='12345678911', username='jjj', raw_password='kkk')

    my_telephone = '12345678910'
    my_password = 'root'

    print(authenticate(telephone='12345678910', raw_password='root'))
    print(authenticate(telephone='12345678911', raw_password='kkk'))

    print(is_exsist_user(telephone=my_telephone))