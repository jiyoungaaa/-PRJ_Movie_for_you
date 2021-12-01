from selenium import  webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time

options = webdriver.ChromeOptions()
# options.add_argument('headless')   ## 이옵션이면 브라우저가 안뜸
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')

driver = webdriver.Chrome('./chromedriver', options= options)

titles = []
reviews = []

# https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020
# https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page=4

for i in range(1, 38):
    url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page={}'.format(i)
    for j in range(1, 21):
        try:
            driver.get(url)
            movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(j)
            title = driver.find_element_by_xpath(movie_title_xpath).text
            print(title)
        except:
            print('error')