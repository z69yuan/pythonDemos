#coding=utf-8  // 写入UTF-8的命令声明
import requests
from bs4 import BeautifulSoup
import re

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from binascii import a2b_base64


from lxml import etree

print("hello world")
print("人生苦短,我用Python！")




def requestUrl(queryKeyWord):
    if len(queryKeyWord) == 0:
        return
    else:
        response = requests.get("https://www.gsmarena.com/res.php3?sSearch=" + queryKeyWord)
        # html = """
        # <script>
        #     const KEY  = "BOiYMJ+RguIgeFLwLDlr2A==";
        #     const IV   = "l3HODr7QRYZrItBZJ2ZuYw==";
        #     const DATA = "x9vqVKGr4nqsIGwey7tQ1GlT6AMlSk77KSE2RxOno7A...";
        # </script>
        # <script>
        # </script>
        # """
        # soup = BeautifulSoup(html,'lxml')
        soup = BeautifulSoup(response.text,'lxml')
        scripts = soup.find_all('script')
        for cur in scripts:
            script = cur.string
            try:
                key = re.search(r'const KEY {2}= "(.*)";', script)
            except Exception as e:
                # print("An error occurred: ", e)
                continue

            # 如果没有找到 KEY、IV 和 DATA，则跳过当前的循环
            if not key:
                continue
            iv = re.search(r'const IV   = "(.*)";', script)
            data = re.search(r'const DATA = "(.*)";', script)
            # print(key.group(1))
            # print(iv.group(1))
            # print(data.group(1))

            return key.group(1),iv.group(1),data.group(1)



def aes_decrypt(key, iv, data):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(data), AES.block_size)
    return plaintext


def parsePhoneName(html):
    root = etree.fromstring(html)
    # result = root.xpath('//strong/span')[0]
    # result = root.xpath('//*[@id="review-body"]/div/ul/li/a/strong')
    # result = root.xpath('//*[@id="review-body"]/div/ul/li/a/strong/span/text()[1]')
    # result = root.xpath('//*[@id="review-body"]/div/ul/li/a/strong/span/text()[2]')
    result = root.xpath('//*[@id="review-body"]/div/ul/li/a/strong/span/text()')

    # 遍历数组，并且用空格进行拼装
    def formatFunc(s):
        return s.strip()

    newResult = list(map(formatFunc,result))
    return " ".join(newResult)

# 获取加密数据
key, iv , encryptedData = requestUrl("CPH2531")

# 转换与解密数据
key_bytes = a2b_base64(key)
iv_bytes = a2b_base64(iv)
data_bytes = a2b_base64(encryptedData)
plainHtml = aes_decrypt(key_bytes,iv_bytes,data_bytes).decode('utf-8')

# 解析一组需要的标签
i = plainHtml.index('<div class="search-more">')
plainHtml = plainHtml[0:i]

soup = BeautifulSoup(plainHtml, 'html.parser')
# 去除无用的换行
for element in soup("\n"):
    element.extract()

# Pretty-print(格式化打印) Beautiful Soup对象的字符串表示形式
formatted_html = soup.prettify()
# 格式化URL
x = formatted_html
# 解析机型名称
e = parsePhoneName(x)

print("************************")
print("plainHtml = " , e)