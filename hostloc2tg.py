# -*- encoding: utf-8 -*-

import requests
from urllib import parse
from lxml import etree
import time
import datetime
from torequests.utils import curlparse


# 获得标准日期
def get_week_day(date):
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期日',
    }
    day = date.weekday()
    return week_day_dict[day]


# 获得网站内容
def get_content(url):
    while True:
        try:
            s = requests.get(url)
            hostloc_content = etree.HTML(s.content).xpath('//table/tr/td[@class="t_f"]/text()')

            if not hostloc_content:
                return "因权限原因，内容无法预览，请手动登陆查看！"
            else:
                s = ''
                for j in hostloc_content:
                    s = s + j
                # 不展示全部内容，防止内容过长，严重影响体验
                return s[0:80].replace("\r\n", '').replace('\n', '').replace('\xa0', '').replace('\u200b', '')

        except Exception as e:
            print("网络原因，无法访问，请稍后再试...")


def mark_down(content):
    # 删除特殊符号，防止发生错误parse
    sign = ['&', '.', '<', '>', ' ', '?', '"', "'", '#', '%', '!', '@', '$', '^', '*', '(', ')', '-', '_', '+', '=', '~', '/', ',', ':', '’', '‘', '“', '”', '%', '^', '——', '{', '}', '*', '[', '、', '\\', ']', '`', '"', "'", '\n']
    for k in sign:
        content = content.replace(k, "")
    return content


# 通过机器人推送到频道或者个人
# 如果推送到频道需要将机器人加入频道并设置为管理员给予权限
def post(chat_id, text):
    try:
        text = parse.quote(text)
        post_url = 'https://api.telegram.org/bot854093881:AAE47iYK**************/sendMessage' \
                   '?parse_mode=MarkdownV2&chat_id={0}&text={1}'.format(chat_id, text)
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'}
        requests.get(post_url, headers=headers)
    except Exception:
        print("推送失败！")
        pass


hostloc_list = {"hello"}
url_1 = "https://www.hostloc.com/"
headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
}
url_hostloc = "https://www.hostloc.com/forum.php?mod=forumdisplay&fid=45&filter=author&orderby=dateline"
while True:
    try:
        r = requests.get(url_hostloc, headers=headers)
        xml_content = etree.HTML(r.content)
        href_list = xml_content.xpath('/html/body/div[@id="wp"]/div[5]/div/div/div[4]/div[2]/form/table/tbody/tr/th/a[3]/@href')
        author = xml_content.xpath('/html/body/div[@id="wp"]/div[5]/div/div/div[4]/div[2]/form/table/tbody/tr/td[2]/cite/a/text()')
        author_url = xml_content.xpath('/html/body/div[@id="wp"]/div[5]/div/div/div[4]/div[2]/form/table/tbody/tr/td[2]/cite/a/@href')
        number = xml_content.xpath('/html/body/div[@id="wp"]/div[5]/div/div/div[4]/div[2]/form/table/tbody/tr/td[3]/a/text()')
        href = xml_content.xpath('/html/body/div[@id="wp"]/div[5]/div/div/div[4]/div[2]/form/table/tbody/tr/th/a[3]/text()')
        print(author)
        print(number)
        for i in range(len(number)):
            if number[i] == '0':
                if str(href[i].replace("\r\n", "")) not in hostloc_list:
                    hostloc_list.add(str(href[i].replace("\r\n", "")))
                    name = href[i].replace("\r\n", "")
                    # 文章链接
                    # print(i)
                    k = i + 1
                    # print(k)
                    url_list = "https://www.hostloc.com/{}".format(href_list[i])
                    # 作者id链接
                    url_author = "https://www.hostloc.com/{}".format(author_url[k])
                    # 时间戳
                    time_1 = time.strftime("%Y-%m-%d    %H:%M:%S", time.localtime())
                    date_1 = get_week_day(datetime.datetime.now())
                    time_2 = time_1 + '    ' + date_1 + '    '
                    time2 = str(time_2).replace('-', '\\-')
                    # 获得预览内容
                    print(get_content(url_list))
                    content_2 = mark_down(get_content(url_list))
                    text = '主        题：' + "***{}***".format(mark_down(name)) + '\n' + '发  布  者：[{0}]({1})'.format(mark_down(author[i + 1]), url_author) + '\n' + '时        间：' + time2 + '\n' + '内容预览：[点击查看——{0}]({1})'.format(content_2, url_list)
                    print(text)
                    # 自己设置推送的id，频道id为负数，个人id为正数
                    post('-100*********', text)
                else:
                    pass
            else:
                pass
        # 多少秒抓取一次网站，自己设定，不要太小，会被ban ip的
        time.sleep(15)
    except Exception as e:
        pass
