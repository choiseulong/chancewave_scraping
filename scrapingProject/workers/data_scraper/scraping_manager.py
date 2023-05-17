from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from workers.scraping_scheduler.scheduler import job
from configparser import ConfigParser
from workers.error_checker.checker import ErrorChecker
import requests as req
import importlib
from datetime import datetime, timedelta
from pytz import timezone
from glob import glob
import random
from time import sleep
import os

SCRAPING_MANAGER_FILE_PATH = os.path.dirname(__file__)
SCRAPING_ROOMS_DIR_PATH = os.path.join(SCRAPING_MANAGER_FILE_PATH, 'scraper_dormitory', 'rooms')

URL_CONFIG_INI_PATH = os.path.join(SCRAPING_MANAGER_FILE_PATH, 'scraper_dormitory', 'scraper_tools', 'url.ini')
FIDDLER_PEM_PATH = os.path.join(SCRAPING_MANAGER_FILE_PATH, 'scraper_dormitory', 'scraper_tools', 'FiddlerRoot.pem')

checker = ErrorChecker()

class ScrapingManager:

    def __init__(self):
        self.channel_url_info_dict = {}
        self.date_range = []
        self.full_channel_code_list = []
    
    def get_requests_session(
            self,
            proxies = {
                "http": "http://127.0.0.1:8010",
                "https":"http:127.0.0.1:8010"
            },
            dev=True
            # proxies = {
            #     "http": "127.0.0.1:8010",
            #     "https":"127.0.0.1:8010"
            # }

        ):
        #test 시에 사용되는 session을 만든다.
        session = req.Session()
        if dev :
            session.verify = FIDDLER_PEM_PATH
            session.proxies = proxies
        elif not dev :
            session.headers = {
                "Connection": "keep-alive",
                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                # "User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"
            }  
        return session

    def get_channel_url(self):
        # url.ini에 작성된 채널 URL정보를 가져와 변수에 담는다
        config = ConfigParser()
        config.read(URL_CONFIG_INI_PATH, encoding='utf-8')
        for section in config.sections():
            section_name = section.lower()
            for item in list(config[section].items()):
                key = item[0]
                value = item[1]
                globals()[f'{section_name}_{key}'] = value
        for key in globals():
            if 'url_' in key :
                self.channel_url_info_dict.update({key[4:] : globals()[key]})
                self.full_channel_code_list.append(key[4:])

    def search_full_channel_code(self, channel_code):
        if not self.channel_url_info_dict :
            self.get_channel_url()
        for code in self.full_channel_code_list:
            if '_' + channel_code in code:
                return code

    def scraping_dev_test(self, channel_code, dev=True):
        # ulsansi_0 등의 채널코드를 받아 테스트 스크래핑을 시작한다
        if not self.channel_url_info_dict :
            self.get_channel_url()
        channel_code_with_location = self.find_channel_code_with_location(channel_code)
        group_name, room_name, channel_code, channel_url = self.parse_scraping_parameters(channel_code_with_location)
        print(group_name, channel_code, 'init')
        session = self.get_requests_session(dev=dev)
        tmp_scraper_file_name_list = get_scraper_file_list_from_group_room(group_name, room_name)
        tmp_room_num = channel_code.split('_')[1]
        scraper_room_address = None
        for tmp_scraper_file_name in tmp_scraper_file_name_list:
            # module 이름으로 변형 위해 python 확장자 제거
            tmp_module_nm = tmp_scraper_file_name[:tmp_scraper_file_name.rfind('.py')]
            if tmp_module_nm == f'scraper_{tmp_room_num}':
                scraper_room_address = f'workers.data_scraper.scraper_dormitory.rooms.{group_name}.{room_name}.{tmp_module_nm}'                
                break
        else:
            scraper_room_address = f'workers.data_scraper.scraper_dormitory.rooms.{group_name}.{room_name}.scraper'
        full_channel_code = self.search_full_channel_code(channel_code)
        scraper = importlib.import_module(scraper_room_address).Scraper(session)
        scraper.scraping_process(channel_code, channel_url, full_channel_code=full_channel_code, dev=dev)
    
    def scraping_init_with_celery(self):
        # celery 에게 스크래핑 진행을 위임한다
        channel_url_list = list(self.channel_url_info_dict.keys())
        random.shuffle(channel_url_list)
        for channel_code_with_location in channel_url_list:
            group_name, room_name, channel_code, channel_url = self.parse_scraping_parameters(channel_code_with_location)
            tmp_scraper_file_name_list = get_scraper_file_list_from_group_room(group_name, room_name)
            tmp_room_num = channel_code.split('_')[1]
            scraper_room_address = None
            for tmp_scraper_file_name in tmp_scraper_file_name_list:
                # module 이름으로 변형 위해 python 확장자 제거
                tmp_module_nm = tmp_scraper_file_name[:tmp_scraper_file_name.rfind('.py')]
                if tmp_module_nm == f'scraper_{tmp_room_num}':
                    scraper_room_address = f'workers.data_scraper.scraper_dormitory.rooms.{group_name}.{room_name}.{tmp_module_nm}'
                    break
            else:
                scraper_room_address = f'workers.data_scraper.scraper_dormitory.rooms.{group_name}.{room_name}.scraper'
            full_channel_code = self.search_full_channel_code(channel_code)
            sleep(1)
            job.delay(scraper_room_address, channel_code, channel_url, full_channel_code)

    def scraping_target_channel_list_synchronously(self):
        channel_list = ['hongcheon_2', 'gwgs_4', 'sokcho_0', 'yw_2', 'yangyang_3', 'taebaek_0', 'samcheok_3', 'cwg_1', 'yangju_0', 'suwon_1', 'gimpo_2', 'hwaseong_0', 'bucheon_2', 'anyang_3', 'goyang_0', 'gunpo_1', 'anseong_2', 'goyang_3', 'anyang_2', 'seongnam_1', 'seongnam_6', 'tongyeong_0', 'geochang_0', 'hygn_0', 'hc_0', 'yangsan_0', 'sacheon_0', 'hadong_0', 'uljin_0', 'gumi_0', 'gbmg_0', 'gc_0', 'gbgs_0', 'cheongdo_0', 'usc_0', 'kinfa_0', 'semas_0', 'kwater_0', 'koreanpc_0', 'redcross_0', 'ekr_0', 'kofic_0', 'keis_0', 'ncc_0', 'kibo_0', 'epis_0', 'bokji_0', 'kodit_0', 'nile_0', 'kra_0', 'kisa_0', 'tipa_0', 'visitkorea_0', 'kpipa_0', 'kobaco_0', 'kf_0', 'lh_0', 'kipi_0', 'bohun_0', 'kyci_0', 'koddi_0', 'khnp_0', 'i815_0', 'gwangjubukgu_1', 'gwangjunamgu_3', 'gwangsan_1', 'gwangjusi_1', 'gwangjubukgu_3', 'gwangjuseogu_1', 'gwangjunamgu_1', 'gwangjudonggu_3', 'suseong_3', 'namdaegu_1', 'dalseong_0', 'daegusi_3', 'daedeok_4', 'djjunggu_0', 'daedeok_3', 'daedeok_2', 'djdonggu_0', 'djjunggu_1', 'daejeonsi_0', 'djseogu_3', 'gijang_3', 'suyeong_2', 'dongnae_5', 'gijang_2', 'busanjin_5', 'yeonje_3', 'bsgangseo_2', 'gangseo_2', 'jongno_4', 'gwanak_0', 'songpa_1', 'mapo_2', 'songpa_3', 'eunpyeong_0', 'jongno_0', 'seongbuk_4', 'seodaemun_4', 'gangnam_1', 'dongjak_0', 'seodaemun_0', 'seongdong_2', 'seocho_2', 'gangnam_0', 'jungnang_1', 'yangcheon_1', 'gwanak_5', 'seoulcity_0', 'seocho_0', 'seocho_1', 'geumcheon_1', 'songpa_0', 'jungnang_0', 'dobong_2', 'gangnam_2', 'dobong_5', 'yongsan_0', 'gwangjin_2', 'seocho_4', 'nowon_1', 'dongjak_1', 'seoulcity_1', 'dongdaemun_5', 'gwanak_4', 'seodaemun_1', 'sejongsi_0', 'ulsanbukgu_2', 'ulsansi_6', 'ulsanbukgu_0', 'ulsansi_7', 'ongjin_0', 'yeonsu_3', 'michuhol_0', 'gyeyang_2', 'incheonsi_1', 'incheonseogu_0', 'damyang_0', 'jangseong_0', 'muan_0', 'gurye_0', 'gangjin_0', 'gokseong_0', 'gunsan_0', 'namwon_0', 'jeonbukdo_2', 'jeonbukdo_0', 'sunchang_0', 'jangsu_0', 'jangsu_1', 'jeju_2', 'jeju_3', 'jeju_1', 'jeju_0', 'jeju_5', 'mediahub_0', 'bokjiro_0', 'gcon_1', 'bizinfo_0', 'jobaba_0', 'kstartup_0', 'kocca_0', 'dapa_0', 'msit_0', 'me_0', 'mois_0', 'cha_0', 'mnd_0', 'mohw_0', 'kma_0', 'mcst_0', 'nfa_0', 'ftc_0', 'kipo_0', 'mss_0', 'moj_0', 'mfds_0', 'molit_0', 'customs_0', 'mafra_0', 'unikorea_0', 'fsc_0', 'moe_0', 'pps_0', 'mofa_0', 'nts_0', 'police_0', 'mpva_0', 'buyeo_0', 'cheongyang_2', 'yesan_3', 'seocheon_3', 'chungju_3', 'jincheon_5', 'yd21_2', 'jecheon_4', 'oc_0', 'goesan_3', 'nowon_0']
        for channel_code in channel_list:
            try:
                self.scraping_dev_test(channel_code, dev=False)
            except Exception as e :
                print(channel_code, e)
    def parse_scraping_parameters(self, channel_code_with_location):
        # 지역정보가 함께 담긴 채널 코드를 가져와서 파싱하고 return 한다
        # channel_code_with_location = ulsan__ulsansi_0의 경우
        # group_name = ulsan, room_name = ulsansi, channel_code = ulsansi_0, 
        # channel_url = channel_url_info_dict[channel_code_with_location]
        group_name = extract_group_code(channel_code_with_location)
        room_name, channel_code = extract_room_name_and_channel_code(channel_code_with_location)
        channel_url = self.channel_url_info_dict[channel_code_with_location]
        return group_name, room_name, channel_code, channel_url

    def find_channel_code_with_location(self, channel_code):
        # 개별 채널 스크래퍼 테스트시 사용한다
        # channel_code = ulsansi_0 로 받은 경우
        # 반환값은 channel_code_with_location = ulsan__ulsansi_0 이다
        for channel_code_with_location in self.channel_url_info_dict.keys():
            channel_code_split = channel_code_with_location.split('__')[1]
            if channel_code == channel_code_split :
                return channel_code_with_location

