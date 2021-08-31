import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CompanyIndexSpider(scrapy.Spider):
    name = 'company_index'
    allowed_domains = ['www.adapt.io']
    start_urls = ['https://www.adapt.io/directory/industry/telecommunications/A-1']


    def parse(self, response):
        for data in response.xpath("//div[@class='DirectoryTopInfo_alphabetLinkListWrapper__4a1SM']/div"):
            link = data.xpath(".//a/@href").get(),
            yield response.follow(url=link[0], callback=self.company_name_with_link)
    
    def company_name_with_link(self, response):
        for name_link in response.xpath("////div[@class='DirectoryList_linkItemWrapper__3F2UE ']"):
            company_name = name_link.xpath(".//a/text()").get(),
            company_link = name_link.xpath(".//a/@href").get(),
            yield{
                'name': company_name[0],
                'link': company_link[0],
            }
        next_page = response.xpath("//div[@class='DirectoryList_actionBtnLink__Seqhh undefined']/a/@href").get(),
        if next_page:
            yield response.follow(url=next_page[0], callback=self.company_name_with_link)


