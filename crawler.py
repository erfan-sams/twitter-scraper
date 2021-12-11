
import snscrape.modules.twitter as sntwitter
import pandas as pd
from random import random
from datetime import date
from multiprocessing import Pool
import time

# https://github.com/JustAnotherArchivist/snscrape/blob/master/snscrape/modules/twitter.py

class Twitter_scraper:

  def __init__(self,
               max_results: int,
               all_words = [],
               exact_pharase=[],
               any_words = [],
               none_words = [],
               hashtags = [],
               mentioned_users = [],
               from_users = [],
               to_users = [],
               **kwargs):
    
    self.number_of_user = 0
    self.max_results = max_results
    self.all_words = Twitter_scraper.all_of_these_words(all_words)
    self.exact_pharase = f'"{exact_pharase}"' if exact_pharase else ''
    self.any_words = Twitter_scraper.any_of_these_words(any_words)
    self.none_words = Twitter_scraper.none_of_these_words(none_words)
    self.these_hashtags = Twitter_scraper.any_of_these_hashtags(hashtags)
    self.mentioned_users = Twitter_scraper.mentioning_these_users(mentioned_users)

    self.query_dict = {'all_words':self.all_words, 'exact_pharase':self.exact_pharase,
                  'any_words':self.any_words, 'none_words':self.none_words, 'these_hashtags':self.these_hashtags,
                  'mentioned_users':self.mentioned_users}

    self.query_dict['from'] = Twitter_scraper.f_or_t_users(from_users, 'from')
    self.query_dict['to'] = Twitter_scraper.f_or_t_users(to_users, 'to')

    for key, value in kwargs.items():
        self.query_dict[key] = (f'({key}:{value})')


  @staticmethod
  def f_or_t_users(users, key):
    if not users:
      return ''
    tmp_list = [f'{key}:{user}' for user in users]
    return('(' + ' OR '.join(tmp_list) + ')')

  @staticmethod
  def all_of_these_words(all_words):
    if not all_words:
      return ''
    return ' '.join(all_words)

  @staticmethod
  def any_of_these_words(any_words):
    if not any_words:
      return ''
    return ('(' + ' OR '.join(any_words) + ')')

  @staticmethod
  def none_of_these_words(none_words):
    if not none_words:
      return ''    
    return ('-' + ' -'.join(none_words))

  @staticmethod
  def any_of_these_hashtags(hashtags):
    if not hashtags:
      return ''    
    tmp_list = ['#'+ h.replace('#','') for h in hashtags]
    return ('(' + ' OR '.join(tmp_list) + ')')

  @staticmethod
  def mentioning_these_users(users):
    if not users:
      return ''    
    tmp_list = ['@'+ h.replace('@','') for h in users]
    return ('(' + ' OR '.join(tmp_list) + ')')

  @staticmethod
  def create_query(query_dict):
    tmp_string = ''
    res = dict([(key, val) for key, val in 
           query_dict.items() if val])
    del query_dict
    query = ' '.join(res.values())
    del res

    return query


  def crawler(self, query, error_counter=0):
    # Creating list to append tweet data
    tweets_list = []
    try:
      # Using TwitterUserScraper  TwitterSearchScraper to scrape data and append tweets to list
      scraper = sntwitter.TwitterSearchScraper(query)
      i = 0
      for tweet in scraper.get_items(): #declare a username
          if i >= self.max_results: #check number and date
            break

          tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.replyCount, tweet.retweetCount,
                tweet.likeCount, tweet.user.username, tweet.lang, tweet.media, tweet.hashtags]) #declare the attributes to be returned
          i += 1
      
    except Exception as e:
      if 'Unable to find guest token' in str(e):
          error_counter += 1
          if error_counter > 3:
            error_counter = 0
            print("Sleep Time!")
            time.sleep(30.3 *60)
            print("Morning!")

          return self.crawler(query, error_counter)

      print(f"query: {query} , {e}")

    # Creating a dataframe from the tweets list above 
    tweets_df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Text', 'Reply Count',
                                                    'Retweet Count', 'Like Count', 'username', 'Lang', 'Media', 'Hashtags'])
    return tweets_df



  def user_crawler(self, user):
    tmp_dict = self.query_dict.copy()
    tmp_dict['from'] = (f'(from:{user})')
    query = Twitter_scraper.create_query(tmp_dict)
    del tmp_dict
    return self.crawler(query)


  def user_mode(self, user_list):   
    user_crawler = self.user_crawler 
    pool = Pool(20)
    df_list = pool.map(user_crawler, user_list)
    pool.close()
    pool.join()
    result_df = pd.concat(df_list, ignore_index=True)
    return result_df




from_users = ['CNN', 'FoxNews', 'ABC', 'BBCWorld', 'TIME', 'CBSNews', 'NBCNews', 'MSNBC','nytimes','washingtonpost']
scraper = Twitter_scraper(max_results=10000, until="2020-01-01", since="2019-01-01", lang="en", from_users=from_users)
tmp_query_dict = scraper.query_dict
my_query = Twitter_scraper.create_query(tmp_query_dict)
result = scraper.crawler(my_query)
result.to_csv('test.csv', index=False)
print(result.shape)



