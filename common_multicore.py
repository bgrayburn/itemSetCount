from multiprocessing import Process
import pymongo
from itertools import combinations
import csv
import time
import sys

mongo_ip = "192.168.1.127"
db_name = "analysis"
collection_name = "common_items"
max_item_threshold = 20

def load_transaction(filename):
  transaction = []
  with open(filename,'rb') as csvfile:
    cread = csv.reader(csvfile, delimiter='|', quotechar="'")
    for row in cread:
      transaction.append(list(row))
  return transaction

def common_job(job_transaction, batch_num):
  mongo_con = pymongo.MongoClient(mongo_ip)
  mongo_col = eval("mongo_con."+db_name+"."+collection_name)

  name_of_sets = ['singles','doubles','triples','quads']
  for ind, v in enumerate(job_transaction):
    print 'batch: ' + str(batch_num) + ' transaction #' + str(ind) + ' with ' + str(v.__len__()) + ' of items'
    for i in range(1,5): #singles, doubles, etc.
      cur_set = name_of_sets[i-1]
      for combo in combinations(v, i):
        combo_set = tuple(set(combo))
        if combo_set[0]=='':
          break
        mongo_col.update({'name':cur_set, 'batch':batch_num}, {'$inc':{'data.'+str(combo_set) : 1}} ,upsert=True)

def make_batches(transaction, batch_size):
  last_pos = 0
  batches = []
  while (last_pos<transaction.__len__()):
    start = last_pos + 1
    end = min(last_pos+batch_size+1, transaction.__len__())
    last_pos = end
    batches.append(transaction[start:end])
  return batches

def still_running(processes):
  out = False
  for p in processes:
    if p.is_alive():
      out = True
  return out

def main(filename):
  transaction = load_transaction(filename)
  transaction = [v for v in transaction if v.__len__()<max_item_threshold]
  batch_size = 50
  batches = make_batches(transaction, batch_size)
  processes = []
  for ind, b in enumerate(batches):
    job = Process(target=common_job, args=([b, ind]))
    processes.append(job)
    job.start()
  return processes

if __name__ == '__main__':
  mongo_con = pymongo.MongoClient(mongo_ip)
  mongo_col = eval("mongo_con."+db_name+"."+collection_name)
  mongo_col.remove()
  processess = main(sys.argv[1])
  while(still_running(processess)):
    time.sleep(2)
