from workers.data_server.mongo_server import MongoServer
from .scraper_tools.tools import *
from .parser_tools.tools import *
import json
from abc import *

class Scraper(metaclass=ABCMeta):
    def __init__(self, session):
        # default var
        self.session = session
        self.mongo = ''
        self.channel_code = ''
        self.channel_url = ''
        self.channel_url_frame = ''
        self.page_count = 0
        self.empty_page_count = 0
        self.additional_key_value = []
        self.retry_count = 0
        self.CSRF_TOKEN = ''

        # scraped data
        self.scraping_target = []
        self.scraping_target_contents = []
        self.collected_data_list = []
        self.channel_name = ''
        self.post_board_name = ''
        self.empty_contents_dict = {}

        # additional urls
        self.post_url = ''
        self.post_url_frame = ''
        self.channel_main_url = ''

        #env
        self.dev = False
        self.limit_page_count = 6

    @abstractmethod
    def scraping_process(self, channel_code, channel_url, dev=False):
        '''
            스크래핑 진행의 틀을 작성함
        '''
        self.dev = dev
        self.mongo = MongoServer(dev)
        self.channel_code = channel_code
        self.channel_url = channel_url
        self.channel_url_frame = channel_url #page_count 적용이 필요한 경우 사용
        self.post_url_frame = self.post_url
        if not self.channel_main_url:
            self.channel_main_url = extract_channel_main_url_from_channel_url(channel_url)
        # 추가 로직 작성 必
    
    def __is_continue(self, check_num):
        if self.page_count == check_num:
            self.scraping_target = []
            return True

    def post_list_scraping(self, post_list_parsing_process, method, data={}, sleep_sec=2, jsonize=False):
        '''
            채널 메인에서 게시글의 기본정보를 가져오기 위한 요청을 처리함
        '''
        if self.__is_continue(self.limit_page_count):
            self.session.close()
            return

        self.collected_data_list = []
        if method == 'get':
            status, response = get_method_response(self.session, self.channel_url, sleep_sec)
        elif method == 'post':
            status, response = post_method_response(self.session, self.channel_url, data, sleep_sec, jsonize)
        elif method == 'urlopen':
            status, response = urlopen_response(self.channel_url, sleep_sec)

        if status == 'ok':
            self.scraping_target = post_list_parsing_process(
                response = response, 
                channel_code = self.channel_code, 
                post_url_frame = self.post_url,
                page_count = self.page_count,
                channel_main_url = self.channel_main_url,
                channel_url = self.channel_url,
                dev = self.dev,
            )

    def target_contents_scraping(self, post_content_parsing_process, sleep_sec=2):
        '''
            채널 상세정보 수집을 위해 추가 요청이 필요한 경우 작성함
        '''
        for target in self.scraping_target :
            post_content = self.target_scraping(post_content_parsing_process, target, sleep_sec)
            if post_content:
                self.scraping_target_contents.append(post_content)

    def target_scraping(self, post_content_parsing_process, target, sleep_sec):
        status = ''
        if 'contents_req_params' in target.keys():
            data = target['contents_req_params']
            status, response = post_method_response(self.session, self.post_url, data, sleep_sec)
        elif 'post_url' in target.keys():
            post_url = target['post_url']
            if type(post_url) == type(None):
                return self.empty_contents_dict
            status, response = get_method_response(self.session, post_url, sleep_sec)

        if status == 'ok':
            post_content = post_content_parsing_process(
                response = response, 
                channel_url = self.channel_url,
                post_url_frame = self.post_url,
                channel_main_url = self.channel_main_url,
                channel_code = self.channel_code,
                dev = self.dev
            )
            if post_content == 'retry' : 
                sleep(300)
                print(f'{self.channel_code} - retry : {self.retry_count}')
                self.retry_count += 1
                if self.retry_count == 3:
                    self.retry_count = 0
                    post_content = []
                else :
                    post_content = self.target_scraping(post_content_parsing_process, target, sleep_sec)
            return post_content

    def collect_data(self):
        '''
            채널 메인에서 게시글의 기본 정보를 담고
            게시글 페이지에서 상세 정보를 담아오면
            이를 DB에 반영하기전 합치는 로직에 해당함
        '''
        if not self.scraping_target_contents:
            self.scraping_target_contents = [{} for _ in range(len(self.scraping_target))] 
        for target_info, target_contents in zip(self.scraping_target, self.scraping_target_contents):
            if 'contents_req_params' in target_info.keys():
                req_body = target_info['contents_req_params']
                del target_info['contents_req_params']
                if 'post_url' not in target_info.keys():
                    target_info.update({'post_url': self.post_url + json.dumps(req_body)}) 
                    post_url_can_use = False
                else :
                    post_url_can_use = True
            elif 'contents_req_params' not in target_info.keys() and 'post_url' in target_info.keys() :
                post_url_can_use = True
            else:
                post_url_can_use = None
            data_frame = get_post_data_frame(self.channel_code, self.channel_url, post_url_can_use, self.channel_name, self.post_board_name)
            data_frame_with_target_info = enter_data_into_data_frame(data_frame, target_info)
            data_frame_with_target_contents = enter_data_into_data_frame(data_frame_with_target_info, target_contents)
            self.collected_data_list.append(data_frame_with_target_contents)
        self.scraping_target_contents = []
        self.scraping_target = []