from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
# options.add_argument('headless')  # 크롤링하는 웹 브라우저를 볼 수 없음
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')

driver = webdriver.Chrome('./chromedriver', options=options)

titles = []
reviews = []

# https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page=1
# https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page=2  37까지
# 영화 제목
# //*[@id="old_content"]/ul/li[1]/a
# //*[@id="old_content"]/ul/li[2]/a
# //*[@id="old_content"]/ul/li[20]/a
# //*[@id="movieEndTabMenu"]/li[6]/a/em 리뷰버튼
# //*[@id="pagerTagAnchor1"]  리뷰페이지 버튼
# //*[@id="reviewTab"]/div/div/div[2]/span/em 리뷰 건수
# //*[@id="reviewTab"]/div/div/ul/li[1]/a/strong  리뷰 제목
# //*[@id="reviewTab"]/div/div/ul/li[4]/a/strong
# //*[@id="content"]/div[1]/div[4]/div[1]/div[4]  #class: user_tx_area
# //*[@id="content"]/div[1]/div[4]/div[1]/div[4]
# //*[@id="pagerTagAnchor2"]/em
#//*[@id="pagerTagAnchor10"]/span

review_button_xpath = '//*[@id="movieEndTabMenu"]/li[6]/a'
review_number_xpath = '//*[@id="reviewTab"]/div/div/div[2]/span/em'

for i in range(1, 38):
    url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page={}'.format(i)
    driver.get(url)
    for j in range(1, 21):
        try:
            movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(j)
            title = driver.find_element_by_xpath(movie_title_xpath).text
            print(title)
            titles.append(title)
            driver.find_element_by_xpath(movie_title_xpath).send_keys(Keys.ENTER)
            driver.find_element_by_xpath(review_button_xpath + '/em').click()
            review_range = driver.find_element_by_xpath(review_number_xpath).text
            review_range = int(review_range.replace(',', '')) // 10 + 2
            for k in range(1, review_range):
                review_page_url = driver.find_element_by_xpath(review_button_xpath).get_attribute('href')
                driver.get(review_page_url + '&Page={}'.format(k))
                for l in range(1, 11):
                    review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]/a/strong'.format(l)
                    try:
                        driver.find_element_by_xpath(review_title_xpath).click()
                        review = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[4]/div[1]/div[4]').text
                        print('========================')
                        print(review)
                        driver.back()
                    except:
                        driver.get(url)
                        break
        except:
            print('error')
