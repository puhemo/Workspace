#! python3
# encoding: utf-8

try:
    import os
    import json
    import re
    from io import BytesIO
    from PIL import Image
    import bs4
    import requests
    import progressbar
except Exception as error:
    print("MISSING SOME MODULE(s)")
    print (error)
    os.system("pip install beautifulsoup4 Pillow requests progressbar ")
    print("TRY TO INSTALL SOME MODs")
    print("PLEASE UPGRADE PIP IF IT DOESN'T WORK ")
    print("Restart this Program!")
    exit(-2)

print("""
        1688 Item Image Spider
""")

def getHtml(url):
    headers = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }
    res = requests.get(url, headers = headers, timeout = 10)
    res.raise_for_status()	
    return res

def saveImg(imgUrl, folder):
    bar = progressbar.ProgressBar(redirect_stdout=True)
    n = 0
    for url in bar(imgUrl):
        n = n + 1
        print("\nGET %s %d >>> " % (folder, n) + url)
        res = getHtml(url)
        data = res.content
        im = Image.open(BytesIO(data))
        ### 宽/高的像素小于300
        if im.size[0] < 300 or im.size[1] < 300:
            print("\nGET <<< USELESS IMG")
            im.close()
            continue
        imgFolder = os.path.join(baseFolder, folder)
        os.makedirs(imgFolder, exist_ok=True)
        imgName = str(n) + '.jpg'
        f = open(os.path.join(imgFolder, imgName), 'wb')
        f.write(data)
        f.close()

url = input('Enter 1688 Url - ')
baseFolder = os.path.basename(url).split('.')[0]

res = getHtml(url)
soup = bs4.BeautifulSoup(res.text, "html.parser")

# Get gallery/color image
m_urls = []
els= soup.select('li[data-imgs]')
for el in els:
    data = el.get('data-imgs')
    url = json.loads(data)['original']
    m_urls.append(url)

# Get description image
elems = soup.select('#desc-lazyload-container')
html =  elems[0].get('data-tfs-url')
data = getHtml(html).text
d_re = 'img alt.*? src.*?(//.*?jpg)'
d_urls = ['https:' + d_url for d_url in re.findall(d_re, data)]

saveImg(m_urls, 'main')
saveImg(d_urls, 'detail')

print("\nHi~Finished~~~")