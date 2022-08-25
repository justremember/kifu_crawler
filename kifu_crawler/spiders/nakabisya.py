import scrapy


class NakabisyaSpider(scrapy.Spider):
    name = 'nakabisya'
    allowed_domains = ['nakabisyakihu.seesaa.net', 'noike.info']
    start_urls = ['http://nakabisyakihu.seesaa.net/article/453744960.html']

    def parse(self, response):
        kif_app_url = response.css('iframe::attr(src)').get()
        file_url = kif_app_url.replace('index.html', 'form.csa')
        file_name = response.css('h2.article__title::text').get().replace('/', ' ') + '.csa'
        yield {
                'file_url': file_url,
                'file_name': file_name
                }
        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


