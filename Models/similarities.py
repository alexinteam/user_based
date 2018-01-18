# -*- coding: utf-8 -*-
# Python 2.7 версии

from threading import Thread
import os
import urllib2


class similarities(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        self.raw = []

    def run(self):
        # Получаем url из очереди
            i = self.queue.get()

            # Скачиваем файл
            self.download_file(i)

            # Отправляем сигнал о том, что задача завершена
            self.queue.task_done()

    def download_file(self, i):
        for j in range(0, len(data_ibs.columns)):
            # Fill in placeholder with cosine similarities
            data_ibs.ix[i, j] = 1 - cosine(data_germany.ix[:, i], data_germany.ix[:, j])