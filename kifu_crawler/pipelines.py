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
import os


class SaveKifPipeline:
    def process_item(self, item, spider):
        kif_contents = item.get('kif_contents')
        if kif_contents:
            with open(os.path.join('kifus', item['file_name'] + '.kif'), 'w') as fo:
                fo.write(kif_contents)
        return item

class CsaPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        return request.meta.get('file_name','')

    def get_media_requests(self, item, info):
        file_url = item['file_url']
        meta = {'file_name': os.path.join('kifus', item['file_name'] + '.csa')}
        yield Request(url=file_url, meta=meta)