def get_scraper_file_list_from_group_room(group_name, room_name):
    total_scraper_file_list = []
    tmp_scraper_file_path_list = glob(
        os.path.join(SCRAPING_ROOMS_DIR_PATH, group_name, room_name) + os.path.sep + 'scraper*.py')
    for tmp_scraper_file_path in tmp_scraper_file_path_list:
        tmp_file_nm = os.path.basename(tmp_scraper_file_path)
        if tmp_file_nm[-3:] != '.py':
            continue
        total_scraper_file_list.append(tmp_file_nm)

    return total_scraper_file_list


def combine_group_room_num_str(group_name, room_name, room_num):
    return group_name + '__' + room_name + '_' + room_num


if __name__ == '__main__':
    print(SCRAPING_MANAGER_FILE_PATH)
    tmp_group_name = 'gyeonggi'
    tmp_room_name = 'gyeonggido'
    tmp_room_num = '0'

    URL_CODE = combine_group_room_num_str(tmp_group_name, tmp_room_name, tmp_room_num)

    config = ConfigParser()
    config.read(URL_CONFIG_INI_PATH, encoding='utf-8')

    TARGET_URL = config['URL'][URL_CODE]

    print(config['URL'][URL_CODE])
    # now = datetime.now(timezone('Asia/Seoul'))
    # todayString = now.strftime('%Y-%m-%d %H:%M:%S')
    # before2WeekString = (now-timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
    # start_date = convert_datetime_string_to_isoformat_datetime(todayString)
    # end_date = convert_datetime_string_to_isoformat_datetime(before2WeekString)

    tmp_scraper_file_name_list = get_scraper_file_list_from_group_room(group_name=tmp_group_name,
                                                                       room_name=tmp_room_name)

    scraper_room_address = None
    for tmp_scraper_file_name in tmp_scraper_file_name_list:

        # module 이름으로 변형 위해 python 확장자 제거
        tmp_module_nm = tmp_scraper_file_name[:tmp_scraper_file_name.rfind('.py')]
        if tmp_module_nm == f'scraper_{tmp_room_num}':
            print(f'{tmp_room_name} IDX {tmp_room_num}')
            scraper_room_address = f'workers.data_scraper.scraper_dormitory.rooms.{tmp_group_name}.{tmp_room_name}.{tmp_module_nm}'
            break
    else:
        print('NOT MATCH IDX')
        scraper_room_address = f'workers.data_scraper.scraper_dormitory.rooms.{tmp_group_name}.{tmp_room_name}.scraper'
    ## full_channel_code
    manager = ScrapingManager()
    full_channel_code = manager.search_full_channel_code(URL_CODE)
    ##

    session = req.Session()
    scraper = importlib.import_module(scraper_room_address).Scraper(session)
    scraper.scraping_process(URL_CODE, TARGET_URL, full_channel_code=full_channel_code)


