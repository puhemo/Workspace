#! python3
# encoding: utf-8

try:
    import os
    import re
    import bs4
    import requests
    from io import BytesIO
    from PIL import Image
except Exception as error:
    print("MISSING SOME MODULE(s)")
    print (error)
    os.system("pip install beautifulsoup4 Pillow requests ")
    print("TRY TO INSTALL SOME MODs")
    print("PLEASE UPGRADE PIP IF IT DOESN'T WORK ")
    print("Restart this Program!")
    exit(-2)
print("""
        Taobao Item Image Spider
""")

def saveName(folder, name):
    Folder = os.path.join(itemId, folder)
    os.makedirs(Folder, exist_ok=True)
    fname =  os.path.join(Folder, name)
    return fname

# 保存图片
def saveImg(imgDict):
    for url in imgDict.keys():
        print("\nGET >>> %s " % url)
        headers = {
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }
        res = requests.get(url, headers = headers, timeout = 10)
        data = res.content
        im = Image.open(BytesIO(data))
        ### 宽/高的像素小于300
        if im.size[0] < 300 or im.size[1] < 300:
            print("\nGET <<< USELESS IMG")
            im.close()
            continue
        f = open(imgDict[url], 'wb')
        f.write(data)
        f.close()

url = input('Enter Taobao Url - ')
if len(url) < 1:
    url = 'https://item.taobao.com/item.htm?spm=a230r.1.14.163.zx416O&id=534076017689&ns=1&abbucket=18#detail'
print('URL:', url)
itemId = re.findall('id=(\d+)', url)[0]

res = requests.get(url)
res.raise_for_status()

reg = r"descUrl.*?location.protocol==='http:' \? '//(.*?)'.?:"
desurl = 'http://' + re.findall(reg, res.text)[0]
req = requests.get(desurl)
req.raise_for_status()
Soup = bs4.BeautifulSoup(req.text, "html.parser")
itemDesc = Soup.select('img')
d_dict = {}
d = 0
for item in itemDesc:
    img_url = item.get('src')
    if img_url == None:
        continue
    d += 1
    d_name = str(d) + '.jpg'
    dName = saveName('detail', d_name)
    d_dict[img_url] = dName

soup = bs4.BeautifulSoup(res.text, "html.parser")
els = soup.select('div[class="tb-pic tb-s50"] > a > img')
m_dict = {}
n = 0
for el in els:
    n += 1
    m_name = str(n) + '.jpg'
    mName = saveName('main', m_name)
    m_data = el.get('data-src').split('_')
    m_url = 'https:' + '_'.join(m_data[:len(m_data)-1])
    m_dict[m_url] = mName

c_dict = {}
cels = soup.select('li[data-value] > a')

for cel in cels:
    c_name = cel.getText().strip('\n') + '.jpg'
    # 替换不支持文件名字符：'/\:*?"<>|'
    c_name = c_name.translate(str.maketrans("|\\?*<\":>+[]/'", '_'*13)) 
    cName = saveName('color', c_name)
    c_data = cel.get('style')
    if c_data == None:
        continue
    try:
        c_url = 'https:' + re.findall('(//.*?jpg?)_\d\dx\d\d', c_data)[0]
    except:
        c_url = 'https:' + re.findall('(//.*?png?)_\d\dx\d\d', c_data)[0]
    c_dict[c_url] = cName

saveImg(m_dict)
saveImg(c_dict)
saveImg(d_dict)

print("\nHi~Finished~~~")
