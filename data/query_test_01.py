# 导入会话类
from connect import session

# 针对User表
from user_modules import User



# 列表
rs_01 = session.query(User).all()

# 查询第一条
rs_02 = session.query(User).first()

# 条件查询   filter   filter_by
rs_03 = session.query(User).filter(User.username == '黄梓晟').all()

print(rs_01)
print('-'*100)

print(rs_02)
print('-'*100)

print(rs_03)
print('-'*100)


print(rs_02.username)
print('-'*100)

print(hasattr(rs_02, 'username'))
print(getattr(rs_02, 'username'))

# my_list = [1,2,3,4,5,6,]


# 通配符 %   like   notlike
print('-'*100)
rs_04 = session.query(User).filter(User.username.like('%梓%')).all()
print(rs_04)


print('-'*100)
rs_05 = session.query(User).filter(User.username.notlike('%梓%')).all()
print(rs_05)


# is_    isnot
print('-'*100)
rs_05 = session.query(User).filter(User.username.is_(None)).all()
print(rs_05)

print('-'*100)
rs_06 = session.query(User).filter(User.username.isnot(None)).all()
print(rs_06)


# in_   notin_
print('-'*100)
rs_07 = session.query(User).filter(User.username.in_(['黄梓晟', '喵喵喵', ])).all()
print(rs_07)


print('-'*100)
rs_08 = session.query(User).filter(User.username.notin_(['黄梓晟', '喵喵喵', ])).all()
print(rs_08)


# limit 限制数量查询
print('-'*100)
rs_09 = session.query(User.username).limit(3).all()
print(rs_09)



# offset 偏移量 排除前三个
print('-'*100)
rs_10 = session.query(User.username).offset(3).all()
print(rs_10)


# slice 切片
print('-'*100)
rs_10 = session.query(User.id).slice(0,5).all()
print(rs_10)


# one 只能查不重复的，唯一的，否则会报错
print('-'*100)
rs_10 = session.query(User).filter(User.id == '12').one()
print(rs_10)


# 排序 order_by
from sqlalchemy import desc
print('-'*100)
rs_11 = session.query(User.username, User.id).filter(User.username != '呜呜呜').order_by(desc(User.id)).limit(3).all()
print(rs_11)



# 聚合函数
# 分组查询一般情况下和聚合函数一起使用   having
print('-'*100)
from sqlalchemy import func, extract, or_


print('-'*100)
rs_12 = session.query(User.password, func.count(User.id)).having(func.count(User.id > 1)).group_by(User.id).all()
print(rs_12)


print('-'*100)
rs_13 = session.query(User.password, func.min(User.id)).group_by(User.id).all()
print(rs_13)


print('-'*100)
rs_14 = session.query(User.password, func.max(User.id)).group_by(User.id).all()
print(rs_14)


print('-'*100)
rs_15 = session.query(User.password, func.sum(User.id)).group_by(User.id).all()
print(rs_15)

print('-'*100)
# label 取别名    extract 提取数据中内容
rs_16 = session.query(
    extract('minute', User.create_time).label('minute'),
    func.count(User.id),
).group_by('minute').all()
print(rs_16)


print('-'*100)
rs_17 = session.query(User).filter(or_(User.password == 'qwe123', User.id == '12')).all()
print(rs_17)

