# 导入会话类
from connect import session

# 针对User表
from user_modules import User
from user_modules import UserDetails


# 多表查询


# 笛卡尔积
print('-'*100)
rs_01 = session.query(User, UserDetails).filter(User.id == UserDetails.user_id).all()
print(rs_01)


# 内连接join
print('-'*100)
rs_02 = session.query(
    User.username,
    UserDetails.lost_login,
).join(
    UserDetails,
    UserDetails.id == User.id,
).filter(UserDetails.id == User.id).all()

print(rs_02)


# 外连接outjoin
print('-'*100)
rs_03 = session.query(
    User.username,
    UserDetails.lost_login,
).outerjoin(
    UserDetails,    # 以第一张表为基准
    UserDetails.id == User.id,
).all()

print(rs_02)



# union联合  去重
print('-'*100)
q1 = session.query(User.id)
q2 = session.query(UserDetails.id)
print(q1.union(q2).all())


# 嵌套查询  子查询

# 声明子表
sql_01 = session.query(UserDetails.lost_login).subquery()

# 默认使用笛卡尔积连接
print(session.query(User, sql_01.c.lost_login).all())



# 原生查询

sql_02 = """
    select * from user
"""

# 可用for迭代查询
rows_01 = session.execute(sql_02)

# 查询一条
print('-'*100)
print(rows_01.fetchone())

# 查询许多
print('-'*100)
print(rows_01.fetchmany())

# 查询所有
print('-'*100)
print(rows_01.fetchall())