import json
import scrapy
from lxml import etree
from scrapy import signals


class LicenseSpider(scrapy.Spider):
    name = "license_spider"

    start_urls = []
    processed_urls = set()  # 用于存储已处理的唯一URL

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(LicenseSpider, cls).from_crawler(crawler, *args, **kwargs)
        # 连接 spider_closed 信号
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def __init__(self, *args, **kwargs):
        super(LicenseSpider, self).__init__(*args, **kwargs)
        # 从 urls.json 文件中读取 URL
        with open('urls.json', 'r') as file:
            data = json.load(file)
            self.start_urls = [entry['url'] for entry in data if 'url' in entry]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, errback=self.errback)

    def parse(self, response):
        # 提取 POM 文本
        pom_text = response.css('pre[data-test="pom-file"]::text').get()

        if pom_text:
            # 解析 XML
            root = etree.fromstring(pom_text.encode('utf-8'))

            # 注册命名空间，以便在 XPath 查询中使用
            namespaces = {'m': 'http://maven.apache.org/POM/4.0.0'}

            # 提取 license name 和 url
            licenses = root.findall('.//m:licenses/m:license', namespaces)
            for license in licenses:
                license_name = license.find('m:name', namespaces).text
                license_url = license.find('m:url', namespaces).text

                self.processed_urls.add(response.url)
                yield {
                    'url': response.url,
                    'license_name': license_name,
                    'license_url': license_url,
                }

            # 无命名空间
            licenses = root.findall('.//licenses/license')
            for license in licenses:
                license_name = license.find('name').text
                license_url = license.find('url').text

                self.processed_urls.add(response.url)
                yield {
                    'url': response.url,
                    'license_name': license_name,
                    'license_url': license_url,
                }

        # 提取所有 <li data-test="license"> 元素的文本
        license_names = response.css('li[data-test="license"]::text').getall()
        for license_name in license_names:
            self.processed_urls.add(response.url)
            yield {
                'url': response.url,
                'license_name': license_name,
            }

    def errback(self, failure):
        self.logger.error(f'Request failed: {failure.request.url}')

    def spider_closed(self, spider):
        print(f'Processed {len(self.processed_urls)} unique URLs.')

# 要运行这个爬虫，请在命令行中使用以下命令：
# scrapy runspider spider.py -o licenses.json

# input: urls.json
# output: licenses.json
