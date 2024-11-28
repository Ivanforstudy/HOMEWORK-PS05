import scrapy

class AllLightsSpider(scrapy.Spider):
    name = "all-lights"
    allowed_domains = ["ststroitel.ru"]
    start_urls = ["https://www.ststroitel.ru/catalog/osveshchenie/"]

    # Добавляем ссылку на конкретный продукт
    specific_product_url = "https://www.ststroitel.ru/catalog/osveshchenie/lampy_svetodiodnye/lenty_svetodiodnye/192603/"
    def parse(self, response):
        # Извлекаем ссылки на продукты
        product_links = response.css('div.product-item a.product-link::attr(href)').getall()
        if product_links:
            # Переходим к первому продукту
            yield response.follow(product_links[0], self.parse_product)
        # Переходим к конкретному продукту
        yield response.follow(self.specific_product_url, self.parse_product)
        # Пагинация: находим следующую страницу и переходим к ней
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
    def parse_product(self, response):
        # Извлекаем детали продукта
        title = response.css('h1.product-title::text').get()
        price = response.css('span.product-price::text').get()
        link = response.url
        yield {
            'title': title,
            'price': price,
            'link': link
        }
# Для запуска:scrapy crawl all-lights -o output.json
