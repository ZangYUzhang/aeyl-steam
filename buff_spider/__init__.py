# 爬取buff平台的商品信息
import asyncio
import aiohttp
from lxml.html import etree
import re
import json
import traceback
import os
from util import fetch_url


async def get_goods_info(url, session):
    # 获取商品信息
    print(url)
    # 最多重试3次
    for i in range(3):
        try:
            html_content = await fetch_url(url, session)
            result = await parse_html(html_content, session)
            result.insert(0, url)
            print(result)
            return result
        except:
            traceback.print_exc()
            continue

    # 上抛异常
    raise RuntimeError("商品信息获取失败")


def read_headers():
    # 读取headers.txt文件，返回键值对
    filePath = os.path.join(os.path.dirname(__file__), 'headers.txt')
    with open(filePath, 'r', encoding='utf-8') as f:
        text = f.read()
    # 键值对
    headers = {}
    for line in text.split('\n'):
        if line:
            key, value = line.split(': ')
            headers[key] = value
    return headers


async def get_sell_info(goods_id, session):
    # 获取在售情况
    sell_info_url = f"https://buff.163.com/api/market/goods/sell_order?game=dota2&goods_id={goods_id}&page_num=1&sort_by=default&mode=&allow_tradable_cooldown=1&_=1693538617921"
    sell_info = json.loads(await fetch_url(sell_info_url, session))
    return sell_info


async def get_buy_info(goods_id, session):
    # 获取求购情况
    buy_info_url = f"https://buff.163.com/api/market/goods/buy_order?game=dota2&goods_id={goods_id}&page_num=1&_=1693540558052"
    buy_info = json.loads(await fetch_url(buy_info_url, session))
    return buy_info


async def get_deal_info(goods_id, session):
    # 获取成交情况
    deal_info_url = f"https://buff.163.com/api/market/goods/bill_order?game=dota2&goods_id={goods_id}&_=1693543131027"
    deal_info = json.loads(await fetch_url(deal_info_url, session))
    return deal_info


async def parse_html(htmlContent, session):
    # 解析html文本，返回商品信息
    root = etree.HTML(htmlContent)
    # 商品名称
    try:
        goods_name = root.xpath('//div[@class="detail-cont"]/div[1]/h1/text()')[0]
    except:
        print(htmlContent)
        raise RuntimeError("商品名称获取失败")
    # 在售商品数量
    goods_num = root.xpath('//ul[@class="new-tab"]/li[1]/a/text()')[0]
    goods_num = re.findall("当前在售\((\d+)\)", goods_num)[0]
    goods_num = int(goods_num)
    # steam市场链接
    steam_url = root.xpath('//div[@class="detail-summ"]/a/@href')[0]
    goods_id = root.xpath('//a[@class="i_Btn i_Btn_mid i_Btn_D_red btn-supply-buy"]/@data-goodsid')[0]

    # 异步获取在售情况、求购情况和成交情况
    sell_info_task = get_sell_info(goods_id, session)
    buy_info_task = get_buy_info(goods_id, session)
    # deal_info_task = get_deal_info(goods_id, session)

    sell_info, buy_info = await asyncio.gather(sell_info_task, buy_info_task)

    # 在售最低价
    lowest_price = float(sell_info['data']['items'][0]['price']) if sell_info['data']['items'] else 0
    # 求购最高价
    highest_price = float(buy_info['data']['items'][0]['price']) if buy_info['data']['items'] else 0

    # 最新成交价
    # latest_price = float(deal_info['data']['items'][0]['price']) if deal_info['data']['items'] else 0

    result = [goods_id, goods_name, goods_num, steam_url, lowest_price, highest_price]
    return result


async def getGoodsUrls(session):
    # 获取商品链接
    url = "https://buff.163.com/api/market/goods?game=dota2&page_num={}&_=1693544159600"
    urls = []
    for pageNum in range(1, 6):
        goods_info = json.loads(await fetch_url(url.format(pageNum), session))
        goods_base_url = "https://buff.163.com/goods/{}?from=market#tab=selling"
        urls += [goods_base_url.format(i["id"]) for i in goods_info['data']['items']]
    return urls
