
'''
使用场景一：　　

　　Generator可用于产生数据流， generator并不立刻产生返回值，
而是等到被需要的时候才会产生返回值，相当于一个主动拉取的过程(pull)，比如现在有一个日志文件，
每行产生一条记录，对于每一条记录，不同部门的人可能处理方式不同，但是我们可以提供一个公用的、按需生成的数据流。

'''

'''
gen_words gen_data_from_file是数据生产者，而count_words count_total_chars是数据的消费者。
可以看到，数据只有在需要的时候去拉取的，
而不是提前准备好。另外gen_words中 (w for w in line.split() if w.strip()) 也是产生了一个generator
'''
def gen_data_from_file(file_name):
    with open(file_name, 'r') as file:
        for line in file:
            yield line


def gen_words(line):
    for word in (w for w in line.split() if w.strip()):
        yield word


def count_words(file_name):
    word_map = {}
    for line in gen_data_from_file(file_name):
        for word in gen_words(line):
            if word not in word_map:
                word_map[word] = 0
            word_map[word] += 1
    return word_map


def count_total_chars(file_name):
    total = 0
    for line in gen_data_from_file(file_name):
        total += len(line)
    return total


if __name__ == '__main__':
    print(count_words('test.txt'), count_total_chars('test.txt'))