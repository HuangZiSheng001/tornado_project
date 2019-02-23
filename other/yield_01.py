def gen_generator():
    yield 1


def gen_value():
    return 1

'''
从上面的代码可以看出，gen_generator函数返回的是一个generator实例，generator有以下特别：

遵循迭代器（iterator）协议，迭代器协议需要实现__iter__、next接口
能过多次进入、多次返回，能够暂停函数体中代码的执行
'''

if __name__ == '__main__':
    ret = gen_generator()
    print(ret, type(ret))

    # <generator object gen_generator at 0x02645648> <type 'generator'>

    ret = gen_value()

    print(ret, type(ret))
    # 1 <type 'int'>



'''
>>> def gen_example():
...     print 'before any yield'
...     yield 'first yield'
...     print 'between yields'
...     yield 'second yield'
...     print 'no yield anymore'
... 
>>> gen = gen_example()
>>> gen.next()　　　　＃ 第一次调用next
before any yield
'first yield'
>>> gen.next()　　　　＃ 第二次调用next
between yields
'second yield'
>>> gen.next()　　　　＃ 第三次调用next
no yield anymore
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteratio
'''