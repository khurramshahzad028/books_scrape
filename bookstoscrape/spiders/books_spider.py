import scrapy


class BooksToScrape(scrapy.Spider):
    name = "bookstoscrape"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        products = response.xpath('//article[@class="product_pod"]')
        for product in products:
            product_url = product.xpath(
                './/div[@class="image_container"]/a/@href').get()

            yield response.follow(product_url, callback=self.product_details)

        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if (next_page is not None):
            yield response.follow(next_page, callback=self.parse)

    def product_details(self, response):
        yield {

            'Product_url':
            response.xpath('.//div[@class="image_container"]/a/@href').get(),

            'Breadcrumb':
            response.xpath('//ul[@class="breadcrumb"]/li/a/text()').getall(),

            'Product_title':
            response.xpath(
                '//div[@class="col-sm-6 product_main"]/h1/text()').get(),

            'Product_price':
            response.xpath(
                '//div[@class="col-sm-6 product_main"]/p/text()').get(),

            'Image_url':
            response.xpath('//div[@id="product_gallery"]//img/@src').get(),

            'Product_description':
            response.xpath
                (
                '//div[@id="product_description"]/following-sibling::p/text()'
                ).get(),

            'UPC':
            response.xpath(
                '//table[@class="table table-striped"]//th[text()="UPC"]/'
                'following-sibling::td/text()'
                ).get(),

            'Available':
            response.xpath(
                '//table[@class="table table-striped"]//th'
                '[text()="Availability"]/following-sibling::td/text()'
                ).get(),

            'Number of reviews':
            response.xpath('//table[@class="table table-striped"]//th[text()='
                           '"Number of reviews"]/following-sibling::td/text()'
                           ).get(),

            'Product_rating':
            response.xpath('//div[@class="col-sm-6 product_main"]/p'
                           '/following-sibling::p/following-sibling::p/@class'
                           ).get(),
        }
