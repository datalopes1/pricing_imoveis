import scrapy


class LopesSpider(scrapy.Spider):
    name = "lopes"
    allowed_domains = ["www.lopes.com.br"]
    start_urls = ["https://www.lopes.com.br/busca/venda/br/ce/fortaleza"]
    page_count = 1
    max_page = 99

    def parse(self, response):
        imoveis = response.css('div.card.ng-star-inserted')
        
        for imovel in imoveis:

            yield {
                'preco' : imovel.css('p.price.ng-star-inserted::text').get(),
                'tipo' : imovel.css('h2.type.ng-star-inserted::text').get(),
                'localizacao' : imovel.css('p.location::text').get(),
                'area' : imovel.css('ul li:nth-child(1) p::text').get(),
                'quartos' : imovel.css('ul li:nth-child(2) p::text').get(),
                'banheiros' : imovel.css('ul li:nth-child(3) p::text').get(),
                'vagas' : imovel.css('ul li:nth-child(4) p::text').get(),
                'condo' : imovel.css('ul.subprices.ng-star-inserted li span::text').get()
            }

        if self.page_count < self.max_page:
            next_page = response.css('li.page-item.page-item-next.ng-star-inserted a::attr(href)').get()
            if next_page:
                self.page_count += 1
                next_page_url = response.urljoin(next_page)
                yield scrapy.Request(url=next_page_url, callback=self.parse)