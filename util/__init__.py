# 自定义工具类库

import aiohttp
import time

# 默认请求头
DEFAULT_HEADERS = {'accept': 'application/json, text/javascript, */*; q=0.01',
                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}


async def fetch_url(url: str, session: aiohttp.ClientSession, headers: dict = DEFAULT_HEADERS) -> str:
    # 发送GET请求，返回响应文本
    async with session.get(url, headers=headers) as response:
        return await response.text()


# 获取当前时间字符串
def get_current_time_str():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
