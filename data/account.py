from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.sql import exists
from sqlalchemy import or_, and_
from sqlalchemy.orm import relationship


from datetime import datetime

from .db import Base, DBSession


session = DBSession()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    telephone = Column(String(15), nullable=False, unique=True)
    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    create_time = Column(DateTime, default=datetime.now)



    def __repr__(self):
        return """<User(id={}, username={}, telephone={},password={}>""".format(
            self.id,
            self.telephone,
            self.username,
            self.password,
        )


    @classmethod
    def add_user(cls, telephone, username, hashed_password):
        '''
        添加用户的函数
        :param username: 用户名
        :param telephone: 手机号码
        :param hashed_password: 已经加密过的密码
        :return: None
        '''
        user = User(telephone=telephone, username=username, password=hashed_password)

        session.add(user)

        session.commit()


    # 通过telephone获取username
    @classmethod
    def get_username_by_telephone(cls, telephone):
        user = session.query(cls).filter(cls.telephone == telephone).first()
        return user.username


    # 核对telephone和password
    @classmethod
    def check_password(cls, telephone, hashed_password):
        user = session.query(cls).filter(cls.telephone == telephone).filter(cls.password == hashed_password).first()

        if user:
            return True

        return False


    # 检查该号码是否已经注册过
    @classmethod
    def is_exists(cls, telephone):
        return session.query(exists().where(User.telephone == telephone)).scalar()



'''

class User(Base):
    #建立一个User模型

    # 固定写法
    __tablename__ = 'user'


    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20))
    password = Column(String(20))
    create_time = Column(DateTime, default=datetime.now())
    _locked = Column(Boolean, default=False, nullable=False)


    def __repr__(self):
        return """<User(id={}, username={}, password={}, create_time={}, locked={})>""".format(
            self.id,
            self.username,
            self.password,
            self.create_time,
            self._locked
        )

    @classmethod
    def get_name(cls, user):
        return session.query(cls).filter(cls.username == user).first()

'''


if __name__ == '__main__':

    # 测试用例
    telephone = '12345678910'
    username = 'root'
    password = 'root'

    my_user = User()
    print(User.is_exists(telephone=telephone))
    print(User.get_username_by_telephone(telephone=telephone))