import scrapy


#crawl all pages of Headlines and news summary of scpecial category like sport
class TasnimCategoryTitle(scrapy.Spider):
    name = 'tasnim_title'

    start_urls=[
        'https://www.tasnimnews.com/fa/service/3/%D9%88%D8%B1%D8%B2%D8%B4%DB%8C'
    ]   

    def parse(self, response):
        for post in response.css('article.list-item'):
            for i in range(1,22):
                if post.css('article.list-item:nth-child(%i) > a:nth-child(1) > div:nth-child(2) > h4:nth-child(2)' % i).get() != None:
                    yield{
                        'category':'ورزش',
                        'body' : post.css('article.list-item:nth-child(%i) > a:nth-child(1) > div:nth-child(2) > h4:nth-child(2)::text' % i).get(),
                        'title':post.css('article.list-item:nth-child(%i) > a:nth-child(1) > div:nth-child(2) > h2:nth-child(1)::text' % i).get()
                    }
        
        for i in range(2,6):
            next_page = response.css('ul.pagination > li:nth-child(%i) > a:nth-child(1)::attr(href)' % i).get()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
            
#crawl special page
class ISNANewsPage(scrapy.Spider):
    name = 'isna_news_page'
    
    start_urls=[
        'https://www.isna.ir/news/8503-17549/%D8%B1%D9%8A%D9%8A%D8%B3-%D8%B3%D8%A7%D8%B2%D9%85%D8%A7%D9%86-%D8%B5%D8%AF%D8%A7-%D9%88-%D8%B3%D9%8A%D9%85%D8%A7-%D8%A7%D8%B2-%D9%87%D9%85%D8%B3%D8%B1%D8%A7%D9%86-%D8%B3%D8%B1%D8%AF%D8%A7%D8%B1%D8%A7%D9%86-%D8%B4%D9%87%D9%8A%D8%AF-%D8%A7%D8%B3%D8%AA%D8%A7%D9%86-%D8%A7%D8%B5%D9%81%D9%87%D8%A7%D9%86-%D8%AA%D9%82%D8%AF%D9%8A%D8%B1',
        'https://www.isna.ir/news/8503-17552/%D8%B1%D9%8A%D9%8A%D8%B3-%D8%AC%D9%85%D9%87%D9%88%D8%B1-%D8%A8%D8%B1-%D8%A7%D8%AC%D8%B1%D8%A7%D9%8A%D9%8A-%D8%B4%D8%AF%D9%86-%D9%87%D8%B1%DA%86%D9%87-%D8%B3%D8%B1%D9%8A%D8%B9-%D8%AA%D8%B1-%D8%AA%D9%88%D8%A7%D9%81%D9%82%D8%A7%D8%AA-%D8%AA%D9%87%D8%B1%D8%A7%D9%86-%D8%AE%D8%A7%D8%B1%D8%B7%D9%88%D9%85',
        'https://www.isna.ir/news/lorestan-17220/%D9%85%D8%AF%D9%8A%D8%B1%D9%83%D9%84-%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87-%D8%B1%D9%8A%D8%B2%D9%8A-%D8%A7%D8%B3%D8%AA%D8%A7%D9%86%D8%AF%D8%A7%D8%B1%D9%8A-%D9%84%D8%B1%D8%B3%D8%AA%D8%A7%D9%86-5-%D8%AF%D8%B1%D8%B5%D8%AF-%D8%A7%D8%B9%D8%AA%D8%A8%D8%A7%D8%B1%D8%A7%D8%AA-%D8%A7%D8%B4%D8%AA%D8%BA%D8%A7%D9%84%D8%B2%D8%A7%D9%8A%D9%8A'
    ]    
    
    def parse(self, response):
        
        if len(response.css('p::text').getall()) != 0:
            yield{
                'categories':response.css('.meta-news > ul:nth-child(2) > li:nth-child(2) > span:nth-child(3)::text').getall(),
                'paraghraph':response.css('p::text').getall(),
                'len':len(response.css('p::text').getall())
            }  
           
        elif len(response.css('.item-text > div:nth-child(1)::text').getall()) >1:
            yield{
                'categories':response.css('.meta-news > ul:nth-child(2) > li:nth-child(2) > span:nth-child(3)::text').getall(),
                'paraghraph':response.css('.item-text > div:nth-child(1)::text').getall(),
                'len':len(response.css('.item-text > div:nth-child(1)::text').getall())
            }
        
        else:
            yield{
                'categories':response.css('.meta-news > ul:nth-child(2) > li:nth-child(2) > span:nth-child(3)::text').getall(),
                'paraghraph':response.css('.item-text::text').getall(),
                'len':len(response.css('.item-text>strong::text').getall())
            }   

             
            

#crawl all paragraph of pages of special topic
class TasnimNEWS(scrapy.Spider):
    name = 'tasnim_news'
    
    start_urls = ['https://www.tasnimnews.com/fa/service/1412/%D8%B3%DB%8C%D8%A7%D8%B3%D8%AA-%D8%A7%DB%8C%D8%B1%D8%A7%D9%86']

    def parse(self, response):
        for href in response.css("article.list-item > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback = self.parse_page)

        for i in range(2,6):
            next_page = response.css('ul.pagination > li:nth-child(%i) > a:nth-child(1)::attr(href)' % i).get()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)    

    def parse_page(self, response):
        yield{
            'categories':[response.css('li.service:nth-child(2) a::text').getall(),response.css('li.service:nth-child(3) a::text').getall()],
            'paraghraph':response.css('p::text').getall()
        }
                                         
#crawl all pages of isna
class IsnaNews(scrapy.Spider):
    name = 'isna_all'
    
    start_urls = ['https://www.isna.ir/archive?pi=1&ms=0&dy=30&mn=3&yr=1385']
    allowed_domains = ['isna.ir']
    
    def parse(self, response):
        
        for href in response.css("li.text>div>h3> a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback = self.parse_page)
        
        for next_page in response.css('.pagination > li.page-item > a::attr(href)'):
            if next_page is not None :
                next_page = response.urljoin(next_page.extract())
                yield scrapy.Request(next_page, callback=self.parse)  

        #just crawl first page of each day
        for j in range(2,32):
            next_day = 'https://www.isna.ir/archive?pi=1&ms=0&dy='+str(j)+'&mn=5&yr=1385'
            yield scrapy.Request(next_day, callback=self.parse)   
        
        
    def parse_page(self, response):
        if len(response.css('p::text').getall()) != 0:
            yield{
                'categories':response.css('.meta-news > ul:nth-child(2) > li:nth-child(2) > span:nth-child(3)::text').getall(),
                'paraghraph':response.css('p::text').getall(),
                'len':len(response.css('p::text').getall()),
            }   
            
        elif len(response.css('.item-text > div:nth-child(1)::text').getall()) >1:
            yield{
                'categories':response.css('.meta-news > ul:nth-child(2) > li:nth-child(2) > span:nth-child(3)::text').getall(),
                'paraghraph':response.css('.item-text > div:nth-child(1)::text').getall(),
                'len':len(response.css('.item-text > div:nth-child(1)::text').getall())
                
            }

        else:
            yield{
                'categories':response.css('.meta-news > ul:nth-child(2) > li:nth-child(2) > span:nth-child(3)::text').getall(),
                'paraghraph':response.css('.item-text::text').getall(),
                'len':len(response.css('.item-text::text').getall())
            }  
            
                                             