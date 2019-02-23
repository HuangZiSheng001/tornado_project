import time
import threading

# yield装  send发
# 在tornado里面，它把这些方式封装成了装饰器
# 当我们想用异步的时候，只需要加上这些装饰器，就可以把代码变成异步
# epoll加协程，异步非阻塞框架，tornado





def func_01(on_finish):
    def inner(on_finish):
        print('---start---')

        # 模拟阻塞
        time.sleep(5)

        print('---end---')

        yield 'hello world'

    threading.Thread(target=inner, args=(on_finish, )).start()



# 原本是用return返回数据，但是它有瓶颈，现在我们用一个函数来返回数据

def on_finish(result):
    print(result)




func_01(on_finish)
time.sleep(2)
print('---b---')