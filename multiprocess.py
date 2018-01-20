#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import sys
import getopt
import threading
import os
import multiprocessing


def ncount(n):  # тестовая CPU-загружающая функция
    while n > 0: n -= 1


if __name__ == '__main__':
    repnum = 10000000
    thrnum = 1
    mode = 'stpm'  # варианты запуска

    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:n:m:")
    except getopt.GetoptError:
        print ("недопустимая опция команды или её значение")

    for opt, arg in opts:
    #     if opt[1:] == 't': thrnum = int(arg)
    #     if opt[1:] == 'n': repnum = int(arg)
        if opt[1:] == 'm': mode = arg

    print("число процессоров (ядер) = {0:d}".format(multiprocessing.cpu_count()))
    print("исполнение в Python версия {0:s}".format(sys.version))
    print("число ветвей выполнения {0:d}".format(thrnum))
    print("число циклов в ветви {0:d}".format(repnum))
    #
    # if 's' in mode:
    #     print("============ последовательное выполнение ============")
    #     clc = time.time()
    #     for i in range(thrnum): ncount(repnum)
    #     clc = time.time() - clc
    #     print("время {0:.2f} секунд".format(clc))
    #
    # if 't' in mode:
    #     print("================ параллельные потоки ================")
    #     threads = []
    #     for n in range(thrnum):
    #         tid = threading.Thread(target=ncount, args=(repnum,))
    #         threads.append(tid)
    #         tid.setDaemon(1)
    #     clc = time.time()
    #     for n in range(thrnum): threads[n].start()
    #     for n in range(thrnum): threads[n].join()
    #     clc = time.time() - clc
    #     print("время {0:.2f} секунд".format(clc))
    #
    # if 'p' in mode:
    #     print("=============== параллельные процессы ===============")
    #     threads = [];
    #     fork = True
    #     clc = time.time()
    #     for n in range(thrnum):
    #         try:
    #             pid = os.fork();
    #         except:
    #             print("ошибка создания дочернего процесса")
    #             fork = False
    #             break
    #         else:
    #             if pid == 0:  # дочерний процесс
    #                 ncount(repnum)
    #                 sys.exit(0)
    #             if pid > 0:  # родительский процесс
    #                 threads.append(pid)
    #     if fork:
    #         for p in threads:
    #             pid, status = os.wait()
    #         clc = time.time() - clc
    #         print("время {0:.2f} секунд".format(clc))

    if 'm' in mode:
        print("=============== модуль multiprocessing ==============")
        parms = []
        for n in range(thrnum):
            parms.append(repnum)
        multiprocessing.freeze_support()
        pool = multiprocessing.Pool(processes=thrnum, )
        clc = time.time()
        pool.map(ncount, parms)
        clc = time.time() - clc
        print("время {0:.2f} секунд".format(clc))