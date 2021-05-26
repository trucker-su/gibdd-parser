import requests
from selenium import webdriver
import bs4
import time
import json

# https://chromedriver.chromium.org/downloads
# Здесь нужно скачать драйвер для установленной на компьютере версии браузера Chrome
# Я использую драйвер для Mac, версия 90.0.4430.24
# Драйвер указывается в переменной path
# time.sleep(3) дает время selenium сгенерировать javascript, так как вся информация о новостях


def main():
    path = '/Users/ilya/Documents/IT/Selenium/chromedriver'

    final_data = dict()

    articles_links = []

    browser = webdriver.Chrome(path)
    browser.get('https://xn--90adear.xn--p1ai/r/65/')

    links = browser.find_elements_by_xpath("//a[contains(@href,'/news/window/')]")

    for elem in links:
        articles_links.append(elem.get_attribute('href'))

    articles_links = list(dict.fromkeys(articles_links))
    count = 0

    for link in articles_links:
        browser.get(link)
        time.sleep(3)
        response = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

        soup = bs4.BeautifulSoup(response, 'html.parser')
        news_item = soup.find('div', {'class': 'news-item'})

        title = str(news_item.find('h2')).replace('<h2>', '').replace('</h2>', '')

        paragraphs = news_item.find_all('p')

        article = [str(p.text).replace('\xa0', '') for p in paragraphs]
        article_text = ''
        for p in article:
            article_text = article_text + p

        final_data[count] = {'title': title, 'article': article_text}

        count += 1

    with open('result.json', 'w') as fp:
        json.dump(final_data, fp, ensure_ascii=False)

    browser.quit()


if __name__ == '__main__':
    main()
