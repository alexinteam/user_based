# -*- coding: utf-8 -*-
# Python 2.7 версии

from threading import Thread
from scipy.spatial.distance import cosine


class Similarities(Thread):
    def __init__(self, queue, data_ibs, data_germany):
        Thread.__init__(self)
        self.queue = queue
        self.data_ibs = data_ibs
        self.data_germany = data_germany
        self.raw = []

    def run(self):
        # Получаем url из очереди
            i = self.queue.get()

            # Скачиваем файл
            for j in range(0, len(self.data_ibs.columns)):
                # Fill in placeholder with cosine similarities
                self.data_ibs.ix[i, j] = 1 - cosine(self.data_germany.ix[:, i], self.data_germany.ix[:, j])

            # Отправляем сигнал о том, что задача завершена
            self.queue.task_done()
