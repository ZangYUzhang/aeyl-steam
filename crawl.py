# 测试模块
import asyncio
import buff_spider
import aiohttp


async def main():
    url = "https://buff.163.com/goods/11475?from=market#tab=selling"
    session = aiohttp.ClientSession()
    await buff_spider.get_goods_info(url, session)
    await session.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
