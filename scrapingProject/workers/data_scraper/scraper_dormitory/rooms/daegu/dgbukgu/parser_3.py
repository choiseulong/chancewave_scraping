from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
'''
    Table Header Warning
    CHANNEL_URL : https://www.buk.daegu.kr/health/index.do?menu_link=/icms/bbs/selectBoardList.do&menu_id=00003291&bbsId=BBSMSTR_000000001202&bbsTyCode=BBST01&bbsAttrbCode=BBSA03&nttId=0&pageIndex=1
    Input Table Header : ['번호', '제목', '담당부서', '등록일', '조회']
    Page Table Header : ['Serial Number', 'Notice Subject', '담당부서', 'Date Created', 'Views']
'''
def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'uploader', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-02-04
    var['post_id_idx'] = 1
    var['table_header'] = ["번호", "제목", "담당부서", "등록일", "조회"]
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_title'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_meta_data = extract_children_tag(soup, 'th', is_child_multiple=True, child_tag_attrs={'scope':'row'})
    for meta_data in tmp_meta_data:
        meta_data_name = extract_text(meta_data)
        meta_data_value = extract_text(find_next_tag(meta_data))
        if 'Notice Subject' in meta_data_name:
            var['post_title'] = meta_data_value.replace('[Bulletin] ', '')
        elif '담당부서' in meta_data_name:
            var['contact'] = extract_contact_numbers_from_text(meta_data_value)
    tmp_contents = extract_children_tag(soup, 'td', child_tag_attrs={'class':'bbsViewBody'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result

