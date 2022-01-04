# import Twitter_scraper
import Twitter_scraper

# Tweets from these accounts
from_users = ['CNN', 'FoxNews', 'ABC', 'BBCWorld', 'TIME', 'CBSNews', 'NBCNews', 'MSNBC','nytimes','washingtonpost']

# Add your parameters you can find acceptable of them in __init__ function
# for kwargs you can set until="yyyy-mm-dd", since="yyyy-mm-dd"
# lang="language code"
# you can find language code on this link https://meta.wikimedia.org/wiki/Template:List_of_language_names_ordered_by_code

scraper = Twitter_scraper(max_results=10**2, until="2020-01-01", since="2019-01-01", lang="en", from_users=from_users, with_replies=False)

# Test
result = scraper.basic_mode()
# Write the dataframe as a csv file
result.to_csv('test.csv', index=False)

def write_file(path, file_format, user_list):
  number_of_users = len(user_list) - 1
  tmp_list = []
  for n in range(1, ((number_of_users//50)+2)):
    try:
      tmp_df = scraper.user_mode(user_list[50*(n-1):50*n])
      tmp_list.append(tmp_df)
    except:
      pass
  result_df = pd.concat(tmp_list, ignore_index=True)

  compression_opts = dict(method='zip',
      archive_name='tweets.csv')
  print('number of tweets', result_df.shape[0])
  exec(f"result_df.to_{file_format}('{path}', index=False, compression=compression_opts)")

  path = 'test.csv'
  # feel free to set your format!
  # for intance that's can be a csv, json, pickle, ...
  # pay attention to df.to_format
  file_format = 'csv'
  write_file(path, file_format, user_list)
