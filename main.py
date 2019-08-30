import requests
import re
import os
import random
from selenium import webdriver
from bs4 import BeautifulSoup

wenkuSearchURL = 'https://wenku.baidu.com/search'

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3879.0 Safari/537.36 Edg/78.0.249.1',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Sec-Fetch-Site': 'none',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

options = webdriver.ChromeOptions()
options.add_argument(
    'user-agent="Mozilla/5.0 (Linux; Flyme 8.0.0; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"')
# driver = webdriver.Chrome(options=options, executable_path="." + os.sep + "lib" + os.sep + "chromedriver.exe")
driver = webdriver.Chrome(options=options)


class osAPI:
    def createDIR(dirName):
        try:
            path = "." + os.sep + dirName
            os.makedirs(path)
        except Exception as e:
            pass

    def saveFile(fileName, content, dirName):
        if content == "":
            print("文件为空，自动跳过该文件")
            return
        try:
            # 防止文件名冲突硬核解决方案
            randomNum = str(random.randrange(10000000, 100000000))
            fileName = "." + os.sep + dirName + os.sep + fileName + "_" + randomNum + ".txt"
            with open(fileName, 'w', encoding='utf-8') as f:
                f.write(content)
                print("已经保存为:", fileName)
        except Exception as e:
            print(e)


class wenkuAPI:
    def __init__(self, keyWord):
        self.keyWord = keyWord

    def downloadDocs(self, urls):
        for url in urls:
            print("文档链接为：" + url)
            driver.get(url)
            try:
                continueToRead = driver.find_element_by_xpath("//div[@class='foldpagewg-text-con']")  # 查找继续阅读的按钮
                continueToRead.click()
            except Exception as e:
                print(e) # 继续阅读的按钮不存在
            # 此处返回渲染完毕后的百度文库页面
            html = driver.execute_script("return document.documentElement.outerHTML")
            t = BeautifulSoup(html, 'lxml')
            t2 = t.find_all("p", class_=re.compile("rtcscls\d_r_\d"))
            content = "\n".join([x.text for x in t2])
            title = t.title.text.split(' - ')[0]
            osAPI.saveFile(fileName=title, content=content, dirName=self.keyWord)

    def searchAPI(self, keyWord, num):
        docsParam = r"<a href=\"(https:\/\/wenku\.baidu\.com\/view\/.+\.html\?from=search)\""  # 不是很好看的正则
        params = {
            'word': keyWord,
            'od': 2,
            'pn': (num - 1) * 10
        }
        res = requests.get(wenkuSearchURL, headers=headers, params=params)
        res.encoding = 'gb2312'
        content = res.text
        return re.findall(docsParam, content)


def main():
    print("启动浏览器准备就绪")
    print("输入文库搜索关键词：")
    keyWord = input()
    print("输入需要文档搜索页数（例如 1-10，一般来说 1 页 10 个文件）：")
    nums = input().split('-')
    minPage = nums[0]
    maxPage = nums[1]
    print("你将要以 「" + keyWord + "」 为关键词搜索，最小页数为 " + minPage + " ，最大页数为 " + maxPage)
    print("确认点击 「Enter」 键")
    input()
    print("正在创建目录 " + keyWord)
    osAPI.createDIR(dirName=keyWord)
    for num in range(int(minPage), int(maxPage) + 1):
        print("正在搜索第" + str(num) + "页结果")
        allURL = wenkuAPI(keyWord=keyWord).searchAPI(keyWord=keyWord, num=num)
        wenkuAPI(keyWord=keyWord).downloadDocs(urls=allURL)

    driver.quit()  # 退出浏览器
    print("资料收集完毕，回车退出程序")
    input()


if __name__ == '__main__':
    main()
