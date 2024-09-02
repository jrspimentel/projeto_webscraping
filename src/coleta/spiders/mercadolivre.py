import scrapy
from datetime import datetime

# Config a request
class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]
    page_count = 1
    max_pages = 15

    def parse(self, response):
        products = response.css('div.ui-search-result__content') # 54 itens por enquanto
        
        # Percorrer a lista com os produtos e seus respectivos elementos
        for product in products: 
          
          # Variavel do preço do produto
          prices = product.css('span.andes-money-amount__fraction::text').getall() 
          cents = product.css('span.andes-money-amount__cents::text').getall() 
          
          # Coleta e armazenamento dos dados
          yield {
            'date_created': datetime.now(),
            'brand': product.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element::text').get(),
            'name_product': product.css('h2.ui-search-item__title::text').get(),
            'old_price_reais': prices[0] if len(prices) > 0 else None,
            'old_price_centavos': cents[0] if len(cents) > 0 else None,
            'new_price_reais': prices[1] if len(prices) > 1 else None,
            'new_price_centavos': cents[1] if len(cents) > 1 else None,
            'reviews_rating_number': product.css('span.ui-search-reviews__rating-number::text').get(),
            'reviews_amount': product.css('span.ui-search-reviews__amount::text').get(),
            'source': self.name,
            'url_source': self.start_urls[0]
            }

        # Config páginação
        if self.page_count < self.max_pages:
          next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
          if next_page:
            self.page_count += 1
            yield scrapy.Request(url=next_page,callback=self.parse)