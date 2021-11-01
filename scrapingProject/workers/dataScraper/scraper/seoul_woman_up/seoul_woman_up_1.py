'''
    0,1,2 required
    User-Agent = ''
'''

class Scraper:
    def __init__(self):
        pass

    def set_headers(self, additionalKeyValue=None):
        headers = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
        }
        if additionalKeyValue :
            for key, value in additionalKeyValue:
                headers.update({key:value})
        self.session.headers = headers

    def scraping_process(self, channelCode, channelUrl, dateRange):
        self.set_env(dateRange)
        pageCount = 1
        while True :
            self.scrapingTarget = self.post_list_scraping(channelCode, pageCount, channelUrl)
            if self.scrapingTarget :
                self.target_contents_scraping()
                self.collect_data(channelCode, channelUrl)
                self.mongo.reflect_scraped_data(self.collectedDataList)
                pageCount += 1
            else:
                print(f'{channelCode}, 유효한 포스트 미존재 지점에 도달하여 스크래핑을 종료합니다')
                break