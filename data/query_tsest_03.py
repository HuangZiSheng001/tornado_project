from sqlalchemy.orm import relationship



from connect import session

# 针对User表
from user_modules import User
from user_modules import UserDetails




if __name__ == '__main__':
    # id为3的数据
    row = session.query(User).get(3)
    print(row)
    print(dir(row))
    print(row.username)