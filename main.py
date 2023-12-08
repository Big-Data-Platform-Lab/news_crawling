from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import csv

class Data:
    def __init__(self, comment, likes, date):
        self.tag = 'news'
        self.comment = comment
        self.likes=likes
        self.date=date


driver = webdriver.Chrome()

# define the Base URL
# search tag '일회용품 사용금지'
base_url = "https://www.chosun.com/nsearch/?query=%EC%9D%BC%ED%9A%8C%EC%9A%A9%ED%92%88%20%EC%82%AC%EC%9A%A9%EA%B8%88%EC%A7%80&page={}&siteid=&sort=1&date_period=all&date_start=&date_end=&writer=&field=&emd_word=&expt_word=&opt_chk=false&app_check=0&website=www,chosun&category="

article_links = []
for page_number in range(1,10):
    url=base_url.format(page_number)
    print(base_url)
    driver.get(url)
    time.sleep(2)

    find_articles=driver.find_elements(By.CLASS_NAME, "text__link.story-card__headline")

    # 각 기사의 href 속성 수집
    for article in find_articles:
        link = article.get_attribute("href")
        article_links.append(link)
print(article_links)

article_res=[]
csv_data=[]
for link in article_links:
    driver.get(link)
    try:
        more_button = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CLASS_NAME, "data-more-btn"))
        )
        more_button.click()
        try:
            article_comments = WebDriverWait(driver, 1).until(
             EC.presence_of_all_elements_located((By.CLASS_NAME, "comment-card__commentcontent"))
            )


            for c in article_comments:
                # 좋아요 수 요소 찾기
                likes_element = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.ID, "up-count"))
                )

                # 좋아요 수 가져오기
                likes_count = likes_element.text
                print("좋아요 수:", likes_count)

                # 댓글 날짜 요소 찾기
                comment_date_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "comment-card__commentdate"))
                )
                comment_date_text = comment_date_element.text
                comment_date = comment_date_text.split()[0]
                print("댓글 날짜:", comment_date)

                print(c.text)
                article_res.append(c.text)

                csv_data.append(Data(c.text, likes_count, comment_date))
        except:
            pass
    except:
        pass

driver.quit()
article_res=set(article_res)
print(len(article_res))
print(article_res)
print(csv_data)

# CSV 파일에 저장
csv_file_path = "big_data_crawling2.csv"

# CSV 파일 쓰기
with open(csv_file_path, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)

    # 헤더 작성
    writer.writerow(["tag", "Comment", "Likes", "Date"])

    # 데이터 작성
    for data in csv_data:
        writer.writerow([data.tag, data.comment, data.likes, data.date])

print(f"데이터가 {csv_file_path}에 성공적으로 저장되었습니다.")