import pandas
import pymongo

mongo_ip = '192.168.1.127'
mongo_con = pymongo.MongoClient(mongo_ip)
mongo_col = mongo_con.analysis.common_items

freq_names = ['singles','doubles','triples','quads']
for fn in freq_names:
  print 'getting ' + fn
  freq_series = pandas.Series()
  cursor = mongo_col.find({'name':fn})
  #aggregate data
  if (cursor.count()>0):
    for doc in cursor:
      if 'data' in doc.keys():
        freq_data = pandas.Series(doc['data'])
        freq_series = pandas.concat([freq_series, freq_data])
    freq_series_grouped_summed = freq_series.groupby(level=0).sum()
    freq_series_grouped_summed.sort(ascending=False)
    freq_series_grouped_summed.index = [', '.join(eval(x)) for x in freq_series_grouped_summed.index]    
    freq_series_grouped_summed.head(100).to_csv('test/output/'+fn+'.csv')
