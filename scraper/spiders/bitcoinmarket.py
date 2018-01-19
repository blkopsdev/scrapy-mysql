import scrapy
import re


class EventItem(scrapy.Item):
    Source = scrapy.Field()
    Pair = scrapy.Field()
    Volume_hr = scrapy.Field()
    Price = scrapy.Field()
    Volume_per = scrapy.Field()
    Updated = scrapy.Field()


class NewEvents (scrapy.Spider):
    name = "bitcoinmarket"
    allowed_domains = ['https://coinmarketcap.com']
    start_urls = ['https://coinmarketcap.com/currencies/bitcoin/']

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self._parse_data, dont_filter=True)

    def _parse_data(self, response):
        fields = [
            'Source',
            'Pair',
            'Volume_hr',
            'Price',
            'Volume_per',
            'Updated'
        ]
        trs = response.xpath('//table//tbody//tr')
        for tr in trs:
            item = EventItem()
            for i in range(1, 7):
                value = [
                    val.strip()
                    for val in tr.xpath('.//td[position()={position} and a]/a/text() |'
                                        ' .//td[position()={position} and span]/span/text() |'
                                        ' .//td[position()={position} and not(span)]/text()'.format(position=i+1)).extract()
                    if val.strip()
                ]
                if fields[i-1] != 'Source' and fields[i-1] != 'Pair' and fields[i-1] != 'Updated':
                    item[fields[i - 1]] = value[0].replace('?', '').replace('*', '').replace('$', '').replace('%', '').replace(',', '').encode('utf-8') if value else None
                else:
                    item[fields[i-1]] = value[0].encode('utf-8') if value else ''

            yield item
