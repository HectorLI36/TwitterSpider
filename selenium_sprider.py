# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import codecs
import sys
import time
from decorator import retry

reload(sys)
sys.setdefaultencoding('utf-8')


def crawl(url):
    chromedriverPath = ""
    # twitter每次更新13条
    eachCount = 13
    # 滚动几次。滚动次数越多，采集的数据越多
    scrollTimes = 100
    # driver = webdriver.Firefox()
    driver = webdriver.Chrome(chromedriverPath)
    driver.get(url)
    try:
        for i in range(scrollTimes):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            lastTweetCss = "#stream-items-id >li:nth-of-type(" + str(eachCount * (i + 2) + 1) + ") .tweet-text"
            print lastTweetCss
            elem = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, lastTweetCss)))
            printTweet(driver)
    finally:
        driver.close()


@retry(ExceptionToCheck=False, tries=10, delay=50)
def printTweet(driver):
    tweetCss = "[data-item-type=tweet]"
    nameCss = ".fullname"
    timeCss = "._timestamp"
    contentCss = ".tweet-text"
    favourites1 = 'data-tweet-stat-count'
    favourites2 = 'favorite'
    items = driver.find_elements_by_css_selector(tweetCss)
    resultArr = []
    for i, item in enumerate(items):
        try:
            nameElem = item.find_element_by_css_selector(nameCss)
            timeElem = item.find_element_by_css_selector(timeCss)
            contentElem = item.find_element_by_css_selector(contentCss)
            f12 = item.find_elements_by_class_name("ProfileTweet-actionCountForPresentation")[3]

            name = nameElem.text
            time = timeElem.text
            content = contentElem.text
            count = f12.text
            resultArr.append([name, time, content, count])
            print("%d: name=%s time=%s content=%s" % (i, name, time, content))
        except Exception, e:
            print("error index=%d" % (i))
    printToCsv(resultArr)


def printToCsv(data):
    writer = csv.writer(codecs.open('result_with_count2.csv', 'w', 'utf-8'))
    writer.writerow(['name', 'time', 'content', 'likes'])
    for item in data:
        writer.writerow(item)
    pass

if __name__ == '__main__':
    url = "https://twitter.com/ManUtd"
    crawl(url)

