import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


USERNAME = 'root'
PASSWORD = 'root'
DATABASE_IP = '127.0.0.1'
DATABASE_PORT = '3306'
DATABASE_NAME = 'tornado_project'

Db_url = 'mysql+pymysql://{username}:{password}@{ip}:{port}/{db_name}?charset=utf8'.format(
    username=USERNAME,
    password=PASSWORD,
    ip=DATABASE_IP,
    port=DATABASE_PORT,
    db_name=DATABASE_NAME,
)



# 连接数据库
engine = create_engine(Db_url)

# 建模要使用继承来建立基类
Base = declarative_base(engine)

# 生成一个会话类，用来操作数据
Session = sessionmaker(engine)

session = Session()



if __name__ == '__main__':
    try:
        # 连接数据库
        connection = engine.connect()
        result = connection.execute('select 1')
        if result:
            print('connect success')
            print(result.fetchone())
    except Exception as ex:
        print(ex)
