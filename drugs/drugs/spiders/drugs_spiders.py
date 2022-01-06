import scrapy


class QuotesSpider(scrapy.Spider):
    name = "drugs"
    start_urls = [
        'https://www.webmd.com/drugs/2/index',
    ]
    def parse(self, response):
        yield {
            # 'first_link': response.css('div.drugs-search-list-conditions li a::attr(href)').get(),
            'alphabet': response.css('li.sub-alpha-square a::text').get(),
            'drugs' : response.css('div.drugs-search-list-conditions li a::text').getall()
        }

        start_urls = response.css('div.alpha-container li a::attr(href)').getall()
        for url in start_urls:
            # text = response.css('div.alpha-container li a::text').get()
            if url is not None:
                url = 'https://www.webmd.com' + url
                sub_urls = response.css('li.sub-alpha-square  a::attr(href)').getall()
                for sub in sub_urls:
                    if sub is not None:
                        sub = 'https://www.webmd.com' + sub 
                        yield response.follow(sub, callback=self.parse)
                        
                yield response.follow(url, callback=self.parse)
        

# response.css('div.alpha-container li a::attr(href)').geall()====>list of all urls

# response.css('div.drugs-search-list-conditions li a::text').getall()====>give all drugs

# response.css('div.alpha-container li a::text').getall() =====>getting alphabets

# response.css('li.sub-alpha-square  a::attr(href)').getall()