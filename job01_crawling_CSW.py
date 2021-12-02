# 'https://github.com/cswniw/-PRJ_Movie_for_you/tree/main'

# crawling 작업

# crawling은 각자 진행하고 빨리 완성되는 코드로 연도를 나눠서 진행하겠습니다.
# 일단 2020년 개봉작만 크롤링 해주시고 저장 형식은 csv로 하겠습니다.
# 나머지는 연도별로 나눠서 크롤링해서 합칠게요.
# 컬럼명은 ['title','reviews']로 통일해주세요.
# 파일명은 "reviews_{}.csv".format(연도) 해주세요.
# 크롤링한 데이터 파일은 아래 링크로 올려주세요
# https://drive.google.com/drive/folders/1mapy5M7_0RH54bFMuKNP_6NQPGWAVr9W?usp=sharing

from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time

options = webdriver.ChromeOptions()
# options.add_argument('headless')
# headless 옵션을 주면 크롤링하는 웹 브라우저를 볼 수 없다.
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')

driver = webdriver.Chrome('./chromedriver', options=options)


# https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page=1  ~37까지

# url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open={}&page={}'
# 영화 제목 xpath
# //*[@id="old_content"]/ul/li[1]/a
# //*[@id="old_content"]/ul/li[20]/a
# //*[@id="movieEndTabMenu"]/li[6]/a/em  리뷰 x_path
# //*[@id="reviewTab"]/div/div/div[2]/span/em  리뷰 건수
# //*[@id="content"]/div[1]/div[4]/div[1]/div[4]  리뷰 본문   'user_tx_area'
# //*[@id="pagerTagAnchor1"]/span


review_button_xpath = '//*[@id="movieEndTabMenu"]/li[6]/a'
review_number_xpath = '//*[@id="reviewTab"]/div/div/div[2]/span/em'

# https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020

# for year in range(2020,2021) :
try :
    for i in range(1,38) :   # 페이지가 37페이지까지 있다.
        url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page={}'.format(i)
        titles = []
        reviews = []
        for j in range(1, 21):  # 1페이지당 1~20개 영화제목
            print(j+((i-1)*20), '번째 영화 크롤링 중')
            try:
                driver.get(url)
                movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(j)
                title = driver.find_element_by_xpath(movie_title_xpath).text
                driver.find_element_by_xpath(movie_title_xpath).click()
                review_page_url = driver.find_element_by_xpath(review_button_xpath).get_attribute('href')
                driver.get(review_page_url)

                # driver.find_element_by_xpath(review_button_xpath).click()
                # time.sleep(0.1)
                # review_page_url = driver.find_element_by_xpath(review_button_xpath).get_attribute('href')

                review_range = driver.find_element_by_xpath(review_number_xpath).text.replace(',',"")
                review_range = int(review_range)
                review_range = review_range // 10 + 2
                if review_range > 10 :
                    review_range = 10
                for k in range(1, review_range) :
                    driver.get(review_page_url + '&page={}'.format(k))
                    time.sleep(0.3)
                    for l in range(1, 11) :  # 1페이지당 리뷰 10개씩
                        review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]/a/strong'.format(l)
                        try :
                            driver.find_element_by_xpath(review_title_xpath).click()
                            time.sleep(0.3)
                            review = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[4]/div[1]/div[4]').text
                            # print("=============================================================")
                            # print(title)
                            # print(review)
                            titles.append(title)
                            reviews.append(review)
                            driver.back()
                        except :
                            # print(l, "번째 review가 없다.")
                            break
            except :
                print('error', i,)

        df_review_20 = pd.DataFrame({'title': titles, "reviews": reviews})
        df_review_20.to_csv('./crawling_data/reviews_2020_{}_{}.csv'.format(2020,i),
                            index=False)

except :
    print("error totally")
finally :
    driver.close()
# df_review = pd.DataFrame({'title':titles, "reviews":reviews})
# df_review.to_csv('./crawling_data/reviews_{}.csv'.format(2020))
print("최승우")