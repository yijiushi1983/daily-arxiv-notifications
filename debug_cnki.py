import requests

urls = [
    'https://search.cnki.com.cn/Search.aspx?q=%E6%B7%B1%E5%9C%B0%E5%AE%9E%E9%AA%8C%E5%AE%A4',
    'https://search.cnki.com.cn/Search.aspx?q=深地实验室',
    'https://world.cnki.net/search/defaultresult/index?query=%E6%B7%B1%E5%9C%B0%E5%AE%9E%E9%AA%8C%E5%AE%A4',
    'https://kns.cnki.net/kns8/defaultresult/index?v=&uniplatform=NZKPT&searchcode=WD&SearchText=深地实验室',
]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

for url in urls:
    try:
        r = requests.get(url, headers=headers, timeout=20)
        print('URL:', url)
        print('Status', r.status_code)
        print('Len', len(r.text))
        print(r.text[:600])
        print('------')
    except Exception as e:
        print('ERR', url, e)
