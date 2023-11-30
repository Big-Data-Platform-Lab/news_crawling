from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

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
                print(c.text)
                article_res.append(c.text)
        except:
            pass
    except:
        pass

driver.quit()
article_res=set(article_res)
print(len(article_res))
print(article_res)