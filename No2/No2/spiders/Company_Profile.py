import scrapy

class CompanyProfileSpider(scrapy.Spider):
    name = 'Company_Profile'
    allowed_domains = ['www.adapt.io']
    start_urls = ['https://www.adapt.io/directory/industry/telecommunications/A-1']

    def parse(self, response):
        for data in response.xpath("//div[@class='DirectoryTopInfo_alphabetLinkListWrapper__4a1SM']/div"):
            link = data.xpath(".//a/@href").get(),
            yield response.follow(url=link[0], callback=self.company_name_with_link)
    
    def company_name_with_link(self, response):
        for name_link in response.xpath("//div[@class='DirectoryList_linkItemWrapper__3F2UE ']"):
            company_name = name_link.xpath(".//a/text()").get(),
            company_link = name_link.xpath(".//a/@href").get(),
            yield response.follow(url=company_link[0], callback=self.company_profile)

        next_page = response.xpath("//div[@class='DirectoryList_actionBtnLink__Seqhh undefined']/a/@href").get(),
        if next_page:
            yield response.follow(url=next_page[0], callback=self.company_name_with_link)

    def company_profile(self, response):
        tag_count = response.xpath("//div[@class='CompanyTopInfo_infoItem__2Ufq5']")
        tag_len = len(tag_count),
        conpany_name=response.xpath("//div[@class='CompanyTopInfo_leftContentWrap__3gIch']/h1/text()").get(),
        company_website = response.xpath("//div[@class='CompanyTopInfo_websiteUrl__13kpn']/text()").get(),
        company_webdomian = company_website[0].split("www.")[-1],
        global company_revenue
        global company_employe_size
        global company_industry
        global company_location
        global contact_details
        global contact_dict

        if tag_len[0]==4:
            company_revenue = response.xpath("(//div[@class='CompanyTopInfo_infoItem__2Ufq5']/div[2]/span[2])[1]/text()").get(),
            company_employe_size = response.xpath("(//div[@class='CompanyTopInfo_infoItem__2Ufq5']/div[2]/span[2])[2]/text()").get(),
            company_industry = response.xpath("(//div[@class='CompanyTopInfo_infoItem__2Ufq5']/div[2]/span[2])[3]/text()").get(),
            location1 = response.xpath("(//div[@class='CompanyTopInfo_infoItem__2Ufq5']/div[2]/span[2])[4]/span[@itemprop='addressLocality']/text()").get(),
            location2 = response.xpath("(//div[@class='CompanyTopInfo_infoItem__2Ufq5']/div[2]/span[2])[4]/span/span[@itemprop='addressRegion']/text()").get(),
            location3 = response.xpath("(//div[@class='CompanyTopInfo_infoItem__2Ufq5']/div[2]/span[2])[4]/span/span[@itemprop='addressCountry']/text()").get(),
            company_location = str(location1[0])+', '+str(location2[0])+', '+str(location3[0]),          

        elif tag_len[0]<4:
            div_list = response.xpath("//div[@class='CompanyTopInfo_rightContentWrap__1u0Pp']/div"),
            div_len = len(div_list),

            if div_len[0]>0:
                for span_list in response.xpath("//div[@class='CompanyTopInfo_rightContentWrap__1u0Pp']/div"):
                    span_list1 = span_list.xpath(".//div[@class='CompanyTopInfo_contentWrapper__2Jkic']/span[1]/text()").get(),

                    if span_list1[0]=='Revenue':
                        company_revenue = span_list.xpath(".//div[@class='CompanyTopInfo_contentWrapper__2Jkic']/span[2]/text()").get(),
                    elif span_list1[0]=='Head Count':
                        company_employe_size = span_list.xpath(".//div[@class='CompanyTopInfo_contentWrapper__2Jkic']/span[2]/text()").get(),
                    elif span_list1[0]=='Industry':
                        company_industry = span_list.xpath(".//div[@class='CompanyTopInfo_contentWrapper__2Jkic']/span[2]/text()").get(),
                    elif span_list1[0]=='Location':
                        location1 = response.xpath("//span[@itemprop='addressLocality']/text()").get(),
                        location2 = response.xpath("//span[@itemprop='addressRegion']/text()").get(),
                        location3 = response.xpath("(//span[@itemprop='addressCountry'])[1]/text()").get(),
                        company_location = str(location1[0])+', '+str(location2[0])+', '+str(location3[0]),
            
        contact_list = response.xpath("//div[@class='TopContacts_topContactList__lnim_']"),
        contact_list_len = len(contact_list),
        contact_details = []
        if contact_list_len[0]>0:
            for contact_persons in response.xpath("//div[@class='TopContacts_roundedBorder__1a3yB undefined']"):
                contact_name = contact_persons.xpath(".//div[@class='TopContacts_contactName__3N-_e']/a/text()").get(),
                contact_jobtitle = contact_persons.xpath(".//p[@class='TopContacts_jobTitle__3M7A2']/text()").get(),
                contact_email= contact_persons.xpath(".//button/text()").get(),
                contact_webdomain= contact_email[0].split("@")[-1].lstrip('(').rstrip('),'),
                contact_info = '{"contact_name":'+'"'+contact_name[0]+'",'+'"contact_jobtitle":'+'"'+contact_jobtitle[0]+'",'+'"contact_webdomain":'+'"'+contact_webdomain[0]+'"}',
                contact_details.append(contact_info[0]),


        yield{
            'conpany_name': conpany_name[0],
            'company_website': company_website[0],
            'company_webdomain': company_webdomian[0],
            'company_revenue': company_revenue[0],
            'company_employe_size': company_employe_size[0],
            'company_industry': company_industry[0],
            'company_location': company_location[0],
            'contact_details': contact_details,
        }

