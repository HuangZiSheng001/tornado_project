# 导入会话类

from .connect import session

# 针对User表
from .user_modules import User




def add_user():
    # 添加多条
    session.add_all(
        [
            User(username='黄梓晟', password='qwe123'),
            User(username='喵喵喵', password='qwe123'),
            User(username='呜呜呜', password='qwe123'),
        ]
    )

    # 添加一条
    # person = User(username='hzs', password='qwe123')
    # session.add(person)

    # 提交事务
    session.commit()


"""查看数据"""
def search_user():

    # 查询所有
    rows = session.query(User).all()

    # 查看第一条
    row = session.query(User).first()





if __name__ == '__main__':
    add_user()