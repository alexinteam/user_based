# -*- coding: utf-8 -*-
# Python 2.7 версии

from Models.similarities import similarities
from scipy.spatial.distance import cosine
import Queue


def main(data_ibs, data_germany):
    """
    Запускаем программу
    """
    for i in range(0, len(data_ibs.columns)):
        # Loop through the columns for each column
        for j in range(0, len(data_ibs.columns)):
            # Fill in placeholder with cosine similarities
            data_ibs.ix[i, j] = 1 - cosine(data_germany.ix[:, i], data_germany.ix[:, j])



    queue = Queue.Queue()

    # Запускаем потом и очередь
    for i in range(10):
        t = similarities(queue);
        t.setDaemon(True)
        t.start()

    a = []
    # Даем очереди нужные нам ссылки для скачивания
    for i in range(0, len(data_ibs.columns)):
        queue.put(i)

    # Ждем завершения работы очереди
    queue.join()

    return a