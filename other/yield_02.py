# -*- coding:utf-8 -*-
import sys
# import Timer
import types
import time

class YieldManager(object):
    def __init__(self, tick_delta = 0.01):
        self.generator_dict = {}
        # self._tick_timer = Timer.addRepeatTimer(tick_delta, lambda: self.tick())

    def tick(self):
        cur = time.time()
        for gene, t in self.generator_dict.items():
            if cur >= t:
                self._do_resume_genetator(gene,cur)

    def _do_resume_genetator(self,gene, cur ):
        try:
            self.on_generator_excute(gene, cur)
        except StopIteration as e:
            self.remove_generator(gene)
        except Exception as e:
            print('unexcepet error', type(e))
            self.remove_generator(gene)

    def add_generator(self, gen, deadline):
        self.generator_dict[gen] = deadline

    def remove_generator(self, gene):
        del self.generator_dict[gene]

    def on_generator_excute(self, gen, cur_time = None):
        t = gen.next()
        cur_time = cur_time or time.time()
        self.add_generator(gen, t + cur_time)

g_yield_mgr = YieldManager()

def yield_dec(func):
    def _inner_func(*args, **kwargs):
        gen = func(*args, **kwargs)
        if type(gen) is types.GeneratorType:
            g_yield_mgr.on_generator_excute(gen)

        return gen
    return _inner_func

@yield_dec
def do(a):
    print('do', a)
    yield 2.5
    print('post_do', a)
    yield 3
    print('post_do again', a)


if __name__ == '__main__':
    do(1)
    for i in range(1, 10):
        print ('simulate a timer, %s seconds passed' % i)
        time.sleep(1)
        g_yield_mgr.tick()


'''
使用场景二：

　　一些编程场景中，一件事情可能需要执行一部分逻辑，然后等待一段时间、或者等待某个异步的结果、
或者等待某个状态，然后继续执行另一部分逻辑。比如微服务架构中，服务A执行了一段逻辑之后，去服务B请求一些数据，
然后在服务A上继续执行。或者在游戏编程中，一个技能分成分多段，先执行一部分动作（效果），然后等待一段时间，
然后再继续。
对于这种需要等待、而又不希望阻塞的情况，我们一般使用回调（callback）的方式。下面举一个简单的例子：
'''