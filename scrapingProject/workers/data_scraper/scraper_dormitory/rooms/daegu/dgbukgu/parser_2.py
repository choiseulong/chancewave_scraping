from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
'''
    Table Header Warning
    CHANNEL_URL : https://www.buk.daegu.kr/index.do?menu_link=/icms/bbs/selectBoardList.do&menu_id=00000196&bbsId=BBSMSTR_000000001052&bbsTyCode=BBST01&bbsAttrbCode=BBSA03&nttId=0&pageIndex=1
    Input Table Header : ['번호', '제목', '담당부서', '등록일', '첨부', '조회']
    Page Table Header : ['Serial Number', 'Notice Subject', '담당부서', 'Date Created', '첨부', 'Views']
'''
def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'is_going_on', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    lec_list = extract_children_tag(soup, 'div', is_child_multiple=True, child_tag_attrs={'class':'lec_list'})
    for lec in lec_list:
        a_tag = extract_children_tag(lec, 'a')
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['post_url_frame'] + href
        )
        var['post_title'].append(
            extract_text_from_single_tag(lec, 'p', child_tag_attrs={'class':'le_name'})
        )
        a_tag_text = extract_text(a_tag)
        if '접수마감' in a_tag_text:
            var['is_going_on'].append(False)
        else :
            print(var['channel_code'], 'is_going_on 확인 필요')
            var['is_going_on'].append(True)

    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type':['post_text_type'],
        'multiple_type' : ['extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', child_tag_attrs={'class':'Thead'})
    tmp_meta_data = extract_children_tag(tbody, 'th', is_child_multiple=True)
    extra_info = {'info_title':'프로그램 소개'}
    for meta_data in tmp_meta_data:
        meta_data_name = extract_text(meta_data)
        meta_data_value = extract_text(find_next_tag(meta_data))
        extra_info.update({f'info_{len(extra_info)}' : (meta_data_name, meta_data_value)})
    var['extra_info'].append(extra_info)
    var['post_text_type'] = 'only_extra_info'
    result = convert_merged_list_to_dict(key_list, var)
    print(result)
    return result

