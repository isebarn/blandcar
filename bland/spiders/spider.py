import scrapy
from ORM import Operations
from ORM import Car


class QuotesSpider(scrapy.Spider):
    name = "cars"
    url = "https://bland.is/classified/entry.aspx?classifiedId={}"
    featuredPropWrapper = ".//div[@class='featuredPropertyWrapper']/div"
    propKey = ".//div[@class='featuredPropertyKey']/text()"
    propVal = ".//div[@class='featuredPropertyValue']/text()"
    price = "//h5[@itemprop='price']/text()"

    def start_requests(self):
        url = "https://bland.is/solutorg/farartaeki/nyir-notadir-bilar-til-solu/?categoryId=17&sub=1&page={}"
        self.saved_ids = Operations.SavedIds()

        for page in range(0, 30):
            yield scrapy.Request(url=url.format(page), callback=self.parse_page)

    def parse_page(self, response):
        vehicle_ids = [
            int(x.extract().split("=")[-1])
            for x in response.xpath('//div[@data-url]/@data-url')
        ]

        new_ids = list(set(vehicle_ids) - set(self.saved_ids))

        for new_id in new_ids:
            yield scrapy.Request(
                url=self.url.format(new_id),
                callback=self.parse_car,
                meta={'_id': new_id},
            )

    def parse_car(self, response):
        values = [
            x.extract() for x in response.xpath("//table")[0].xpath(".//td/text()")
        ]
        values = {values[x]: values[x + 1] for x in range(0, len(values), 2)}
        price = (
            response.xpath(self.price)
            .extract_first()
            .strip()
            .replace(' kr', '')
            .replace('.', '')
        )
        values['price'] = float(price) if price.isnumeric() else 0

        values['_id'] = response.meta.get('_id')

        car = Operations.SaveCar(Car(values))
