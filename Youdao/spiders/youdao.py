# -*- coding: utf-8 -*-
import scrapy
import time
import random
from hashlib import md5
import json

from ..items import YoudaoItem


class YoudaoSpider(scrapy.Spider):
    name = 'youdao'
    allowed_domains = ['fanyi.youdao.com']
    post_url='http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    word=input('请输入要翻译的单词:')

    def start_requests(self):
        ts, salt, sign = self.get_salt_sign_ts()
        formdata = {
            "i": self.word,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": salt,
            "sign": sign,
            "ts": ts,
            "bv": "65313ac0ff6808a532a1d4971304070e",
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME",
        }

        yield scrapy.FormRequest(
            url=self.post_url,
            formdata=formdata,
            callback=self.parse,
            cookies=self.get_cookies()
        )

    def get_cookies(self):
        cookie="OUTFOX_SEARCH_USER_ID=-769428740@10.169.0.84; JSESSIONID=aaa6Y0U-5XxdFag4K9T5w; OUTFOX_SEARCH_USER_ID_NCOO=1495411215.9552743; ___rl__test__cookies=1573805083428"
        cookies={}
        c_list=cookie.split('; ')
        for c in c_list:
            cookies[c.split('=')[0]]=c.split('=')[1]
        return cookies

    def get_salt_sign_ts(self):
        ts=str(int(time.time()*1000))
        salt=ts+str(random.randint(0,9))
        string='fanyideskweb'+self.word+salt+'n%A-rKaT5fb[Gy?;N5@Tj'
        s=md5()
        s.update(string.encode())
        sign=s.hexdigest()
        return ts,salt,sign

    def parse(self, response):
        item=YoudaoItem()
        html=json.loads(response.text)
        item['result']=html['translateResult'][0][0]['tgt']
        yield item
