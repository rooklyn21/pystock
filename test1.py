# 给定一个非负整数 c ，你要判断是否存在两个整数 a 和 b，使得 a2 + b2 = c。

# 思路：
# 对C的平方根取整，设为n
# 如果n<=1，返回false；
# i从n到1循环，m=c-i*i，
#     如果m开平方是整数，返回true，[n,m]
#     否则继续循环。
from math import *
import time

def get_time(f):

    def inner(*arg,**kwarg):
        s_time = time.time()
        res = f(*arg,**kwarg)
        e_time = time.time()
        print('耗时：{}秒'.format(e_time - s_time))
        return res
    return inner

class Solution(object):
    result = None
    def judgeSquareSum(self, c):
        if c<0:
            return False

        n=sqrt(c)
        if n == int(n):
            # print(c, "=square of two numbers", int(n), 0)
            return True
        else:
            for i in range(1, int(n)+1):
                m = c-pow(i, 2)
                k = sqrt(m)
                if k == int(k):
                    # print(c, "=square of two numbers", i, int(k))
                    result = (c,m,k)
                    return True
            return False

    def judgeSquareSum2(self, c):
        if not c:
            return False

        k = int(sqrt(c))
        l = int(sqrt(c / 2))
        for i in range(k, l - 1, -1):
            m = sqrt(c - i * i)
            if int(m) == m:
                # print(c, i, int(m))
                result = (c,m,i)
                return True
        return False


@get_time
def main():
    for i in range(0, 90000):
        Solution().judgeSquareSum2(i)

main()

