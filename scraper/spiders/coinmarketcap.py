import scrapy
import re


class EventItem(scrapy.Item):
    Name = scrapy.Field()
    Symbol = scrapy.Field()
    MarketCap = scrapy.Field()
    Price = scrapy.Field()
    CirculatingSupply = scrapy.Field()
    Volume = scrapy.Field()
    Percent_1h = scrapy.Field()
    Percent_24h = scrapy.Field()
    Percent_7d = scrapy.Field()


class NewEvents (scrapy.Spider):
    name = "coinmarketcap"
    allowed_domains = ['https://coinmarketcap.com']
    start_urls = ['https://coinmarketcap.com/all/views/all/']

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self._parse_data, dont_filter=True)

    def _parse_data(self, response):
        fields = [
            '',
            'Symbol',
            'MarketCap',
            'Price',
            'CirculatingSupply',
            'Volume',
            'Percent_1h',
            'Percent_24h',
            'Percent_7d'
        ]
        trs = response.xpath('//table//tbody//tr[@id]')
        for tr in trs:
            item = EventItem()
            for i in range(1, 10):
                value = [
                    val.strip()
                    for val in tr.xpath('.//td[position()={position} and a]/a/text() |'
                                        ' .//td[position()={position}]/text()'.format(position=i+1)).extract()
                    if val.strip()
                ]
                if fields[i-1] != 'Symbol' and fields[i-1] != 'Name':
                    value = value[0].replace('?', '').replace('*', '').replace('$', '').replace('%', '').replace(',', '').replace('Low ', '').replace('Vol', '0').encode('utf-8') if value else None
                    item[fields[i-1]] = value if value else None
                else:
                    item[fields[i-1]] = value[0].encode('utf-8') if value else ''
            yield item
