from abc import *
'''
    추상화된 스크래퍼 코드
    
'''

class Scraper(metaclass=ABCMeta):
    @abstractmethod
    def scraping_process(self, channelCode, channelUrl, dateRange):
        '''
            스크래핑 진행의 전체적인 틀을 작성함
        '''
        pass
        
    @abstractmethod
    def post_list_scraping(self):
        '''
            채널 메인에서 게시글의 기본정보를 가져오기 위한 요청을 처리함
        '''
        pass

    @abstractmethod
    def collect_data(self):
        '''
            채널 메인에서 게시글의 기본 정보를 담고
            게시글 페이지에서 상세 정보를 담아오면
            이를 DB에 반영하기전 합치는 로직에 해당함
        '''
        pass

    def target_contents_scraping(self):
        '''
            채널 상세정보 수집을 위해 추가 요청이 필요한 경우(매우 빈번) 작성함
        '''
        pass

    def set_headers_process(self):
        '''
            session headers 에 cookie, content-type 등 추가 params가 필요한 경우에 작성함
        '''
        pass