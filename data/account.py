from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.sql import exists
from sqlalchemy import or_, and_
from sqlalchemy.orm import relationship


from datetime import datetime

from .db import Base, DBSession


session = DBSession()


# 用户信息表
class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telephone = Column(String(15), nullable=False, unique=True)
    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    create_time = Column(DateTime, default=datetime.now)

    # 对posts表的引用，注意要双向引用
    posts = relationship('Post', back_populates='user')

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

    @classmethod
    def get_user_by_telephone(cls, telephone):
        '''
        通过telephone获取username
        :param telephone:
        :return: username
        '''
        user = session.query(cls).filter(cls.telephone == telephone).first()
        return user



    @classmethod
    def check_password(cls, telephone, hashed_password):
        '''
        核对telephone和password
        :param telephone:
        :param hashed_password:
        :return: bool
        '''
        user = session.query(cls).filter(cls.telephone == telephone).filter(cls.password == hashed_password).first()
        if user:
            return True
        return False



    @classmethod
    def is_exists(cls, telephone):
        '''
        检查该号码是否已经注册过
        :param telephone:
        :return: bool
        '''
        return session.query(exists().where(User.telephone == telephone)).scalar()


# 用户图片信息
class Post(Base):

    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String(200))
    thumb_url = Column(String(200))

    user_id = Column(Integer, ForeignKey('user.id'))

    # 对user表的引用
    user = relationship('User', back_populates='posts')

    def __repr__(self):
        return f'<Post(id={self.id}, image_url={self.image_url},\
         thumb_url={self.thumb_url}, user_id={self.user_id}, user={self.user})>'


class Like(Base):
    """
    用户喜欢图片的信息
    """
    __tablename__ = "likes"
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False, primary_key=True)

    def __repr__(self):
        return f"""<Like(user_id={self.user_id}, post_id={self.post_id})>"""



if __name__ == '__main__':

    # 测试用例
    '''
     telephone = '12345678910'
    username = 'root'
    password = 'root'

    my_user = User()
    print(User.is_exists(telephone=telephone))
    print(User.get_username_by_telephone(telephone=telephone))
    '''
    # 创建表格(谨慎使用，要注意数据库版本规范)
    Base.metadata.create_all()

