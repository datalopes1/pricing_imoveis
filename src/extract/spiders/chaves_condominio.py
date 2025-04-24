import scrapy


class ChavesCondominioSpider(scrapy.Spider):
    name = "chaves_condominio"
    allowed_domains = ["www.chavesnamao.com.br"]
    start_urls = ["https://www.chavesnamao.com.br/casas-em-condominio-a-venda/ce-fortaleza/"]
    page_count = 1
    max_page = 99

    def parse(self, response):
        imoveis = response.css('span.card-module__cvK-Xa__cardContent')
        
        for imovel in imoveis:
            raw_area = imovel.css('p.styles-module__aBT18q__body2.undefined::text').getall()
            condos = imovel.css('span.card-module__cvK-Xa__cardContent p small::text').getall()

            yield {
                'preco' : imovel.css('span.card-module__cvK-Xa__cardContent p b::text').get(),
                'tipo' : 'Condomínio',
                'localizacao' : imovel.css('address p:nth-of-type(2)::text').get(),
                'area' : raw_area[1] if raw_area else None,
                'quartos' : imovel.css('span.style-module__Yo5w-q__list p:nth-of-type(2)::text').get(),
                'banheiros' : imovel.css('span.style-module__Yo5w-q__list p:nth-of-type(4)::text').get(),
                'vagas' : imovel.css('span.style-module__Yo5w-q__list p:nth-of-type(3)::text').get(),
                'condo' : condos[1] if condos else None,

            }

        if self.page_count < self.max_page:
            next_page = response.css('span.row.w100.style-module__yjYI8a__nextlink a::attr(href)').get()
            if next_page:
                self.page_count += 1
                next_page_url = response.urljoin(next_page)
                yield scrapy.Request(url=next_page_url, callback=self.parse)