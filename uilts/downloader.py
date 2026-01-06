import re
from time import sleep
from typing import List, TypedDict

import requests
from bs4 import BeautifulSoup


def getSoup(url: str):
    sleep(1)
    html = requests.get(url, "lxml")
    html.encoding = "utf-8"
    return BeautifulSoup(html.text, features="lxml")

class Item(TypedDict):
    title: str

class Category(TypedDict):
    name: str
    list: List[Item]

class Downloader:
    dict_item: set[str]
    
    def __init__(self, fp):
        self.dict_item = set()
        self.outFile = open(fp, "w", encoding="utf-8")

    def getAll(self):
        # 来自观测枢
        channelMap :dict[str, int] = {
            '游戏图鉴': 17,
            '货币战争图鉴': 209,
        }

        # 爬取数据
        for channel in channelMap:
            res = requests.get(f"https://act-api-takumi-static.mihoyo.com/common/blackboard/sr_wiki/v1/home/content/list?app_sn=sr_wiki&channel_id={channelMap.get(channel)}")
            data = res.json()['data']
            if data is None:
                print(f"{channel}获取失败，跳过该分类")
                continue
            categoryList: list[Category] = data['list'][0]['children']
            
            count = 0
            for category in categoryList:
                dataList = category.get('list')
                for item in dataList:
                    reg = r"【.*?】"
                    title: str = re.sub(reg, "", item.get("title"))
                    
                    # 统一符号
                    title = title.replace('·', '•')
                    title = title.replace('・', '•')
                    
                    self.dict_item.add(title)
                    count+=1
                    
                    # 拆分词条
                    splitChar :List[str] = [' ', '•', '，']
                    for char in splitChar:
                        if title.find(char) > -1:
                            for word in title.split(char):
                                self.dict_item.add(word)
                                count += 1
            print(f"获取{channel}完毕，共写入{count}个词条")

        # 写入文件
        self.outFile.write('\n'.join(self.dict_item))
        print(f"爬取信息完毕，去重后共{len(self.dict_item)}个词条")
        self.outFile.close()
