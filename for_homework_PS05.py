import scrapy

class LightingSpider(scrapy.Spider):
    name = 'lighting'
    allowed_domains = ['ststroitel.ru']
    start_urls = ['https://ststroitel.ru']

    def parse(self, response):
        # Извлекаем ссылки на страницы с продуктами
        product_links = response.css('div.product-item a.product-link::attr(href)').getall()
        for link in product_links:
            yield response.follow(link, self.parse_product)

        # Пагинация: находим следующую страницу и переходим к ней
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_product(self, response):
        # Извлекаем название, цену и ссылку на источник освещения
        title = response.css('h1.product-title::text').get().strip()
        price = response.css('span.product-price::text').get().strip()
        link = response.url

        yield {
            'title': title,
            'price': price,
            'link': link
        }

