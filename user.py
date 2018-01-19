# -*- coding: utf-8 -*-
# Python 2.7 версии

import pandas as pd
from scipy.spatial.distance import cosine
import threading
from timeit import default_timer as timer

start = timer()

# --- Read Data --- #
data = pd.read_csv('data.csv')

# --- Start Item Based Recommendations --- #
# Drop any column named "user"
data_germany = data.drop('user', 1)

# Create a placeholder dataframe listing item vs. item
data_ibs = pd.DataFrame(index=data_germany.columns,columns=data_germany.columns)

# Lets fill in those empty spaces with cosine similarities
# Loop through the columns
# for i in range(0,len(data_ibs.columns)):
#     # Loop through the columns for each column
#     for j in range(0,len(data_ibs.columns)):
#         # Fill in placeholder with cosine similarities
#         data_ibs.ix[i, j] = 1-cosine(data_germany.ix[:, i], data_germany.ix[:, j])


def similaritiesHandler(args, event_for_wait, event_for_set):
    event_for_wait.wait() # wait for event
    event_for_wait.clear() # clean event for future
    cos(*args)
    event_for_set.set() # set event for neighbor thread


def cos(array,start,stop):
    for ii in range(start, stop):
        data_ibs.ix[array[ii][0], array[ii][1]] = 1 - cosine(data_germany.ix[:, array[ii][0]], data_germany.ix[:, array[ii][1]])
    return


b=[]
for i in range(0, len(data_ibs.columns)):
    for j in range(0, len(data_ibs.columns)):
        b.append((i,j))


# init events
e1 = threading.Event()
e2 = threading.Event()
e3 = threading.Event()
e4 = threading.Event()

# init threads
t1 = threading.Thread(target=similaritiesHandler, args=((b,0,10000), e1, e2))
t2 = threading.Thread(target=similaritiesHandler, args=((b,10000,20000), e2, e3))
t3 = threading.Thread(target=similaritiesHandler, args=((b,20000,30000), e3, e4))
t4 = threading.Thread(target=similaritiesHandler, args=((b,30000,40000), e4, e1))

# start threads
t1.start()
t2.start()
t3.start()
t4.start()

e1.set() # initiate the first event

# join threads to the main thread
t1.join()
t2.join()
t3.join()
t4.start()
# print data_ibs
end = timer()

print("Time taken:", end-start)

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
# print time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())


