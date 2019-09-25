#多线程例子

from multiprocessing.dummy import Pool

def calc_power2(num):
    return num * num

pool = Pool(3)

origin_num = [x for x in range(11)]
result = pool.map(calc_power2, origin_num)
print(f'计算1-10的平方根分别为:{result}')