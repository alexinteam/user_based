# -*- coding: utf-8 -*-
# Python 2.7 версии

import os
import urllib2
from threading import Thread
import Queue
from Models.similarities import similarities

def main(urls):
    """
    Запускаем программу
    """
    queue = Queue.Queue()

    # Запускаем потом и очередь
    for i in range(5):
        t = similarities(queue)
        t.setDaemon(True)
        t.start()

    a = []
    # Даем очереди нужные нам ссылки для скачивания
    for url in urls:
        queue.put(url)
        index = urls.index(url)
        a.append(index)

    # Ждем завершения работы очереди
    queue.join()

    return a


if __name__ == "__main__":
    urls = ["http://www.irs.gov/pub/irs-pdf/f1040.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040a.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040ez.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040es.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040sb.pdf"]

    print main(urls)