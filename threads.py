# -*- coding: utf-8 -*-
# Python 2.7 версии

import os
import urllib2
from threading import Thread
import Queue


class Downloader(Thread):
    """
    Пример многопоточной загрузки файлов из интернета
    """

    def __init__(self, queue):
        """Инициализация потока"""
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        # Получаем url из очереди
            url = self.queue.get()

            # Скачиваем файл
            self.download_file(url)

            # Отправляем сигнал о том, что задача завершена
            self.queue.task_done()

    def download_file(self, url):
        """Скачиваем файл"""
        handle = urllib2.urlopen(url)
        fname = os.path.basename(url)

        with open(fname, "wb") as f:
            while True:
                chunk = handle.read(1024)
                if not chunk:
                    break
                f.write(chunk)


def main(urls):
    """
    Запускаем программу
    """
    queue = Queue.Queue()

    # Запускаем потом и очередь
    for p in range(50):
        t = Downloader(queue)
        t.setDaemon(True)
        t.start()

    # Даем очереди нужные нам ссылки для скачивания
    for url in urls:
        queue.put(url)

    # Ждем завершения работы очереди
    queue.join()


if __name__ == "__main__":
    urls = ["http://www.irs.gov/pub/irs-pdf/f1040.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040a.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040ez.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040es.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040sb.pdf"]

    main(urls)