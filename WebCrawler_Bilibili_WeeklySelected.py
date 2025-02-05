import requests
import lxml
import bs4

from selenium import webdriver as web
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
num = 300
for j in range(0, 51):
    """ 每周必看页面"""
    browser = web.Edge()
    browser.get(f"https://www.bilibili.com/v/popular/weekly?num={num-j}")
    lis = browser.find_elements(By.TAG_NAME, "a")
    urls = []
    for i in  lis:
        if("video" in i.get_attribute("href")):
            urls.append(i.get_attribute("href"))
    urls.pop()
    while len(urls) == 0:
        browser.get(f"https://www.bilibili.com/v/popular/weekly?num={num - j}")
        sleep(0.5)
        lis = browser.find_elements(By.TAG_NAME, "a")
        urls = []
        for i in lis:
            if ("video" in i.get_attribute("href")):
                urls.append(i.get_attribute("href"))
        urls.pop()
    browser.close()

    with open("url.txt", "w") as c:
        for i in urls:
            c.write(i+"\n")



    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Referer': 'https://www.bilibili,com/',
    'Connection': 'keep-alive'
    }

    for url in urls:
        response = requests.get(url, headers=headers)
        sleep(0.5)
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, features="lxml")
        for i in soup.find_all("div"):
            try:
                if "view" in i["class"]:
                    view_data = i.find("div", {'class': "view-text"}).getText()
            except Exception:
                pass
        try:
            for i in soup.find("div", {"class": "video-tag-container"}).find_all("div"):
                channel = i.find("div", {"class":"firstchannel-tag"}).find("a").getText()
        except Exception:
            pass

            for i in soup.find_all("span"):
                try:
                    if("video-like-info" in i['class']):
                        likes = (i.getText())
                except Exception:
                    pass
                try:
                    if("video-coin-info" in i["class"]):
                            coins = i.getText()
                except Exception:
                    pass
                try:
                    if("video-fav-info" in i["class"]):
                        favourites = i.getText()
                except Exception:
                    pass
                try:
                    if("video-share-info" in i["class"]):
                        share = i.getText()
                except Exception:
                    pass
        try:
            up = soup.find("a", {"class": "up-name vip"}).getText()
        except Exception:
            try:
                up = soup.find("a", {"class": "up-name"}).getText()
            except Exception:
                pass
        try:
            print(soup.h1.getText())
            print("video maker", up)
            print("view data", view_data)
            print("channel", channel)
            print("likes", likes)
            print("coins", coins)
            print("collection", favourites)
            print("shares", share)
            print("_________________________________________________________________________________\n")
        except Exception:
            print("\n"*10, "output error", "\n"*10)

        """存入txt"""
        try:
            with open("data.txt","a", encoding="gbk") as q:
                q.write(soup.h1.getText()+"\n")
                q.write("video maker "+up+"\n")
                q.write("view data "+ view_data+"\n")
                q.write("channel "+ channel+"\n")
                q.write("likes "+ likes+"\n")
                q.write("coins "+ coins+"\n")
                q.write("collects "+ favourites+"\n")
                q.write("shares "+ share+"\n")
                q.write("_________________________________________________________________________________\n")
                q.close()
        except Exception:
            print("\n"*10, "output error", "\n"*10)