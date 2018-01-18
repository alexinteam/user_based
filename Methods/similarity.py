# -*- coding: utf-8 -*-
# Python 2.7 версии

from Models.similarities import Similarities
from scipy.spatial.distance import cosine
import Queue


def main(data_ibs, data_germany, i):
    """
    Запускаем программу
    """

    queue = Queue.Queue()

    # Запускаем потом и очередь
    for k in range(10):
        t = Similarities(queue, data_ibs, data_germany)
        t.setDaemon(True)
        t.start()

    a = []
    # Даем очереди нужные нам ссылки для скачивания
    queue.put(i)

    # Ждем завершения работы очереди
    queue.join()

    return a