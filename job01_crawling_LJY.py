from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.keys import Keys


options = webdriver.ChromeOptions()
options.add_argument('headless') #웹브라우저가 안 뜸, 메모리상에만 뜬 채로 크롤링을 함.
options.add_argument('window-size=1920x10180')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')
driver = webdriver.Chrome('./chromedriver', options=options)


# https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page=1
# https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page=2   37까지
# 영화 제목 xpath
# //*[@id="old_content"]/ul/li[1]/a
# //*[@id="old_content"]/ul/li[2]/a
# //*[@id="old_content"]/ul/li[20]/a
# //*[@id="movieEndTabMenu"]/li[6]/a/em  리뷰버튼,
# //*[@id="reviewTab"]/div/div/div[2]/span/em 리뷰 건수

# //*[@id="pagerTagAnchor1"]   리뷰 페이지 버튼
# //*[@id="pagerTagAnchor10"]/em   리뷰 다음 페이지 버튼
# //*[@id="reviewTab"]/div/div/ul/li[1]/a/strong 리뷰 제목
# //*[@id="SE-ec9bce5c-9be3-47a9-9957-b075426d88fb"] 리뷰 한 줄
# //*[@id="content"]/div[1]/div[4]/div[1]/div[4]        # class:user_tx_area

review_button_xpath = '//*[@id="movieEndTabMenu"]/li[6]/a'
review_number_xpath = '//*[@id="reviewTab"]/div/div/div[2]/span/em'

try:
    for i in range(1, 44):
        url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2019&page={}'.format(i)
        titles = []
        reviews = []
        for j in range(1, 21):
            print(j+((i-1)*20), '번째 영화 크롤링 중')
            try:
                driver.get(url)
                time.sleep(0.4)
                movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(j)
                title = driver.find_element_by_xpath(movie_title_xpath).text
                driver.find_element_by_xpath(movie_title_xpath).send_keys(Keys.ENTER)
                time.sleep(0.4)
                review_page_url = driver.find_element_by_xpath(review_button_xpath).get_attribute('href')
                driver.get(review_page_url)
                time.sleep(0.4)
                review_range = driver.find_element_by_xpath(review_number_xpath).text
                review_range = review_range.replace(',', '')
                review_range = int(review_range)
                review_range = review_range // 10 + 2
                if review_range > 6:
                    review_range = 6
                for k in range(1, review_range):
                    driver.get(review_page_url + '&page={}'.format(k))
                    time.sleep(0.4)
                    for l in range(1, 11):
                        review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]/a/strong'.format(l)
                        try:
                            driver.find_element_by_xpath(review_title_xpath).click()
                            time.sleep(0.4)
                            review = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[4]/div[1]/div[4]').text
                            # print('===================== =====================')
                            # print(title)

                            # print(review)
                            titles.append(title)
                            reviews.append(review)
                            driver.back()
                        except:
                            print(l, '번째 review가 없다.')
                            #driver.get(url)
                            break

            except:
                print('error')
            df_review_20 = pd.DataFrame({'title':titles, 'reviews':reviews})
            df_review_20.to_csv('./crawling_data/reviews_{}_{}.csv'.format(2019,i), index=False)
except:
    print('totally error')
finally:
    driver.close()


# df_review = pd.DataFrame({'title':titles, 'reviews':reviews})
# df_review.to_csv('./crawling_data_/reviews_{}.csv'.format(2020))

