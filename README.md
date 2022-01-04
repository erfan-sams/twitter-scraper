# TwitterScraper

TwitterScraper is a helper class to using snscrape for crawling twitter data.

## snscrape

snscrape is a scraper for social networking services (SNS). It scrapes things like user profiles, hashtags, or searches and returns the discovered items, e.g. the relevant posts.

For more information check out this [Github](https://github.com/JustAnotherArchivist/snscrape)

## Requirements
snscrape requires Python 3.8 or higher. The Python package dependencies are installed automatically when you install snscrape.

## Installation

First you must install snscrape (I recommend that installed this library from Github)

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install snscrape.

Or:
Install requirements by running 
```bash
pip install -r requirements.txt
```


## Usage
Create an instance from the class and after that, there are two prepared functions for your usage.

```python
import TwitterScraper

# Tweets from these accounts
from_users = ['CNN', 'FoxNews', 'ABC', 'BBCWorld', 'TIME', 'CBSNews', 'NBCNews', 'MSNBC','nytimes','washingtonpost']

# Add your parameters you can find acceptable of them in __init__ function
# for kwargs you can set until="yyyy-mm-dd", since="yyyy-mm-dd"
# lang="language code" 
# you can find language code on this link https://meta.wikimedia.org/wiki/Template:List_of_language_names_ordered_by_code

scraper = TwitterScraper(max_results=10**2, until="2020-01-01", since="2019-01-01", lang="en", from_users=from_users, with_replies=False)

```

###Basic_mode
That is just send a simple query to the crawler and return pandas dataframe of reults.

```python
# Test
result = scraper.basic_mode()
# Write the dataframe as a csv file
result.to_csv('test.csv', index=False)

```

###User_mode
We use this mode to use the multithreading feature and crawl data faster
this mode send a request per twitter account. number of threads set as 22 but feel free to change it!

```python
result = scraper.user_mode(user_list)
result.to_csv('test.csv', index=False)
```
I defined the below function for my work you can use it if you like :)

```python
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

```
### Coalb link
There are some tricky things you must do before using this library on colab
hence default python of colab is 3.7 and we need version 3.8 or higher and for that reason, we must run these code on colab. but that's not enogh!!!


After installation of python 3.8+ and libraries on colab you need to write your code as a python file and run it with this command. cause in the colab cells we still have the python 3.7 !!!

you can find sample code on this link [colab](https://colab.research.google.com/drive/18jcZ9GGw033ZwxSO8rB5iGawKQWwAGU2?usp=sharing)

```python
# run it after below code
! python my-file.py
```

```python
!sudo apt-get update 
!sudo apt-get install python3.8

#change alternatives
!sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1
!sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2

#check python version
!python --version

! curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py 
! python3 get-pip.py --force-reinstall 

!pip install git+https://github.com/JustAnotherArchivist/snscrape.git

# require libraries
! pip install pandas 
! pip install datetime

```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
