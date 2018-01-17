
# --- Import Libraries --- #

import pandas as pd
from scipy.spatial.distance import cosine
import time
import os
import urllib2
from threading import Thread
import Queue

print time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

# --- Read Data --- #
data = pd.read_csv('data1.csv')

# --- Start Item Based Recommendations --- #
# Drop any column named "user"
data_germany = data.drop('user', 1)

# Create a placeholder dataframe listing item vs. item
data_ibs = pd.DataFrame(index=data_germany.columns,columns=data_germany.columns)


def main(urls):
    """
    Запускаем программу
    """
    queue = Queue.Queue()

    # Запускаем потом и очередь
    for i in range(50):
        t = Downloader(queue)
        t.setDaemon(True)
        t.start()

    # Даем очереди нужные нам ссылки для скачивания
    for url in urls:
        queue.put(url)

    # Ждем завершения работы очереди
    queue.join()

# Lets fill in those empty spaces with cosine similarities
# Loop through the columns
for i in range(0,len(data_ibs.columns)) :
    # Loop through the columns for each column
    urls = ["http://www.irs.gov/pub/irs-pdf/f1040.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040a.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040ez.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040es.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040sb.pdf"]

    main(urls)
    for j in range(0,len(data_ibs.columns)) :
      # Fill in placeholder with cosine similarities
      data_ibs.ix[i, j] = 1-cosine(data_germany.ix[:, i], data_germany.ix[:, j])

print data_ibs
# # Create a placeholder items for closes neighbours to an item
# data_neighbours = pd.DataFrame(index=data_ibs.columns,columns=[range(1,11)])
#
# # Loop through our similarity dataframe and fill in neighbouring item names
# for i in range(0, len(data_ibs.columns)):
#     data_neighbours.ix[i, :10] = data_ibs.ix[0:, i].sort_values(ascending=False)[:10].index
#
# # --- End Item Based Recommendations --- #
#
# # --- Start User Based Recommendations --- #
#
# # Helper function to get similarity scores
# def getScore(history, similarities):
#    return sum(history*similarities)/sum(similarities)
#
# # Create a place holder matrix for similarities, and fill in the user name column
# data_sims = pd.DataFrame(index=data.index,columns=data.columns)
# data_sims.ix[:,:1] = data.ix[:,:1]
#
# #Loop through all rows, skip the user column, and fill with similarity scores
# for i in range(0,len(data_sims.index)):
#     for j in range(1,len(data_sims.columns)):
#         user = data_sims.index[i]
#         product = data_sims.columns[j]
#
#         if data.ix[i][j] == 1:
#             data_sims.ix[i][j] = 0
#         else:
#             product_top_names = data_neighbours.ix[product][1:10]
#             product_top_sims = data_ibs.ix[product].sort_values(ascending=False)[1:10]
#             user_purchases = data_germany.ix[user,product_top_names]
#
#             data_sims.ix[i][j] = getScore(user_purchases,product_top_sims)
#
# # Get the top songs
# data_recommend = pd.DataFrame(index=data_sims.index, columns=['user','1','2','3','4','5','6'])
# data_recommend.ix[0:,0] = data_sims.ix[:,0]
#
# # Instead of top song scores, we want to see names
# for i in range(0,len(data_sims.index)):
#     data_recommend.ix[i,1:] = data_sims.ix[i,:].sort_values(ascending=False).ix[1:7,].index.transpose()
#
# # Print a sample
# print data_recommend.ix[:, :6]
print time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())


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
