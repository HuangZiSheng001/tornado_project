from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from .connect import Base, session
from datetime import datetime
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    telephone = Column(String(15), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)

    def __init__(self, *args, **kwargs):
        telephone = kwargs.get('telephone')
        username = kwargs.get('username')
        password = kwargs.get('password')

        self.telephone = telephone
        self.username = username
        self.password = password


    def __repr__(self):
        return """<User(id={}, username={}, telephone={},password={}>""".format(
            self.id,
            self.telephone,
            self.username,
            self.password,
        )


    def check_password(self, raw_password):
        # result = check_password_hash(self.password, raw_password)
        result = True
        return result



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