# 定义各种实体类模型
class PriceInfo:
    # 饰品价格信息模型
    def __init__(self):
        self.url = None                     # 平台指定“商品地址”
        self.min_price = None               # 商品最低售价
        self.latest_sale_price = None       # 商品最新成交价
        self.latest_buy_price = None        # 商品最新求购价    
        self.update_time = None             # 商品更新时间

class Cosmetic:
    # 饰品信息模型
    def __init__(self):
        self.name_cn = ""                    # 商品名称（中文）
        self.name_en = ""                    # 商品名称英文（market hash name）
        self.secondary_attribute = ""        # 饰品的次要属性
        self.update_time = None              # 数据最后更新时间
        self.c5_info = PriceInfo()           # C5平台价格信息
        self.buff_info = PriceInfo()         # BUFF平台价格信息
        self.steam_info = PriceInfo()        # Steam平台价格信息

