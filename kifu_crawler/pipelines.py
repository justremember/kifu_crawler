# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import FilesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request


class KifuCrawlerPipeline:
    def process_item(self, item, spider):
        return item

class CsaPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        return request.meta.get('file_name','')

    def get_media_requests(self, item, info):
        file_url = item['file_url']
        meta = {'file_name': item['file_name']}
        yield Request(url=file_url, meta=meta)
