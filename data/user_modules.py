from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from .connect import Base
from datetime import datetime
from sqlalchemy.orm import relationship


from .connect import session


class User(Base):
    '''建立一个User模型'''

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


class UserDetails(Base):
    __tablename__ = 'user_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_card = Column(Integer, nullable=True, unique=True)
    lost_login = Column(DateTime)
    login_num = Column(Integer, default=0)

    # 外键在Userdetails里，用UserDetails查询User，为正向查询
    user_id = Column(Integer, ForeignKey('User.id'))

    # 使用的为类名，是模型的名字,  uselist为假时表示一对一
    userdetail = relationship('User', backref='details', uselist=False, cascade='all')


    def __repr__(self):
        return """<UserDetails(id={}, id_card={}, lost_login={}, login_num={}, user_id={})>""".format(
            self.id,
            self.id_card,
            self.lost_login,
            self.login_num,
            self.user_id,
        )


user_article = Table('user_article', Base.metadata,
    # 联合主键
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('article_id', Integer, ForeignKey('article.id'), primary_key=True),
)



class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(500), nullable=True)
    create_time = Column(DateTime, default=datetime.now)

    article_user = relationship('User', backref='articles', secondary=user_article)


    def __repr__(self):
        return 'Article(id={}, content={}, create_time={})'.format(
            self.id,
            self.content,
            self.create_time
        )


if __name__ == '__main__':

    # 创建表格
    Base.metadata.create_all()
