# 测试模块
import buff_spider
from models import Goods


def main():
    goods = Goods()
    goods.buff_info.url = "https://buff.163.com/goods/11475?from=market#tab=selling"
    goods.update_buff_info()


if __name__ == "__main__":
    main()
