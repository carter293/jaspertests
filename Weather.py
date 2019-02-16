
# -*- coding: utf-8-*-
import requests
import re
from lxml import html
import random


def getCurrentWeather(url, mic):
    headers = {'User-agent': 'wswp'}
    ctemppath = """//*[@id="feed-tabs"]/ul/li[1]/div[1]/div[2]/div/span[1]"""
    skypath = """//*[@id="feed-tabs"]/ul/li[1]/div[1]/div[2]/span"""
    coldDesc = ['tad chilly', 'little cold', 'cold one', "kind of cold"]
    hotDesc = ["scorcher", 'bit warm', 'real hot one', "bloody hot one",
               "hot enough to be sweating like a priest in a school"]
    curDesc = ['Currently', "Today", "Right now", "Outside"]
    skyDesc = ["with the sky to be ",
               "with the sky described as ",
               "with the weather man saying the sky is "]
    skyIntro = random.choice(skyDesc)
    cur = random.choice(curDesc)

    resp = requests.get(url, headers=headers)
    byte_data = resp.content
    source_code = html.fromstring(byte_data)
    tree1 = source_code.xpath(ctemppath)
    cTemp = tree1[0].text_content()[:2]

    tree2 = source_code.xpath(skypath)
    sky = tree2[0].text_content()

    if int(cTemp) > 30 or int(cTemp) == 30:
        temp = random.choice(hotDesc)
        mic.say(cur + " it's a " + temp + " at " + cTemp + " degrees " + skyIntro + sky)

    if int(cTemp) < 15 or int(cTemp) == 15:
        temp = random.choice(coldDesc)
        mic.say(cur + " it's a " + temp + " at " + cTemp + " degrees " + skyIntro + sky)

    if 15 < int(cTemp) < 30:
       mic.say(cur + "it's" + cTemp + " degrees " + skyIntro + sky)


def handle(text, mic, profile):
    url = 'https://www.accuweather.com/en/au/perth/26797/weather-forecast/26797'
    getCurrentWeather(url, mic)

def isValid(text):
    return bool(re.search(r"\bweather\b", text, re.IGNORECASE)) or bool(re.search(r"\boutside\b", text, re.IGNORECASE))
