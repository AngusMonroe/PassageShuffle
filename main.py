import re
from random import shuffle

import urllib.request
from HandleJs import Py4Js


def open_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req)
    data = response.read().decode('utf-8')
    return data


def translate(content, tk, sl='en', tl='zh-CN'):
    if len(content) > 4891:
        print("翻译的长度超过限制！！！")
        return

    content = urllib.parse.quote(content)

    url = "http://translate.google.cn/translate_a/single?client=t&sl=%s&tl=%s&hl=%s&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1&srcrom=0&ssel=0&tsel=0&kc=2&tk=%s&q=%s" % (
    sl, tl, tl, tk, content)

    # 返回值是一个多层嵌套列表的字符串形式，解析起来还相当费劲，写了几个正则，发现也很不理想，
    # 后来感觉，使用正则简直就是把简单的事情复杂化，这里直接切片就Ok了
    result = open_url(url)

    end = result.find("\",")
    if end > 4:
        print(result[4:end])
        return result[4:end]
    return ''


def en2zh(content):
    js = Py4Js()

    tk = js.getTk(content)
    return translate(content, tk)


def zh2en(content):
    js = Py4Js()

    tk = js.getTk(content)
    return translate(content, tk, sl='zh-CN', tl='en')


if __name__ == "__main__":
    # test()

    f_in = open('input.txt', 'r', encoding='utf8')
    f_out = open('output.txt', 'w', encoding='utf8')

    txt = f_in.read()
    txt = re.sub('\n', ' ', txt)

    txt_en = zh2en(txt)
    txt_zh = en2zh(txt)

    sents = txt[:-1].split('。')
    shuffle(sents)

    f_out.write('。'.join(sents))

    f_in.close()
    f_out.close()
    print('Done!')
