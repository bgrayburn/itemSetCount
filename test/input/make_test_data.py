import pandas
import numpy as np
from numpy.random import rand

numOfRecords = 1000
maxNumOfItems = 5
weighting = 'exponential' #exponential, flat, or gaussian

items = []
for i in range(15):
   items += ['Item'+str(i)]
print("created item list: " + str(items))
cur_record = 0
with open("test_data.csv", "wb") as file:
  while (cur_record<numOfRecords):
    record_length = int(np.floor(rand()*(maxNumOfItems)))+1
    rec_items = []
    for i in range(record_length):
      found_a_good_one = False
      while not found_a_good_one:
        test_item = items[int(np.floor(rand()*(items.__len__())))]
        #print("test_item= "+test_item)
        if test_item not in rec_items:
            found_a_good_one = True
            #print('found a good one!')
            rec_items += [test_item]
            #print('number of records = ' + str(rec_items.__len__()))
    file.write(("|").join(rec_items)+"\n")
    if (cur_record%1 == 0):
      print("current record: " + str(cur_record))
    cur_record+=1

