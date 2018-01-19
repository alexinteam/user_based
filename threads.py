import os
from multiprocessing import Pool

def multi_run_wrapper(args):
    a = add(*args)
    return a

def add(x,y):
    return x+y
if __name__ == "__main__":
    from multiprocessing import Pool
    pool = Pool(4)
    results = pool.map(multi_run_wrapper,[(1,2),(1,3),(1,4),(1,5),(1,6),(1,7)])
    print results