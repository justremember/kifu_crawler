import scrapy
import re


class NakabisyaSpider(scrapy.Spider):
    name = 'nakabisya'
    allowed_domains = ['nakabisyakihu.seesaa.net', 'noike.info']
    start_urls = ['http://nakabisyakihu.seesaa.net/article/453744960.html']

    def parse(self, response):
        kif_app_url = response.css('iframe::attr(src)').get()
        file_url = kif_app_url.replace('index.html', 'form.csa')
        file_name = response.css('h2.article__title::text').get().replace('/', ' ')
        kif_contents = response.css('.article__content').re_first(r'</iframe>.*<a name="more">')
        if kif_contents:
            kif_contents = kif_contents.replace('</iframe>', '').replace('<a name="more">', '').replace('<br>', '\n')
            # remove all html tags
            html_tags = re.compile(r'<.*?>')
            kif_contents = re.sub(html_tags, '', kif_contents)
            # remove duplicate newlines
            dup_newlines = re.compile(r'\n+')
            kif_contents = re.sub(dup_newlines, '\n', kif_contents.strip())

        yield {
                'file_url': file_url,
                'file_name': file_name,
                'kif_contents': kif_contents
                }
        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


